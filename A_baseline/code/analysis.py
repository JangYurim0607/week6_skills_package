import csv, html
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from common import *

fm.fontManager.addfont('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
plt.rcParams['font.family'] = 'Noto Sans CJK JP'
plt.rcParams['axes.unicode_minus'] = False

rows = list(csv.DictReader(open(f'{DATA}/roblox_games.csv', encoding='utf-8')))
for r in rows:
    r['live'] = int(r['live_players_approx']) if r['live_players_approx'] else None
    r['life'] = float(r['lifetime_visits_b']) if r['lifetime_visits_b'] else None

# 장르 묶음(작성자 분류, CSV genre 값 기준)
GROUP = {
 'Roleplay':'역할놀이·소셜·꾸미기', 'Social deduction':'역할놀이·소셜·꾸미기',
 'Fashion competition':'역할놀이·소셜·꾸미기', 'Avatar sandbox':'역할놀이·소셜·꾸미기',
 'Pet-trading':'수집·시뮬레이터·타이쿤', 'Meme/Steal-game':'수집·시뮬레이터·타이쿤',
 'Fishing simulator':'수집·시뮬레이터·타이쿤', 'Idle/tycoon':'수집·시뮬레이터·타이쿤',
 'RNG clicker':'수집·시뮬레이터·타이쿤', 'Simulator':'수집·시뮬레이터·타이쿤',
 'Competitive shooter':'전투·액션·경쟁', 'Anime grind RPG':'전투·액션·경쟁',
 'Anime action-combat':'전투·액션·경쟁',
 'Survival/Horror':'서바이벌·호러·장애물', 'Fast-cycle obby':'서바이벌·호러·장애물',
}
GENRE_KO = {'Roleplay':'역할놀이','Pet-trading':'펫 거래','Fast-cycle obby':'빠른 순환 장애물(옵비)',
 'Survival/Horror':'서바이벌·호러','Competitive shooter':'경쟁 슈팅','Anime grind RPG':'애니 육성 RPG',
 'Social deduction':'사회적 추리','Anime action-combat':'애니 액션 전투','Meme/Steal-game':'밈·훔치기',
 'Fishing simulator':'낚시 시뮬레이터','Idle/tycoon':'방치·타이쿤','RNG clicker':'확률(RNG) 클리커',
 'Fashion competition':'패션 대결','Simulator':'시뮬레이터','Avatar sandbox':'아바타 샌드박스'}
for r in rows:
    r['group'] = GROUP[r['genre']]
GROUPS = ['역할놀이·소셜·꾸미기','수집·시뮬레이터·타이쿤','전투·액션·경쟁','서바이벌·호러·장애물']
COL = {'역할놀이·소셜·꾸미기':'#e07a5f','수집·시뮬레이터·타이쿤':'#3d85c6','전투·액션·경쟁':'#6a994e','서바이벌·호러·장애물':'#7b5ea7'}
SELECTED = ['Brookhaven RP','99 Nights in the Forest','Steal a Brainrot']

stats = {}
for g in GROUPS:
    rs = [r for r in rows if r['group']==g]
    lv = [r['live'] for r in rs if r['live'] is not None]
    stats[g] = dict(n=len(rs), n_live=len(lv), live_sum=sum(lv), live_avg=sum(lv)/len(lv),
                    top=max((r for r in rs if r['live']), key=lambda r:r['live'])['game'],
                    life_sum=sum(r['life'] for r in rs if r['life']), n_life=sum(1 for r in rs if r['life']))
total_live = sum(s['live_sum'] for s in stats.values())

# 차트 1: 장르 묶음별 동접 합계
fig, ax = plt.subplots(figsize=(7.2, 2.7), dpi=200)
vals = [stats[g]['live_sum']/1000 for g in GROUPS]
bars = ax.bar(range(4), vals, color=[COL[g] for g in GROUPS], width=0.6)
ax.set_xticks(range(4)); ax.set_xticklabels([g.replace('·','·\n',1) if len(g)>8 else g for g in GROUPS], fontsize=8.5)
for b, g in zip(bars, GROUPS):
    s = stats[g]
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+15, f"{s['live_sum']/1000:,.0f}천명\n({s['n_live']}개 게임, 평균 {s['live_avg']/1000:,.0f}천)", ha='center', fontsize=8)
ax.set_ylabel('천 명', fontsize=9)
ax.set_ylim(0, max(vals)*1.25)
ax.spines[['top','right']].set_visible(False)
ax.set_title('장르 묶음별 동접 합계 (RoWatcher 2026-06-10 스냅샷, 동접 값이 있는 15개 게임)', fontsize=9.5, loc='left')
plt.tight_layout(); plt.savefig(f'{WORK}/chart_group.png'); plt.close()

# 차트 2: 게임별 동접
rs = sorted([r for r in rows if r['live']], key=lambda r:r['live'])
fig, ax = plt.subplots(figsize=(7.2, 3.3), dpi=200)
for i, r in enumerate(rs):
    sel = r['game'] in SELECTED
    ax.barh(i, r['live']/1000, color=COL[r['group']], edgecolor='#111' if sel else 'none', linewidth=1.8 if sel else 0, height=0.7)
    ax.text(r['live']/1000+6, i, f"{r['live']/1000:,.0f}천" + ('  ◀ 선정' if sel else ''), va='center', fontsize=7.5, fontweight='bold' if sel else 'normal')
ax.set_yticks(range(len(rs))); ax.set_yticklabels([r['game'][:34] for r in rs], fontsize=7.5)
ax.set_xlabel('동접 (천 명)', fontsize=8.5); ax.set_xlim(0, 600)
ax.spines[['top','right']].set_visible(False)
handles = [plt.Rectangle((0,0),1,1,color=COL[g]) for g in GROUPS]
ax.legend(handles, GROUPS, fontsize=7.5, loc='lower right', frameon=False)
ax.set_title('게임별 동접 (검은 테두리 = 제작 선정 3개)', fontsize=9.5, loc='left')
plt.tight_layout(); plt.savefig(f'{WORK}/chart_game.png'); plt.close()

e = html.escape
def fmt_live(v): return f'{v:,}' if v else '값 없음'
def fmt_life(v): return f'{v:.1f}B (약 {v*10:,.0f}억)' if v else '값 없음'

# 표 4
tbl = ''
for r in rows:
    sel = r['game'] in SELECTED
    tbl += f"<tr class='{'sel' if sel else ''}'><td class=c>{r['rank']}</td><td>{e(r['game'])}{' ★' if sel else ''}</td><td>{e(r['genre'])}<br><span class=sm>{GENRE_KO[r['genre']]}</span></td><td>{e(r['group'])}</td><td class=r>{fmt_live(r['live'])}</td><td class=r>{fmt_life(r['life'])}</td></tr>"

# 키워드 후보 (노트가 있는 4개 게임만 상세, 앵글은 노트 내용에 근거)
KW = {
 'Brookhaven RP': [
  ('Brookhaven RP 집 꾸미기','Brookhaven RP house ideas','정보 탐색','집·테마 장소 115개 이상 중 꾸밀 곳 소개'),
  ('Brookhaven RP 차 종류','Brookhaven RP vehicles','정보 탐색','탈것 190개 이상, 무료 24개 이상 vs 유료 게임패스'),
  ('Brookhaven RP 시작 방법','how to start Brookhaven RP','입문','집 잡고 차 타고 합류까지 1분쯤'),
  ('Brookhaven RP 직업','Brookhaven RP jobs','정보 탐색','직업 아이콘 80개 이상이지만 보수 없는 장식'),
  ('Brookhaven RP 업데이트','Brookhaven RP update','최신 정보','금요일 주 단위 업데이트 (예: 2026-03-27 부활절 이벤트)'),
 ],
 'Adopt Me!': [
  ('Adopt Me 펫 알 부화','Adopt Me egg hatching','정보 탐색','알 종류마다 나오는 펫이 다름, 희귀도 5단계'),
  ('Adopt Me 네온 펫 만들기','Adopt Me how to make neon pet','방법','같은 종류 다 자란 펫 4마리 합치기'),
  ('Adopt Me 메가 네온','Adopt Me mega neon','방법','네온 4마리를 합치면 메가 네온'),
  ('Adopt Me 펫 교환 사기','Adopt Me trading scam','주의·예방','교환 사기로 2020년 거래 면허·사기 경고 추가'),
  ('Adopt Me 펫 희귀도','Adopt Me pet rarity','정보 탐색','희귀도 5단계와 성장 단계'),
 ],
 'Steal a Brainrot': [
  ('Steal a Brainrot 방어 방법','Steal a Brainrot base defense','방법·공략','레이저 장벽, 슬롯 잠금, NPC 경비, 방어막'),
  ('Steal a Brainrot 훔치는 법','how to steal in Steal a Brainrot','방법·공략','슬롯에 닿아 있으면 훔치기 게이지가 참'),
  ('Steal a Brainrot 리버스 시기','Steal a Brainrot rebirth when','방법·공략','가이드 기준 첫 리버스 약 8~10시간 뒤'),
  ('Steal a Brainrot 희귀도 순위','Steal a Brainrot rarity tier list','정보 탐색','커먼부터 브레인롯 갓까지 6단계'),
  ('Steal a Brainrot 게임패스','Steal a Brainrot game passes','구매 판단','배틀패스·빠른 훔치기·더블 머니·VIP 서버 가격'),
 ],
 '99 Nights in the Forest': [
  ('99 Nights in the Forest 공략','99 Nights in the Forest guide','방법·공략','낮에는 채집·탐험, 저녁에는 캠프 방어'),
  ('99 Nights in the Forest 모닥불','99 Nights campfire fuel','방법·공략','모닥불은 꺼지면 안 됨, 연료는 나무'),
  ('99 Nights in the Forest 클래스','99 Nights in the Forest classes','정보 탐색','채집가·전사·건축가·정찰병 4가지'),
  ('99 Nights in the Forest 멀티','99 Nights in the Forest multiplayer','방법·공략','역할 분담, 쓰러진 팀원 되살리기'),
  ('99 Nights in the Forest 실종된 아이','99 Nights in the Forest rescue kids','정보 탐색','숲에 흩어진 실종된 아이를 구하는 목표'),
 ],
}
kwhtml = ''
for g, items in KW.items():
    kwhtml += f"<h3>{e(g)}</h3><table class=kw><tr><th>한국어 후보</th><th>영어 후보</th><th>검색 의도</th><th>숏츠 앵글 (조사 노트 근거)</th></tr>"
    for k,en,it,ang in items:
        kwhtml += f"<tr><td>{e(k)}</td><td>{e(en)}</td><td>{it}</td><td>{e(ang)}</td></tr>"
    kwhtml += '</table>'
others = [r for r in rows if r['game'] not in KW]
oth = ''
for r in others:
    name = r['game'].split(' (')[0]
    oth += f"<tr><td>{e(r['game'])}</td><td>{e(name)} 공략 / {e(name)} 하는 법</td><td>{e(name)} guide / how to play {e(name)}</td><td>정보 탐색(일반 수식어 기반)</td></tr>"

def n(x): return f'{x:,}'
g1, g2, g3, g4 = (stats[g] for g in GROUPS)
sorted_g = sorted(GROUPS, key=lambda g:-stats[g]['live_sum'])
gtxt = ' > '.join(f"{g}({n(stats[g]['live_sum'])})" for g in sorted_g)
top2 = sorted(r['live'] for r in rows if r['live'])[-3:]

CSS = BASE_CSS + """
.page { padding: 16mm 16mm 14mm 16mm; page-break-after: always; height: 297mm; position: relative; overflow:hidden; }
.page:last-child { page-break-after: auto; }
h1 { font-size: 21pt; margin: 0 0 2mm; color:#16324f; line-height:1.25; }
h2 { font-size: 14pt; margin: 5mm 0 2mm; color:#16324f; border-left: 4px solid #3d85c6; padding-left: 2.5mm; }
h3 { font-size: 11pt; margin: 4mm 0 1.5mm; color:#16324f; }
p, li { margin: 1mm 0; }
ul { padding-left: 5mm; margin: 1mm 0; }
.sub { color:#5a6577; font-size:9.5pt; margin-bottom:4mm; }
.box { background:#f2f6fb; border:1px solid #cfdbea; border-radius:2mm; padding:3mm 4mm; margin:3mm 0; }
.warn { background:#fff6e5; border:1px solid #f0cf8a; }
table { border-collapse: collapse; width:100%; font-size:8.5pt; }
th { background:#16324f; color:#fff; padding:1.5mm 2mm; text-align:left; font-weight:500; }
td { border-bottom:1px solid #dde3ea; padding:1.3mm 2mm; vertical-align: top; }
tr.sel td { background:#fff3d6; font-weight:700; }
.c { text-align:center; } .r { text-align:right; white-space: nowrap; } .sm { color:#6b7585; font-size:7.5pt; }
table.gt td { font-size:8pt; padding:1mm 2mm; } table.gt td:nth-child(4), table.gt td:nth-child(3) { white-space:nowrap; }
table.ot td { font-size:7.6pt; padding:0.9mm 2mm; }
table.kw { font-size:8.3pt; margin-bottom:1mm; }
img { width:100%; display:block; margin: 2mm 0; }
.foot { position:absolute; bottom:8mm; left:16mm; right:16mm; font-size:7.5pt; color:#8a93a3; display:flex; justify-content:space-between; }
.tag { display:inline-block; background:#e8eef6; border-radius:1mm; padding:0 1.5mm; font-size:8pt; color:#16324f; }
.cols { display:flex; gap:4mm; } .cols > div { flex:1; }
.card { border:1px solid #cfdbea; border-radius:2mm; padding:3mm; }
.card h3 { margin-top:0; }
"""
def foot(i): return f"<div class=foot><span>로블록스 게임 숏츠 키워드 분석 리포트</span><span>{i} / 6</span></div>"

sel_info = {r['game']: r for r in rows}
bh, nn, sb = sel_info['Brookhaven RP'], sel_info['99 Nights in the Forest'], sel_info['Steal a Brainrot']

P1 = f"""<div class=page>
<h1>로블록스 게임 숏츠 키워드 분석 리포트</h1>
<div class=sub>유튜브 쇼츠·틱톡 제작용 | 분석 기준: RoWatcher 2026-06-10 스냅샷(CSV), 게임 조사 노트(2026-10-15 정리)</div>
<h2>한 장 요약</h2>
<div class=box>
<p><b>무엇을 분석했나.</b> 인기 게임 16개의 장르·동접·누적 방문수를 장르 묶음 4개로 나눠 비교하고, 조사 노트가 있는 4개 게임(Brookhaven RP, Adopt Me!, Steal a Brainrot, 99 Nights in the Forest)의 키워드 후보를 만들었습니다. 검색량 데이터는 없어서, 동접과 누적 방문수를 수요의 <b>대리 지표</b>로 썼습니다.</p>
<p><b>어떤 게임 3개를 골랐나.</b> <b>Brookhaven RP, 99 Nights in the Forest, Steal a Brainrot</b>입니다.</p>
</div>
<ul>
<li><b>Brookhaven RP</b>: 동접 {n(bh['live'])}명으로 16개 중 1위, 누적 방문 {bh['life']}B로 값이 있는 게임 중 최대(모두 RoWatcher 2026-06-10 기준). 규칙이 단순해 30초 안에 설명하기 쉽습니다.</li>
<li><b>99 Nights in the Forest</b>: 동접 {n(nn['live'])}명으로 4위. CSV에서 서바이벌/호러로 분류된 유일한 게임이고, 낮/밤 구조와 모닥불이 장면으로 나뉘어 숏츠 구성이 쉽습니다.</li>
<li><b>Steal a Brainrot</b>: 동접 {n(sb['live'])}명(9위)이지만 누적 방문 {sb['life']}B로 값이 있는 게임 중 2위(Brookhaven RP 다음). '훔치기'라는 갈등 구조가 있어 훅을 만들기 좋습니다.</li>
</ul>
<h2>핵심 관찰</h2>
<ul>
<li>동접 합계는 {gtxt} 순입니다(명, 동접 값이 있는 15개 게임 합).</li>
<li>동접 상위 3개(Brookhaven RP, Adopt Me!, +1 Speed Keyboard Escape)가 전체 합계의 {sum(top2)/total_live*100:.0f}%를 차지합니다. 상위 쏠림이 큰 시장입니다.</li>
<li>Adopt Me!는 동접 2위로 수치상 후보지만, 3개를 장르가 겹치지 않게 고르려고 이번에는 백업(4순위)으로 두었습니다. 이 선택은 분석자의 판단이며 검색량으로 검증된 것이 아닙니다.</li>
</ul>
<div class='box warn'><b>먼저 알아둘 점.</b> 이 리포트의 키워드는 모두 <b>검증되지 않은 후보</b>입니다. 검색량, 유튜브·틱톡 조회수, 해시태그 사용량 데이터가 없습니다. 아래 수치는 모두 시점·출처가 붙은 값입니다.</div>
{foot(1)}</div>"""

P2 = f"""<div class=page>
<h2 style="margin-top:0">데이터 범위와 한계</h2>
<table>
<tr><th style="width:26%">자료</th><th>내용</th></tr>
<tr><td>roblox_games.csv</td><td>인기 게임 16개의 장르, 동접(live_players_approx), 누적 방문수(단위 B=10억). 출처 RoWatcher 2026-06-10 스냅샷. 동접은 근사값입니다.</td></tr>
<tr><td>game_notes.md</td><td>게임 4개의 출처 있는 조사 노트(2026-10-15 정리). 게임 내용(규칙·기능)은 이 노트에 있는 것만 사용했습니다.</td></tr>
</table>
<h3>한계</h3>
<ul>
<li><b>검색량 없음.</b> 구글·네이버·유튜브·틱톡 검색량, 조회수, 해시태그 사용량은 신뢰할 출처가 없어 가져오지 못했습니다. 지어내지 않았고, 수요는 동접·방문수로만 대리했습니다.</li>
<li><b>값이 빠진 칸.</b> 누적 방문수는 16개 중 {sum(1 for r in rows if r['life'])}개만 있습니다. Grow a Garden은 동접 값이 없어 동접 비교와 합계에서 제외했습니다(누적 방문수 35.5B만 있음).</li>
<li><b>시점이 다른 수치.</b> CSV(2026-06-10)와 조사 노트의 수치는 시점·출처가 달라 같은 게임도 값이 다릅니다. 예를 들어 Adopt Me!의 누적 방문은 CSV 43.8B, 노트 40.8B 이상(2025년 11월 기준)입니다. 이 리포트의 표와 차트는 CSV 값만 씁니다.</li>
<li><b>Brookhaven RP 누적 방문수.</b> 노트(RoWatcher 글)는 804억, CSV(2026-06-10 스냅샷)는 834억(83.4B)입니다. 시점 차이이며 서로 모순되지 않습니다. 이 리포트의 표와 차트는 CSV 값만 씁니다.</li>
<li><b>장르 묶음은 분석자 분류.</b> CSV의 장르 값 15종을 4개 묶음으로 나눈 것이며 공식 분류가 아닙니다. 다르게 묶으면 합계 순위가 달라질 수 있습니다.</li>
<li><b>한국어 키워드.</b> 게임별 한국어 공식 명칭과 국내 별칭은 출처를 찾지 못했습니다. 한국어 키워드는 영문 게임명과 일반 수식어를 합친 후보입니다. 노트가 없는 12개 게임은 게임 내용 자료가 없어 앵글을 쓰지 않았습니다.</li>
</ul>
<h2>장르 묶음별 수요 비교</h2>
<img src="file://{WORK}/chart_group.png">
<table>
<tr><th>장르 묶음</th><th>게임 수</th><th>동접 합계</th><th>동접 평균</th><th>묶음 내 동접 1위</th></tr>
{''.join(f"<tr><td>{g}</td><td class=r>{stats[g]['n']} (동접 값 {stats[g]['n_live']})</td><td class=r>{n(stats[g]['live_sum'])}</td><td class=r>{n(round(stats[g]['live_avg']))}</td><td>{e(stats[g]['top'])}</td></tr>" for g in GROUPS)}
</table>
<p class=sm>동접 합계는 RoWatcher 2026-06-10 근사값의 합입니다. 수집·시뮬레이터·타이쿤 묶음은 게임 수가 많아 합계가 커지므로 평균과 같이 봐야 합니다. 평균으로 보면 서바이벌·호러·장애물 묶음이 가장 높습니다.</p>
{foot(2)}</div>"""

P3 = f"""<div class=page>
<h2 style="margin-top:0">게임별 수요 표</h2>
<table class=gt>
<tr><th style="width:6%">순위</th><th style="width:29%">게임</th><th style="width:19%">장르 (CSV)</th><th style="width:22%">장르 묶음</th><th style="width:10%">동접(명)</th><th style="width:14%">누적 방문수</th></tr>
{tbl}
</table>
<p class=sm>출처: RoWatcher 2026-06-10 스냅샷(CSV). Grow a Garden은 exitlag/rowatcher 기준 누적 방문수만 있습니다. ★ = 제작 선정 3개. 누적 방문수 B는 10억 단위입니다.</p>
<img src="file://{WORK}/chart_game.png" style="margin-top:1mm">
{foot(3)}</div>"""

P4 = f"""<div class=page>
<h2 style="margin-top:0">게임별 키워드 후보</h2>
<div class='box warn'><b>모두 검증되지 않은 후보입니다.</b> 검색량 데이터가 없고, 한국어 후보는 영문 게임명에 일반 수식어를 붙여 만들었습니다. 검색 의도는 분석자의 분류입니다.</div>
{kwhtml}
{foot(4)}</div>"""

P5 = f"""<div class=page>
<h2 style="margin-top:0">노트가 없는 12개 게임의 키워드 후보</h2>
<p class=sm>게임 내용 자료가 없어서 영문 게임명과 일반 수식어로만 만든 후보입니다. 숏츠 앵글은 비워 두지 않고 "보류"로 두었으며, 자료를 확보한 뒤 정합니다. 마찬가지로 검증되지 않은 후보입니다.</p>
<table class='kw ot'><tr><th style="width:22%">게임 (CSV 표기)</th><th>한국어 후보</th><th>영어 후보</th><th>검색 의도</th></tr>{oth}</table>
<h2>선택한 3개 게임의 선정 근거와 제작 우선순위</h2>
<table>
<tr><th style="width:6%">순위</th><th style="width:20%">게임</th><th>선정 근거 (수치는 RoWatcher 2026-06-10 기준)</th><th style="width:28%">주의</th></tr>
<tr><td class=c>1</td><td><b>Brookhaven RP</b><br><span class=sm>역할놀이·소셜</span></td><td>동접 {n(bh['live'])}명(1위), 누적 방문 {bh['life']}B. 퀘스트·레벨·게임 내 화폐가 없고 집/탈것/장소 구성이 숫자로 설명되어 훅과 정보형 숏츠 모두 가능. 시작이 쉬워 촬영 부담이 낮음.</td><td>목표가 없다는 약점, 채팅 기반 안전 우려가 노트에 있음. 안전 이슈는 앵글로 쓰지 않음.</td></tr>
<tr><td class=c>2</td><td><b>99 Nights in the Forest</b><br><span class=sm>서바이벌·호러</span></td><td>동접 {n(nn['live'])}명(4위), 누적 방문 {nn['life']}B. 낮(채집)과 밤(방어)의 반복 구조, 모닥불, 점점 강해지는 적 등 장면으로 나뉘는 규칙이 많아 30초 구성이 쉬움. 앞의 1순위와 장르가 겹치지 않음.</td><td>호러 요소가 있어 연령 표기·썸네일 수위는 촬영 때 확인 필요.</td></tr>
<tr><td class=c>3</td><td><b>Steal a Brainrot</b><br><span class=sm>밈·훔치기 (타이쿤형)</span></td><td>동접 {n(sb['live'])}명(9위)이지만 누적 방문 {sb['life']}B로 값이 있는 게임 중 2위. 훔치기 갈등과 방어 방법이 명확해 '지키는 법' 앵글을 만들기 좋음.</td><td>공략 가이드 안에서도 일부 수치가 서로 어긋난다고 노트에 적혀 있어 희귀도별 수치는 대본에서 제외.</td></tr>
<tr><td class=c>백업</td><td>Adopt Me!<br><span class=sm>펫 거래</span></td><td>동접 {n(sel_info['Adopt Me!']['live'])}명(2위), 누적 방문 {sel_info['Adopt Me!']['life']}B. 동접은 99 Nights·Steal a Brainrot보다 높지만(누적 방문은 Steal a Brainrot이 더 큼) Steal a Brainrot과 같은 수집 묶음이라 장르 분산을 위해 4순위로 둠.</td><td>동접 기준으로는 선정 가능했음. 다음 편 후보 1순위.</td></tr>
</table>
{foot(5)}</div>"""

P6 = f"""<div class=page>
<h2 style="margin-top:0">다음 단계</h2>
<div class=cols>
<div class=card><h3>1. 검색량 확인하기</h3>
<ul><li>구글 키워드 플래너, 네이버 검색광고 키워드 도구, 유튜브·구글 트렌드로 이 리포트의 키워드 후보(한국어/영어)를 하나씩 넣어 월간 검색량을 확인합니다.</li>
<li>한국어 후보는 영문명 + 수식어 조합이므로, 실제 검색창 자동완성에서 쓰는 표기(한글 음역 포함)를 따로 수집합니다.</li></ul></div>
<div class=card><h3>2. 반응 데이터 확인하기</h3>
<ul><li>유튜브 쇼츠·틱톡에서 후보 키워드를 직접 검색해 상위 영상의 조회수, 게시일, 길이를 표로 기록합니다.</li>
<li>해시태그 페이지의 영상 수·조회수도 같은 방식으로 직접 기록합니다.</li></ul></div>
</div>
<div class=cols style="margin-top:1mm">
<div class=card><h3>3. 게임 자료 보강</h3>
<ul><li>노트가 없는 12개 게임은 출처 있는 조사 노트를 만든 뒤 앵글을 정합니다.</li>
<li>Brookhaven RP 누적 방문수는 시점 차이(노트 804억 vs CSV 834억)이므로, 자막에 쓸 때 기준 시점을 함께 적습니다.</li></ul></div>
<div class=card><h3>4. 제작 후 측정</h3>
<ul><li>3편을 올린 뒤 1주 단위로 조회수, 시청 지속률, 댓글 수를 기록해 어떤 앵글이 반응이 좋은지 비교합니다.</li>
<li>반응이 좋은 앵글의 게임부터 Adopt Me! 등 후속 편을 만듭니다.</li></ul></div>
</div>
<h2>제작 일정 제안</h2>
<table>
<tr><th style="width:18%">단계</th><th>할 일</th><th style="width:22%">산출물</th></tr>
<tr><td>1</td><td>키워드 후보 검색량 확인(위 1, 2)</td><td>검증된 키워드 표</td></tr>
<tr><td>2</td><td>스토리보드의 촬영 가이드에 따라 플레이 영상 촬영·실측</td><td>원본 클립 3세트</td></tr>
<tr><td>3</td><td>편집, 자막에 수치 기준 표기, 업로드(유튜브 쇼츠·틱톡)</td><td>숏츠 3편</td></tr>
<tr><td>4</td><td>조회수·지속률 측정 후 후속 편 결정</td><td>결과 메모</td></tr>
</table>
<div class='box'><b>정리.</b> 이번 분석은 검색량 없이 동접·방문수로 수요를 짐작한 1차 선별입니다. 선정 순위는 가설이며, 위 1~2단계 확인 결과에 따라 바뀔 수 있습니다.</div>
{foot(6)}</div>"""

doc = f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body>{P1}{P2}{P3}{P4}{P5}{P6}</body></html>"
html_to_pdf(doc, f'{OUT}/keyword_analysis.pdf', 'keyword_analysis')
print('done', {g: stats[g] for g in GROUPS}, total_live, sum(top2)/total_live)
