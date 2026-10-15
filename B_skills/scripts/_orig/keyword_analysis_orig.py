#!/usr/bin/env python3
"""Roblox 숏츠 키워드 분석 (표준 라이브러리만 사용).

입력: data/roblox_games.csv
출력: --out 디렉터리에
  - keywords.csv          게임 x 수식어 키워드 후보 + 수요 점수 + 의도 + 숏츠 앵글
  - cluster_summary.md    장르 클러스터별 요약
  - top_picks.json        대본 작성에 넘길 상위 게임

주의: 검색량 데이터가 없으므로 수요 점수는 동시 접속자와 누적 방문수를 섞은 대리 지표다.
키워드는 템플릿으로 만든 '후보'이며 실제 검색량으로 검증된 값이 아니다.
"""
import argparse
import csv
import json
import math
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

# (한국어 수식어, 영어 수식어, 의도, 숏츠 앵글)
MODIFIERS = [
    ("꿀팁", "tips", "informational", "30초 꿀팁 한 가지"),
    ("공략", "guide", "informational", "초보가 막히는 구간 해결"),
    ("모르면 손해", "mistakes", "informational", "흔한 실수 3개"),
    ("신기록", "world record", "entertainment", "기록 도전 / 챌린지"),
    ("아이템 순위", "best items", "commercial", "아이템 티어 정리"),
    ("버그", "glitch", "entertainment", "웃긴 버그 모음"),
    ("업데이트", "update", "news", "신규 업데이트 요약"),
    ("vs", "vs", "commercial", "두 선택지 비교"),
]


def family_of(genre: str) -> str:
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


def demand_score(ccu, visits):
    """0~100. 동시 접속자(60%)와 누적 방문수(40%)를 로그 스케일로 섞는다. 둘 중 하나가 없으면 있는 값만 쓴다."""
    parts = []
    if ccu:
        parts.append((math.log10(ccu) - 4) / (math.log10(500000) - 4) * 100)
    if visits:
        parts.append((math.log10(visits) - 0.5) / (math.log10(90) - 0.5) * 100)
    if not parts:
        return 0.0
    if len(parts) == 2:
        s = 0.6 * parts[0] + 0.4 * parts[1]
    else:
        s = parts[0]
    return round(max(0.0, min(100.0, s)), 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--top", type=int, default=3, help="대본 대상 게임 수")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    games = []
    with open(args.csv, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ccu = num(row["live_players_approx"])
            visits = num(row["lifetime_visits_b"])
            games.append(
                {
                    "game": row["game"].strip(),
                    "genre": row["genre"].strip(),
                    "family": family_of(row["genre"]),
                    "ccu": ccu,
                    "visits": visits,
                    "score": demand_score(ccu, visits),
                }
            )

    rows = []
    for g in games:
        for ko, en, intent, angle in MODIFIERS:
            rows.append(
                {
                    "game": g["game"],
                    "family": g["family"],
                    "keyword_ko": f"로블록스 {g['game']} {ko}",
                    "keyword_en": f"roblox {g['game'].lower()} {en}",
                    "intent": intent,
                    "shorts_angle": angle,
                    "demand_score": g["score"],
                }
            )
    rows.sort(key=lambda r: (-r["demand_score"], r["game"], r["intent"]))
    with open(out / "keywords.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    by_fam = defaultdict(list)
    for g in games:
        by_fam[g["family"]].append(g)

    lines = ["# 클러스터 요약", "", "수요 점수는 동시 접속자와 누적 방문수를 섞은 대리 지표입니다(검색량 아님).", ""]
    fam_rank = sorted(by_fam.items(), key=lambda kv: -sum(x["score"] for x in kv[1]) / len(kv[1]))
    for fam, gs in fam_rank:
        gs = sorted(gs, key=lambda x: -x["score"])
        avg = sum(x["score"] for x in gs) / len(gs)
        lines.append(f"## {fam} (게임 {len(gs)}개, 평균 점수 {avg:.1f})")
        for x in gs:
            ccu = f"{int(x['ccu']):,}" if x["ccu"] else "수치 없음"
            lines.append(f"- {x['game']} / {x['genre']} / 동접 {ccu} / 점수 {x['score']}")
        lines.append("")
    (out / "cluster_summary.md").write_text("\n".join(lines), encoding="utf-8")

    # 장르가 겹치지 않게 상위 게임을 고른다 (클러스터당 1개)
    picks, used = [], set()
    for g in sorted(games, key=lambda x: -x["score"]):
        if g["family"] in used:
            continue
        picks.append({"game": g["game"], "genre": g["genre"], "family": g["family"], "score": g["score"]})
        used.add(g["family"])
        if len(picks) == args.top:
            break
    (out / "top_picks.json").write_text(json.dumps(picks, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"게임 {len(games)}개, 키워드 후보 {len(rows)}개 -> {out}")
    for p in picks:
        print(f"  pick: {p['game']} ({p['family']}, {p['score']})")


if __name__ == "__main__":
    main()
