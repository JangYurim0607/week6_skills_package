#!/usr/bin/env python3
"""Roblox 숏츠 키워드 분석 (확장판).

기존 버전(scripts/_orig/keyword_analysis_orig.py)에서 바뀐 점:
  - 조사 노트(game_notes.md)가 있는 게임만 '제작 가능'으로 분류한다. 노트 없는 게임은 사실 규칙 때문에
    대본을 쓸 수 없으므로 후보에서 뺀다(원래 버전은 노트 없는 obby 게임을 3위로 뽑았다).
  - seo-keyword-research 스킬의 4가지 검색 의도(정보/비교·탐색/거래/내비게이션)로 분류하고,
    숏츠에 맞지 않는 오락형을 따로 둔다.
  - 스킬의 우선순위 공식(Volume x CTR x Business value / (KD+1))은 검색량과 KD가 없어 계산하지 못한다.
    대신 수요 대리 점수 + 가중치 민감도 점검을 계산한다.
  - 장르 묶음 차트와 산점도를 만든다(matplotlib, Noto Sans CJK JP).

검색량 데이터는 없다. 수요 점수는 동시 접속자와 누적 방문수를 섞은 대리 지표이며 검색량이 아니다.
키워드는 템플릿과 조사 노트에서 만든 '후보'이고 검증된 값이 아니다.

사용: python3 keyword_analysis.py --csv data/roblox_games.csv --notes data/game_notes.md --out DIR
"""
import argparse
import csv
import json
import math
import re
from collections import defaultdict
from pathlib import Path

FAMILIES = {
    "social_rp": ["roleplay", "social deduction"],
    "grind_collect": ["simulator", "pet-trading", "idle", "rng", "fishing", "meme", "steal"],
    "horror_survival": ["survival", "horror"],
    "combat": ["anime", "shooter", "combat", "rpg"],
    "obby": ["obby"],
    "fashion_avatar": ["fashion", "avatar"],
}

FAMILY_KO = {
    "social_rp": "역할놀이·사회추리",
    "grind_collect": "수집·육성·시뮬레이터",
    "horror_survival": "생존·공포",
    "combat": "전투·액션·슈터",
    "obby": "장애물(오비)",
    "fashion_avatar": "패션·아바타",
}

GENRE_KO = {
    "Roleplay": "역할놀이",
    "Pet-trading": "펫 교환",
    "Fast-cycle obby": "빠른 순환 오비",
    "Survival/Horror": "생존·공포",
    "Competitive shooter": "경쟁 슈터",
    "Anime grind RPG": "애니 노가다 RPG",
    "Social deduction": "사회추리",
    "Anime action-combat": "애니 액션 전투",
    "Meme/Steal-game": "밈·훔치기",
    "Fishing simulator": "낚시 시뮬레이터",
    "Idle/tycoon": "방치형·타이쿤",
    "RNG clicker": "RNG 클리커",
    "Fashion competition": "패션 경쟁",
    "Simulator": "시뮬레이터",
    "Avatar sandbox": "아바타 샌드박스",
}

# seo-keyword-research 스킬 Step 3의 4분류 + 숏츠용 오락형
INTENT_KO = {
    "informational": "정보형",
    "commercial": "비교·탐색형",
    "transactional": "거래형",
    "navigational": "내비형",
    "entertainment": "오락형(스킬 분류 밖)",
}

# 노트 없는 게임용 템플릿 후보 (한국어 수식어, 영어 수식어, 의도, 숏츠 앵글). 게임 내용에 대한 주장은 담지 않는다.
TEMPLATE_MODS = [
    ("초보 공략", "beginner guide", "informational", "초보가 막히는 구간 하나 해결"),
    ("업데이트", "update", "navigational", "신규 업데이트 요약"),
    ("버그 모음", "glitch", "entertainment", "웃긴 장면 모음"),
]

# 노트가 있는 게임의 내용 기반 후보. 모든 앵글은 game_notes.md에 있는 내용만 가리킨다.
# (한국어 후보, 영어 후보, 의도, 숏츠 앵글, 근거 노트 항목)
CONTENT_KEYWORDS = {
    "Brookhaven RP": [
        ("Brookhaven RP 시작 방법", "brookhaven rp how to start", "informational", "집 잡고 차 타고 합류까지 한 판 따라가기", "시작이 쉽다(약 1분)"),
        ("Brookhaven RP 집 종류", "brookhaven rp houses", "informational", "집·테마 장소 115개 이상 중 몇 곳 구경", "집과 테마 장소 115개 이상"),
        ("Brookhaven RP 무료 탈것", "brookhaven rp free vehicles", "informational", "무료 탈것 24개 이상 중 타 보기", "탈것 190개 이상, 24개 이상 무료"),
        ("Brookhaven RP 게임패스 가격", "brookhaven rp gamepass price", "transactional", "유료 탈것 275~799 로벅스 정리", "게임패스 275~799 로벅스"),
        ("Brookhaven RP 직업 보수", "brookhaven rp jobs pay", "informational", "직업 아이콘은 장식, 보수 없음 확인", "직업 아이콘 80개 이상, 보수 없음"),
        ("Brookhaven RP 업데이트", "brookhaven rp update", "navigational", "금요일 주 단위 업데이트 확인", "업데이트는 보통 금요일 주 단위"),
        ("Brookhaven RP 안전", "is brookhaven rp safe", "informational", "채팅 기반 안전 우려 소개(민감, 제작 보류)", "Common Sense 등급 8+"),
    ],
    "Adopt Me!": [
        ("Adopt Me 네온 펫 만들기", "adopt me how to make neon pets", "informational", "다 자란 같은 종류 펫 4마리 합치기", "펫 4마리 합치면 네온"),
        ("Adopt Me 메가 네온", "adopt me mega neon", "informational", "네온 4마리를 합치면 메가 네온", "네온 4마리 합치면 메가 네온"),
        ("Adopt Me 알 종류 펫", "adopt me eggs pets", "informational", "알마다 나오는 펫이 다르다", "알 종류마다 나오는 펫이 다름"),
        ("Adopt Me 펫 희귀도", "adopt me pet rarity", "informational", "희귀도 5단계 소개", "희귀도 5단계"),
        ("Adopt Me 교환 사기", "adopt me trading scam", "informational", "거래 면허와 사기 경고가 생긴 이유", "2020년 거래 면허·사기 경고"),
        ("Adopt Me 로벅스 펫", "adopt me robux pets", "transactional", "로벅스로만 파는 펫이 있다", "로벅스로만 파는 펫도 있음"),
    ],
    "99 Nights in the Forest": [
        ("99 Nights in the Forest 공략", "99 nights in the forest guide", "informational", "낮에는 모으고 저녁엔 캠프로 돌아오는 루틴", "낮 탐색, 저녁 캠프 복귀"),
        ("99 Nights 모닥불 연료", "99 nights in the forest campfire fuel", "informational", "연료는 나무, 나가기 전 여분 챙기기", "모닥불 연료는 나무"),
        ("99 Nights 클래스", "99 nights in the forest classes", "commercial", "클래스 4가지 비교", "클래스 4가지"),
        ("99 Nights 솔로 vs 멀티", "99 nights in the forest solo vs multiplayer", "commercial", "멀티가 더 수월한 이유와 역할 분담", "멀티가 더 수월, 역할 분담"),
        ("99 Nights 실종된 아이", "99 nights in the forest missing children", "informational", "숲에 흩어진 아이 구하기", "실종된 아이들을 구하는 것이 목표"),
        ("99 Nights 적 종류", "99 nights in the forest enemies", "informational", "뒤로 갈수록 무리가 커지는 적", "뒤로 갈수록 무리가 커지고 빨라짐"),
    ],
    "Steal a Brainrot": [
        ("Steal a Brainrot 기지 방어", "steal a brainrot base defense", "informational", "비싼 것은 뒤쪽, 싼 것은 앞쪽 미끼", "방어와 미끼 배치"),
        ("Steal a Brainrot 리버스 시기", "steal a brainrot rebirth when", "informational", "첫 리버스 권장 시점(가이드 기준)", "첫 리버스 약 8~10시간 뒤"),
        ("Steal a Brainrot 희귀도", "steal a brainrot rarity tiers", "commercial", "희귀도 단계 정리(가이드 수치 불일치 있음)", "희귀도 6단계"),
        ("Steal a Brainrot 훔치기 게이지", "steal a brainrot steal gauge", "informational", "슬롯에 닿으면 게이지가 차는 방식", "훔치기 게이지"),
    ],
}


def parse_noted_games(notes_path):
    names = []
    for line in Path(notes_path).read_text(encoding="utf-8").splitlines():
        m = re.match(r"^##\s+\d+\.\s+(.+?)\s*$", line)
        if m:
            names.append(m.group(1))
    return names


def family_of(genre):
    g = genre.lower()
    for fam, keys in FAMILIES.items():
        if any(k in g for k in keys):
            return fam
    return "other"


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def norm_ccu(ccu):
    return (math.log10(ccu) - 4) / (math.log10(500000) - 4) * 100


def norm_visits(v):
    return (math.log10(v) - 0.5) / (math.log10(90) - 0.5) * 100


def demand_score(ccu, visits, w_ccu=0.6):
    """0~100. 동시 접속자와 누적 방문수를 로그 스케일로 섞는다. 한쪽이 없으면 있는 값만 쓴다(그 경우 점수 신뢰도가 낮다)."""
    parts = []
    if ccu:
        parts.append(norm_ccu(ccu))
    if visits:
        parts.append(norm_visits(visits))
    if not parts:
        return 0.0
    if len(parts) == 2:
        s = w_ccu * parts[0] + (1 - w_ccu) * parts[1]
    else:
        s = parts[0]
    return round(max(0.0, min(100.0, s)), 1)


def load_games(csv_path, noted):
    games = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ccu = num(row["live_players_approx"])
            visits = num(row["lifetime_visits_b"])
            name = row["game"].strip()
            games.append({
                "rank": int(row["rank"]),
                "game": name,
                "genre": row["genre"].strip(),
                "genre_ko": GENRE_KO.get(row["genre"].strip(), row["genre"].strip()),
                "family": family_of(row["genre"]),
                "ccu": ccu,
                "visits": visits,
                "score": demand_score(ccu, visits),
                "has_notes": name in noted,
                "data_gap": "동접 없음" if ccu is None else ("방문수 없음" if visits is None else ""),
            })
    return games


def pick_top(games, k, require_notes=True, w_ccu=0.6):
    pool = [g for g in games if (g["has_notes"] or not require_notes)]
    scored = sorted(pool, key=lambda g: -demand_score(g["ccu"], g["visits"], w_ccu))
    picks, used = [], set()
    for g in scored:
        if g["family"] in used:
            continue
        picks.append(g["game"])
        used.add(g["family"])
        if len(picks) == k:
            break
    return picks


def make_charts(games, outdir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager as fm

    plt.rcParams["font.family"] = "Noto Sans CJK JP"
    plt.rcParams["axes.unicode_minus"] = False
    ink, mute, accent = "#1f2937", "#6b7280", "#2563eb"
    palette = ["#2563eb", "#0d9488", "#d97706", "#7c3aed", "#db2777", "#4b5563", "#16a34a"]

    # 차트 1: 장르 묶음별 동접 합계 + 게임당 평균(마커)
    by_fam = defaultdict(list)
    for g in games:
        by_fam[g["family"]].append(g)
    order = sorted(by_fam, key=lambda f: -sum((x["ccu"] or 0) for x in by_fam[f]))
    fig, ax = plt.subplots(figsize=(7.2, 3.9), dpi=200)
    for i, fam in enumerate(order):
        with_ccu = [x for x in by_fam[fam] if x["ccu"]]
        tot = sum(x["ccu"] for x in with_ccu) / 1000
        avg = tot / len(with_ccu)
        ax.barh(i, tot, color=accent, height=0.55, alpha=0.9)
        ax.scatter([avg], [i], marker="D", s=38, color="#f59e0b", edgecolor="white", linewidth=0.8, zorder=4)
        top = max(with_ccu, key=lambda x: x["ccu"])["game"].split(" (")[0]
        n_missing = len(by_fam[fam]) - len(with_ccu)
        extra = f", 동접 수치 없음 {n_missing}개" if n_missing else ""
        ax.text(tot + 12, i - 0.08, f"합계 {tot:,.0f}K  (게임 {len(by_fam[fam])}개{extra})", va="center", fontsize=7.5, color=ink)
        ax.text(tot + 12, i + 0.2, f"1위 {top[:34]}", va="center", fontsize=6.8, color=mute)
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([FAMILY_KO[f] for f in order], fontsize=9, color=ink)
    ax.invert_yaxis()
    ax.set_xlabel("동시 접속자 (천 명, RoWatcher 2026-06-10 스냅샷)", fontsize=8.5, color=mute)
    ax.set_xlim(0, 1450)
    ax.tick_params(axis="x", labelsize=8, colors=mute)
    for s_ in ("top", "right", "left"):
        ax.spines[s_].set_visible(False)
    ax.spines["bottom"].set_color("#d1d5db")
    ax.scatter([], [], marker="D", s=38, color="#f59e0b", label="게임당 평균 동접")
    ax.barh([], [], color=accent, label="묶음 동접 합계")
    ax.legend(fontsize=7.5, frameon=False, loc="lower right")
    ax.set_title("장르 묶음별 수요 비교 (동접 기준, 검색량 아님)", fontsize=10.5, color=ink, loc="left")
    fig.tight_layout()
    fig.savefig(outdir / "chart_clusters.png")
    plt.close(fig)

    # 차트 2: 동접 vs 누적 방문수 산점도 (둘 다 있는 게임만)
    fig, ax = plt.subplots(figsize=(7.2, 3.9), dpi=200)
    pts = [g for g in games if g["ccu"] and g["visits"]]
    for g in pts:
        pick = g.get("picked")
        col = "#dc2626" if pick else (accent if g["has_notes"] else "#9ca3af")
        ax.scatter(g["visits"], g["ccu"] / 1000, s=70 if pick else 45, color=col, zorder=3, edgecolor="white", linewidth=0.8)
        name = g["game"].split(" (")[0]
        dx, dy, ha = 1.04, 0, "left"
        if g["game"] == "Murder Mystery 2":
            dy = -14
        if g["game"] == "Adopt Me!":
            dy = 12
        if g["game"] == "99 Nights in the Forest":
            dy = -10
        ax.annotate(name, (g["visits"], g["ccu"] / 1000), xytext=(6, dy / 2), textcoords="offset points", fontsize=7.5, color=ink, ha=ha, va="center")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(8, 140)
    ax.set_ylim(60, 700)
    ax.set_xticks([10, 20, 40, 80])
    ax.set_xticklabels(["100억", "200억", "400억", "800억"])
    ax.set_yticks([100, 200, 400])
    ax.set_yticklabels(["10만", "20만", "40만"])
    from matplotlib.ticker import NullFormatter
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.set_xlabel("누적 방문수 (로그 눈금)", fontsize=8.5, color=mute)
    ax.set_ylabel("동시 접속자 (로그 눈금)", fontsize=8.5, color=mute)
    ax.tick_params(labelsize=8, colors=mute)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(True, color="#e5e7eb", linewidth=0.6, zorder=0)
    ax.set_title(f"동접 대비 누적 방문수 (둘 다 수치가 있는 {len(pts)}개 게임)", fontsize=10.5, color=ink, loc="left")
    ax.scatter([], [], color="#dc2626", label="선정 3개")
    ax.scatter([], [], color=accent, label="조사 노트 있음")
    ax.scatter([], [], color="#9ca3af", label="조사 노트 없음(제작 불가)")
    ax.legend(fontsize=7.5, frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(outdir / "chart_scatter.png")
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--notes", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--no-charts", action="store_true")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    noted = set(parse_noted_games(args.notes))
    games = load_games(args.csv, noted)
    missing = noted - {g["game"] for g in games}
    assert not missing, f"CSV에 없는 노트 게임: {missing}"

    # 1) 템플릿 후보(노트 없는 게임) + 내용 기반 후보(노트 있는 게임)
    rows = []
    for g in games:
        if g["has_notes"]:
            for ko, en, intent, angle, basis in CONTENT_KEYWORDS[g["game"]]:
                rows.append({"game": g["game"], "family": g["family"], "kind": "내용 기반", "keyword_ko": ko,
                             "keyword_en": en, "intent": intent, "intent_ko": INTENT_KO[intent],
                             "shorts_angle": angle, "notes_basis": basis, "demand_score": g["score"],
                             "verified": "아니오(검색량 없음)"})
        else:
            for ko, en, intent, angle in TEMPLATE_MODS:
                short = g["game"].split(" (")[0]
                rows.append({"game": g["game"], "family": g["family"], "kind": "템플릿", "keyword_ko": f"{short} {ko}",
                             "keyword_en": f"roblox {short.lower()} {en}", "intent": intent,
                             "intent_ko": INTENT_KO[intent], "shorts_angle": angle, "notes_basis": "",
                             "demand_score": g["score"], "verified": "아니오(검색량 없음)"})
    with open(out / "keywords.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # 2) 선정 + 가중치 민감도
    picks = pick_top(games, args.top)
    for g in games:
        g["picked"] = g["game"] in picks
    pure_top = pick_top(games, args.top, require_notes=True)
    sens = {}
    for label, w in [("동접60:방문40(기본)", 0.6), ("동접만", 1.0), ("방문만", 0.0), ("50:50", 0.5)]:
        pool = [g for g in games if g["has_notes"]]
        if w == 1.0:
            sc = {g["game"]: round(norm_ccu(g["ccu"]), 1) for g in pool if g["ccu"]}
        elif w == 0.0:
            sc = {g["game"]: round(norm_visits(g["visits"]), 1) for g in pool if g["visits"]}
        else:
            sc = {g["game"]: demand_score(g["ccu"], g["visits"], w) for g in pool}
        rank = sorted(sc, key=lambda k: -sc[k])
        sens[label] = {"scores": sc, "order": rank,
                       "picks_with_cluster_rule": pick_top(games, args.top, True, w) if w not in (1.0, 0.0) else None}
    # 군집 규칙 없는 순수 상위 3
    plain = sorted([g for g in games if g["has_notes"]], key=lambda g: -g["score"])[: args.top]
    (out / "sensitivity.json").write_text(json.dumps({
        "picks_cluster_rule": picks,
        "plain_top_by_score_among_noted": [g["game"] for g in plain],
        "weightings": sens,
        "note": "동접만/방문만 가중치에서는 점수 순서만 비교했다. 군집 규칙은 기본 가중치에서만 적용.",
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    # 3) 군집 요약
    by_fam = defaultdict(list)
    for g in games:
        by_fam[g["family"]].append(g)
    lines = ["# 클러스터 요약", "", "수요 점수는 동시 접속자와 누적 방문수를 섞은 대리 지표입니다(검색량 아님).", ""]
    summ = []
    for fam, gs in sorted(by_fam.items(), key=lambda kv: -sum(x["ccu"] or 0 for x in kv[1])):
        gs = sorted(gs, key=lambda x: -x["score"])
        tot = sum(x["ccu"] or 0 for x in gs)
        avg = sum(x["score"] for x in gs) / len(gs)
        summ.append({"family": fam, "label": FAMILY_KO[fam], "n": len(gs), "ccu_total": tot,
                     "n_missing_ccu": sum(1 for x in gs if not x["ccu"]), "avg_score": round(avg, 1),
                     "games": [x["game"] for x in gs]})
        lines.append(f"## {FAMILY_KO[fam]} (게임 {len(gs)}개, 동접 합계 {tot:,.0f}, 평균 점수 {avg:.1f})")
        for x in gs:
            ccu = f"{int(x['ccu']):,}" if x["ccu"] else "수치 없음"
            lines.append(f"- {x['game']} / {x['genre']} / 동접 {ccu} / 점수 {x['score']} / 조사 노트 {'있음' if x['has_notes'] else '없음'}")
        lines.append("")
    (out / "cluster_summary.md").write_text("\n".join(lines), encoding="utf-8")
    (out / "cluster_summary.json").write_text(json.dumps(summ, ensure_ascii=False, indent=2), encoding="utf-8")

    (out / "games.json").write_text(json.dumps(games, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "top_picks.json").write_text(json.dumps(
        [{"game": g["game"], "genre": g["genre"], "family": g["family"], "score": g["score"]}
         for g in games if g["game"] in picks], ensure_ascii=False, indent=2), encoding="utf-8")

    if not args.no_charts:
        make_charts(games, out)

    print(f"게임 {len(games)}개 (조사 노트 있음 {len(noted)}개), 키워드 후보 {len(rows)}개 -> {out}")
    print("선정(군집당 1개, 노트 있는 게임만):", ", ".join(picks))
    print("노트 있는 게임 점수순:", ", ".join(f"{g['game']} {g['score']}" for g in sorted([x for x in games if x['has_notes']], key=lambda x: -x['score'])))
    for k, v in sens.items():
        print(f"  [{k}] 순서:", " > ".join(v["order"]), "| 군집규칙 선정:", v["picks_with_cluster_rule"])


if __name__ == "__main__":
    main()
