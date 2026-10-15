#!/usr/bin/env python3
"""keyword_analysis.pdf 생성. 입력은 keyword_analysis.py 가 만든 output/artifacts/keyword_run/."""
import base64
import csv
import html
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from pdf_common import BASE_CSS, render_pdf  # noqa: E402
from keyword_analysis import INTENT_KO, FAMILY_KO  # noqa: E402

OUT = HERE.parent / "output"
RUN = OUT / "artifacts" / "keyword_run"


def esc(s):
    return html.escape(str(s))


def img(name, cls=''):
    b = base64.b64encode((RUN / name).read_bytes()).decode()
    return f"<img class='{cls}' src='data:image/png;base64,{b}'>"


def fmt_ccu(x):
    return f"{int(x):,}" if x else "수치 없음"


def fmt_v(x):
    return f"{x:.1f}" if x else "수치 없음"


def main():
    games = json.loads((RUN / "games.json").read_text(encoding="utf-8"))
    kws = list(csv.DictReader(open(RUN / "keywords.csv", encoding="utf-8")))
    sens = json.loads((RUN / "sensitivity.json").read_text(encoding="utf-8"))
    clusters = json.loads((RUN / "cluster_summary.json").read_text(encoding="utf-8"))
    by = {g["game"]: g for g in games}
    picks = sens["picks_cluster_rule"]
    n_noted = sum(1 for g in games if g["has_notes"])
    n_noccu = sum(1 for g in games if not g["ccu"])
    n_novis = sum(1 for g in games if not g["visits"])
    n_both = sum(1 for g in games if g["ccu"] and g["visits"])

    css = BASE_CSS + """
    h1 { font-size: 21pt; } .sub { color: var(--mute); font-size: 9.6pt; margin-bottom: 8pt; }
    .grid3 { display:grid; grid-template-columns: repeat(3, 1fr); gap: 7pt; margin: 6pt 0; }
    .card { border:.8pt solid var(--rule); border-radius:4pt; padding:6pt 8pt; font-size:8.6pt; }
    .card .gn { font-size:11pt; font-weight:800; } .card .big { font-size:17pt; font-weight:800; color: var(--accent); line-height:1.1; }
    .card .rk { color: var(--mute); font-size:7.8pt; }
    table.t th, table.t td { font-size: 8.1pt; padding: 2.6pt 4pt; }
    table.g16 th, table.g16 td { font-size: 7.9pt; padding: 2.2pt 4pt; white-space: nowrap; }
    img.sc { width: 88%; }
    table.k th, table.k td { font-size: 7.5pt; padding: 1.5pt 4pt; line-height:1.35; }
    .sel { background:#eff6ff; }
    .dim { color: #9ca3af; }
    .ban { background:#fffbeb; border:.8pt solid #f59e0b; border-radius:4pt; padding:4pt 8pt; font-size:8.4pt; margin: 4pt 0 6pt; }
    .tree { font-size:8.2pt; } .tree b { color: var(--accent); }
    """

    H = [f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>로블록스 숏츠 키워드 분석 리포트</title><style>{css}</style></head><body>"]

    # ------------------------------------------------ 1쪽 요약
    H.append("<div class='page'>")
    H.append("<h1>로블록스 숏츠 키워드 분석 리포트</h1>")
    H.append("<div class='sub'>유튜브 쇼츠·틱톡용 · 데이터 기준 RoWatcher 2026-06-10 스냅샷, 조사 노트 2026-10-15</div>")
    H.append("<h2 style='margin-top:4pt'>한 장 요약</h2>")
    H.append(f"""<p>인기 로블록스 게임 {len(games)}개의 장르, 동시 접속자, 누적 방문수를 비교하고, 조사 노트로 사실을 확인할 수 있는 게임 중에서 숏츠 3편을 만들 게임 3개를 골랐다. 게임마다 한국어·영어 키워드 후보와 검색 의도, 숏츠 앵글을 정리했다.</p>""")
    H.append("""<div class='ban'><b>가장 큰 한계</b> 검색량, 조회수, 해시태그 사용량 데이터는 구하지 못했다. 이 리포트의 수요는 '지금 동시에 접속한 사람 수와 누적 방문수'로 본 대리 지표이고 검색 수요가 아니다. 키워드는 모두 후보이며 검증된 값이 아니다.</div>""")
    H.append("<h3>선정한 3개</h3><div class='grid3'>")
    why = {
        "Brookhaven RP": "동접·누적 방문수 모두 16개 중 1위(동접 CSV 기준). 역할놀이 묶음 대표이고 노트에 집, 탈것, 직업 등 쓸 수 있는 사실이 많다.",
        "Adopt Me!": "조사 노트가 있는 게임 중 수집·육성 묶음 1위. 펫 합성 규칙처럼 한 컷으로 보여 줄 수 있는 '방법'형 주제가 있다.",
        "99 Nights in the Forest": "생존·공포 묶음의 유일한 게임. 낮에 모으고 밤에 버티는 구조가 명확해서 정보형 숏츠로 풀기 쉽다.",
    }
    for i, n in enumerate(picks, 1):
        g = by[n]
        H.append(f"<div class='card'><div class='rk'>{i}순위 · {esc(g['genre_ko'])} ({esc(g['genre'])})</div><div class='gn'>{esc(n)}</div>"
                 f"<div class='big'>{g['score']}</div><div class='rk'>수요 점수(0~100) · 동접 {fmt_ccu(g['ccu'])} · 누적 방문 {int(round(g['visits']*10))}억</div>"
                 f"<p style='margin-top:4pt'>{esc(why[n])}</p></div>")
    H.append("</div>")
    H.append("<h3>고른 방법</h3><ol style='padding-left:15pt'>")
    H.append(f"<li>조사 노트가 있어 게임 내용을 사실대로 쓸 수 있는 {n_noted}개(Brookhaven RP, Adopt Me!, Steal a Brainrot, 99 Nights in the Forest)만 제작 후보로 둔다. 노트가 없는 게임은 점수가 높아도 대본을 쓸 수 없다. 예를 들어 +1 Speed Keyboard Escape(점수 {by['+1 Speed Keyboard Escape (Candy & Chocolate)']['score']})는 16개 중 동접 3위인데 노트가 없어 뺐다.</li>")
    H.append("<li>수요 점수(동접 60%, 누적 방문수 40%, 로그 눈금)가 높은 순으로 본다.</li>")
    H.append(f"<li>같은 장르 묶음에서는 1개만 고른다. 그래서 점수 {by['Steal a Brainrot']['score']}인 Steal a Brainrot은 같은 묶음의 Adopt Me!에 밀리고, 점수 {by['99 Nights in the Forest']['score']}인 99 Nights in the Forest가 들어갔다. 두 게임은 1.5점 차이라서 이 점수 식으로는 우열을 가를 수 없다. 묶음 규칙이 결정한 선택이고, Steal a Brainrot이 1순위 예비다.</li></ol>")
    H.append("<h3>이 리포트에서 얻은 것</h3><ul>")
    H.append(f"<li>장르 묶음 중 동접 합계는 수집·육성·시뮬레이터가 가장 크지만 게임 수가 7개라서 게임당 평균은 역할놀이·사회추리가 훨씬 높다(2쪽 차트).</li>")
    H.append(f"<li>숫자가 비어 있는 게임이 많다. 동접이 없는 게임 {n_noccu}개, 누적 방문수가 없는 게임 {n_novis}개라서 두 값을 모두 비교할 수 있는 게임은 {n_both}개뿐이다.</li>")
    H.append("<li>점수 가중치를 바꾸면 3위와 4위 순서가 바뀐다(6쪽). 선정은 가중치에 민감한 부분이 있다.</li></ul>")
    H.append("</div>")

    # ------------------------------------------------ 2쪽 범위와 한계 + 묶음 차트
    H.append("<div class='page'><h2 style='margin-top:0'>데이터 범위와 한계</h2>")
    H.append("<table class='t'><tr><th style='width:20%'>자료</th><th>내용</th><th style='width:38%'>한계</th></tr>")
    H.append(f"<tr><td>roblox_games.csv</td><td>RoWatcher 2026-06-10 스냅샷, 게임 {len(games)}개의 장르, 동시 접속자(대략), 누적 방문수(십억). Grow a Garden의 누적 방문수는 ExitLag 글 값.</td><td>동시 접속자는 한 시점의 근삿값이다. 동접 없음 {n_noccu}개, 누적 방문수 없음 {n_novis}개.</td></tr>")
    H.append("<tr><td>game_notes.md</td><td>게임 4개(Brookhaven RP, Adopt Me!, Steal a Brainrot, 99 Nights in the Forest)의 출처 있는 조사 노트(2026-10-15 정리). 출처는 RoWatcher, BlueStacks, Wikipedia, PlayNews, ExitLag 글.</td><td>나머지 12개 게임은 내용 조사가 없다. 출처마다 수치 시점이 다르다.</td></tr>")
    H.append("<tr><td>없는 데이터</td><td>검색량, 유튜브·틱톡 조회수, 해시태그 사용량, 한국어 공식 명칭과 별칭.</td><td>접근 가능한 신뢰 출처를 찾지 못했다. 이 값들은 지어내지 않았다. 한국어 키워드는 영문 게임명에 일반 수식어를 붙인 후보다.</td></tr></table>")
    H.append("<h3>출처와 시점에 따른 수치 차이</h3><ul>")
    H.append("<li>같은 게임도 출처와 시점에 따라 값이 다르다. Brookhaven RP 누적 방문수는 CSV(2026-06-10 스냅샷) 834억, 노트(RoWatcher 글) 804억 이상으로 시점 차이다. Adopt Me!는 CSV 43.8B, 노트(위키백과, 2025년 11월 기준) 408억 이상이다.</li>")
    H.append("<li>Steal a Brainrot 노트에는 2025년 10월에 동시 접속 2,540만 명을 넘었다는 가이드 기준 보도가 있다. CSV의 2026-06-10 값은 151,000이다. 이 차이는 설명하지 못했다. 점수는 CSV 값만으로 계산했다.</li></ul>")
    H.append("<h3>수요 점수가 뜻하는 것과 아닌 것</h3><ul>")
    H.append("<li>동시 접속자(60%)와 누적 방문수(40%)를 각각 로그 눈금으로 0~100에 맞춰 섞은 값이다. 동접은 1만~50만, 방문수는 약 32억~900억을 0~100으로 잡았다. 이 범위와 60:40 가중치는 임의로 정했다.</li>")
    H.append("<li>한쪽 값만 있으면 있는 값만 쓴다. 그래서 Grow a Garden(72.2)은 누적 방문수만으로 계산한 값이라 다른 게임과 같은 기준이 아니다.</li>")
    H.append("<li>플레이 인구가 많다고 그 게임의 팁 영상을 검색하는 사람이 많다는 보장은 없다. 점수는 검색량을 구하기 전에 쓰는 임시 순서표다.</li></ul>")
    H.append(f"<h2>장르 묶음별 수요 비교</h2>{img('chart_clusters.png')}")
    top = clusters[0]
    rp = next(c for c in clusters if c["family"] == "social_rp")
    H.append(f"<p class='note'>막대는 묶음 안 게임의 동접 합계다. {top['label']}가 합계 {top['ccu_total']/1000:,.0f}K로 가장 크지만 게임 {top['n']}개의 합이고, 동접 수치가 없는 1개(Grow a Garden)는 빠져 있다. 게임당 평균(마름모)은 {rp['label']}이 {rp['ccu_total']/rp['n']/1000:,.0f}K로 가장 높다. 합계는 묶음에 든 게임 수에 좌우된다.</p>")
    H.append("</div>")

    # ------------------------------------------------ 3쪽 수요 표 + 산점도
    H.append("<div class='page'><h2 style='margin-top:0'>게임별 수요 표</h2>")
    H.append("<table class='t g16'><tr><th class='n'>순위</th><th>게임</th><th>장르</th><th>묶음</th><th class='n'>동시 접속자</th><th class='n'>누적 방문(십억)</th><th class='n'>점수</th><th>노트</th></tr>")
    for g in games:
        cls = "sel" if g["game"] in picks else ""
        mark = " ★" if g["game"] in picks else ""
        star = "*" if (not g["ccu"] or not g["visits"]) else ""
        H.append(f"<tr class='{cls}'><td class='n'>{g['rank']}</td><td><b>{esc(g['game'].split(' (')[0])}</b>{mark}</td><td>{esc(g['genre_ko'])}</td>"
                 f"<td>{esc(FAMILY_KO[g['family']])}</td><td class='n'>{fmt_ccu(g['ccu'])}</td><td class='n'>{fmt_v(g['visits'])}</td>"
                 f"<td class='n'>{g['score']}{star}</td><td>{'있음' if g['has_notes'] else '<span class=dim>없음</span>'}</td></tr>")
    H.append("</table><p class='note'>★ 선정한 3개. *는 동접 또는 누적 방문수가 없어 한쪽 값만으로 계산한 점수라 다른 행과 같은 기준이 아니다. 출처: RoWatcher 2026-06-10 스냅샷(Grow a Garden 누적 방문수는 ExitLag). 게임 이름 +1 Speed Keyboard Escape (Candy &amp; Chocolate)는 줄여 적었다.</p>")
    H.append(f"<h3>동접과 누적 방문수</h3>{img('chart_scatter.png','sc')}")
    H.append("<p class='note'>두 축 모두 로그 눈금이다. 오른쪽 위에 있을수록 지금 접속자도 많고 누적 방문도 많다. 빨간 점이 선정한 3개다. Steal a Brainrot(파랑)은 누적 방문수에 비해 동접이 낮은 쪽이다.</p></div>")

    # ------------------------------------------------ 4~5쪽 키워드
    H.append("<div class='page'><h2 style='margin-top:0'>게임별 키워드 후보</h2>")
    H.append("<div class='ban'><b>모두 후보입니다.</b> 검색량으로 검증한 값이 아니다. 한국어 후보는 영문 게임명에 일반 수식어를 붙였고(공식 한국어 명칭을 찾지 못함), 조사 노트가 있는 게임은 노트에 있는 내용만 앵글로 삼았다. 의도 분류는 키워드 리서치 기준의 4가지(정보형, 비교·탐색형, 거래형, 내비형)에 숏츠용 '오락형'을 더했고, 실제 검색 결과로 검증한 분류가 아니다.</div>")
    H.append("<h3>조사 노트가 있는 4개 게임 (내용 기반 후보 23개)</h3>")
    H.append("<table class='k'><tr><th style='width:24%'>한국어 후보</th><th style='width:24%'>영어 후보</th><th style='width:11%'>의도</th><th>숏츠 앵글</th><th style='width:17%'>노트 근거</th></tr>")
    gi = 0
    for g in ["Brookhaven RP", "Adopt Me!", "99 Nights in the Forest", "Steal a Brainrot"]:
        tag = "★ 선정" if g in picks else "예비"
        H.append(f"<tr><td colspan='5' style='background:#f3f4f6;font-weight:700'>{esc(g)} <span class='pill'>{tag}</span></td></tr>")
        for k in [x for x in kws if x["game"] == g]:
            H.append(f"<tr><td>{esc(k['keyword_ko'])}</td><td>{esc(k['keyword_en'])}</td><td>{esc(k['intent_ko'])}</td><td>{esc(k['shorts_angle'])}</td><td class='mute'>{esc(k['notes_basis'])}</td></tr>")
    H.append("</table></div>")

    H.append("<div class='page'><h2 style='margin-top:0'>노트가 없는 12개 게임 (템플릿 후보)</h2>")
    H.append("<p class='small'>내용 조사가 없어서 게임 내용을 가리키지 않는 3개 템플릿만 적용했다. 의도는 모두 같다: <b>초보 공략</b>(정보형, 앵글: 초보가 막히는 구간 하나 해결), <b>업데이트</b>(내비형, 앵글: 신규 업데이트 요약), <b>버그 모음</b>(오락형, 앵글: 웃긴 장면 모음). 이 후보로 대본을 쓰려면 먼저 해당 게임을 조사해야 한다.</p>")
    H.append("<table class='k'><tr><th style='width:30%'>게임 (장르 묶음)</th><th>한국어 후보</th><th>영어 후보</th></tr>")
    for g in games:
        if g["has_notes"]:
            continue
        ks = [x for x in kws if x["game"] == g["game"]]
        H.append(f"<tr><td><b>{esc(g['game'])}</b><br><span class='mute tiny'>{esc(FAMILY_KO[g['family']])}</span></td>"
                 f"<td>{'<br>'.join(esc(k['keyword_ko']) for k in ks)}</td><td>{'<br>'.join(esc(k['keyword_en']) for k in ks)}</td></tr>")
    H.append("</table>")
    cnt = Counter((k["intent_ko"]) for k in kws)
    H.append(f"<h3>후보 {len(kws)}개의 의도 분포</h3><p class='small'>" + " · ".join(f"{k} {v}개" for k, v in cnt.most_common()) + ". 비교·탐색형과 거래형은 노트에서 '클래스 4가지', '솔로 vs 멀티', '게임패스 275~799 로벅스' 같은 내용이 있는 경우에만 붙였다.</p>")
    H.append("<h3>선정 3개의 주제 묶음 (피벗 → 묶음 → 숏츠 소재)</h3><div class='tree'>")
    tree = {
        "Brookhaven RP": [("시작·구성", "시작 방법, 집 종류, 직업 보수"), ("구매", "무료 탈것, 게임패스 가격"), ("운영", "업데이트")],
        "Adopt Me!": [("펫 키우기", "알 종류, 희귀도, 네온, 메가 네온"), ("거래", "교환 사기, 거래 면허"), ("구매", "로벅스 펫")],
        "99 Nights in the Forest": [("하루 루틴", "공략, 모닥불 연료"), ("선택", "클래스, 솔로 vs 멀티"), ("전투·구조", "적 종류, 실종된 아이")],
    }
    for g, cl in tree.items():
        H.append(f"<p style='margin:2pt 0'><b>{esc(g)}</b> → " + " / ".join(f"<b style='color:#374151'>{a}</b>({b})" for a, b in cl) + "</p>")
    H.append("</div></div>")

    # ------------------------------------------------ 6쪽 선정 근거, 우선순위, 다음 단계
    H.append("<div class='page'><h2 style='margin-top:0'>선정 근거와 제작 우선순위</h2>")
    H.append("<table class='t'><tr><th>순서</th><th>게임</th><th class='n'>점수</th><th>근거</th><th>먼저 겨냥할 키워드 후보</th></tr>")
    prim = {
        "Brookhaven RP": ("Brookhaven RP 직업 보수 / brookhaven rp jobs pay", "동접 1위. 직업 아이콘 80개 이상인데 보수가 없다는 사실이 첫 문장 훅으로 쓰기 좋다."),
        "Adopt Me!": ("Adopt Me 네온 펫 만들기 / adopt me how to make neon pets", "노트 있는 게임 중 점수 2위. 합성 규칙이 '방법' 질문 형태라 Shorts 제목 검색과 맞는다."),
        "99 Nights in the Forest": ("99 Nights 모닥불 연료 / 99 nights in the forest campfire fuel", "생존·공포 묶음 대표. 낮·밤 루틴과 연료 질문이 한 편 안에 답까지 들어간다."),
    }
    for i, n in enumerate(picks, 1):
        H.append(f"<tr class='sel'><td class='n'>{i}</td><td><b>{esc(n)}</b></td><td class='n'>{by[n]['score']}</td><td>{esc(prim[n][1])}</td><td>{esc(prim[n][0])}</td></tr>")
    H.append(f"<tr><td class='n'>예비</td><td><b>Steal a Brainrot</b></td><td class='n'>{by['Steal a Brainrot']['score']}</td><td>점수는 99 Nights와 1.5점 차. 같은 묶음의 Adopt Me!에 밀렸다. 기지 방어, 리버스 등 쓸 사실이 많아 다음 후보 1순위.</td><td>Steal a Brainrot 기지 방어 / steal a brainrot base defense</td></tr></table>")
    H.append("<p class='small'>제작 순서는 점수 순서(편 1 Brookhaven RP, 편 2 Adopt Me!, 편 3 99 Nights in the Forest)를 따랐다. 이 순서가 조회수를 보장하지는 않는다.</p>")
    H.append("<h3>가중치를 바꾸면 순서가 어떻게 되는가</h3><table class='t'><tr><th>가중치</th><th>노트 있는 4개 게임의 점수 순서</th><th>묶음 규칙으로 뽑은 3개</th></tr>")
    for lab, v in sens["weightings"].items():
        pk = ", ".join(v["picks_with_cluster_rule"]) if v["picks_with_cluster_rule"] else "해당 없음(순서만 비교)"
        H.append(f"<tr><td>{esc(lab)}</td><td>{esc(' > '.join(v['order']))}</td><td>{esc(pk)}</td></tr>")
    H.append("</table><p class='note'>동접만 보면 99 Nights가 Steal a Brainrot보다 앞서고, 누적 방문수만 보면 Steal a Brainrot이 Adopt Me!보다도 앞선다. 3개 선정에서 1순위 Brookhaven RP는 어느 가중치에서도 바뀌지 않는다.</p>")
    H.append("<h3>키워드 리서치 기준의 우선순위 식을 못 쓴 이유</h3><p class='small'>기준 식은 (검색량 × 예상 클릭률 × 사업 가치) ÷ (난이도 + 1)이다. 검색량과 난이도 값이 없어서 계산하지 못했고, 사업 가치도 이 채널에는 정의되지 않는다. 그래서 개별 키워드의 순위는 매기지 않고 게임 단위 순서만 냈다.</p>")
    H.append("<h2>다음 단계</h2><ol style='padding-left:15pt'>")
    for t in [
        "<b>검색량 확인</b> 위 후보를 Google 키워드 플래너, 네이버 검색광고 키워드 도구, YouTube 검색창 자동완성에 넣어 월 검색량과 연관어를 확인한다. 상대 추이는 Google 트렌드와 네이버 데이터랩, 틱톡은 TikTok Creative Center의 해시태그·키워드 지표를 본다(가능 여부와 범위는 계정·지역에 따라 다르다).",
        "<b>후보 정리</b> 검색량이 확인되면 이 리포트의 의도 분류와 앵글을 다시 맞춰 보고, 검색량 없는 후보를 정리한다. 우선순위 식도 그때 계산할 수 있다.",
        "<b>수치 갱신</b> 동접과 누적 방문수는 RoWatcher에서 다시 받는다. 스냅샷 시점에 따라 순위가 바뀐다.",
        "<b>조사 노트 확대</b> 노트가 없는 게임(예: 점수 87.5인 +1 Speed Keyboard Escape)을 조사해서 제작 후보를 넓힌다.",
        "<b>한국어 명칭 조사</b> 한국 커뮤니티에서 쓰는 게임 이름과 별칭을 찾아 키워드에 반영한다. 지금은 찾지 못했다.",
        "<b>3편 업로드 후 측정</b> 편마다 3초 이탈, 완주율, 저장, 공유, 댓글을 기록하고, 같은 내용에 훅만 바꾼 영상으로 비교한다. 이 값이 생기면 수요 점수와의 관계를 확인한다.",
    ]:
        H.append(f"<li>{t}</li>")
    H.append("</ol></div></body></html>")

    out = OUT / "keyword_analysis.pdf"
    render_pdf("".join(H), str(out))
    print("OK", out)


if __name__ == "__main__":
    main()
