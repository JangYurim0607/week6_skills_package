import html, math
from common import *
e = html.escape

# 샷: (장면 설명, 내레이션, 자막, 자막 기준(없으면 ''), 효과음/BGM, 스케치(kind, [라벨]))
VIDEOS = [
 dict(
  game='Brookhaven RP', title='퀘스트도 화폐도 없는데 동접 1위? Brookhaven RP',
  angle='규칙이 없는 게임이 왜 인기인지, 집·탈것 구성과 약점까지 30초 정리', color='#e07a5f',
  hook='첫 3초: 도시 풍경 와이드에서 빠르게 줌인하며 "퀘스트도 화폐도 없는데, 동접 1위?"라는 질문을 던진다. 있어야 할 것이 없는데 1위라는 의문으로 붙잡는다. 동접 1위의 기준 시점은 자막 아래 작은 글씨로 함께 보여 준다.',
  end='끝 장면: 내가 잡은 집 앞에 차를 세우고 카메라가 천천히 빠진다. 댓글 유도(어떤 집을 잡을지)와 다음 편 예고(99 Nights in the Forest) 자막.',
  shots=[
   ('도시 와이드 샷에서 화면 중앙으로 빠르게 줌인.','퀘스트도 화폐도 없는데, 동접 1위?','퀘스트도 화폐도 없는데 동접 1위?','동접 1위: RoWatcher 2026-06-10 스냅샷 기준','짧은 "띠링" 효과음 + 빠른 비트 시작',('wide',['도시'])),
   ('타이틀 카드 "Brookhaven RP"와 함께 거리를 걷는 캐릭터 시점.','Brookhaven RP는 모던 도시에서 역할놀이를 하는 무료 게임이에요.','모던 도시 역할놀이 · 무료','','비트 유지, 타이틀 등장 시 가벼운 스윕',('single',['타이틀','캐릭터'])),
   ('로비에서 집을 고르고 입장한 뒤 차에 타서 출발하는 과정을 빠르게 편집.','집을 잡고 차를 타면, 1분쯤이면 장면에 합류할 수 있어요.','집 잡고, 차 타고, 합류 약 1분','시작 소요: 조사 노트 기준(2026-10-15 정리)','차 시동 효과음, 컷마다 짧은 틱 소리',('split',['집 선택','차 탑승'])),
   ('집 내부와 테마 장소(연구소, 유령의 집, 성 중 촬영된 곳), 탈것 여러 대를 연속 컷으로.','집과 테마 장소는 115개 이상, 탈것은 190개 이상이에요.','집·장소 115+ / 탈것 190+','수치: 조사 노트 기준(2026-10-15 정리)','컷마다 가벼운 팝 소리, 숫자 등장 시 강조음',('list',['집·장소 115+','탈것 190+','연구소·성'])),
   ('경찰, 의사 등 직업 아이콘 화면을 보여 주고 아이콘을 눌러 보는 장면.','직업 아이콘도 80개 넘게 있지만, 보수는 없는 장식이에요.','직업 아이콘 80+ (보수 없음)','수치: 조사 노트 기준(2026-10-15 정리)','"뿅" 효과음, 보수 없음 자막에서 낮은 톤',('list',['직업 아이콘','보수 없음'])),
   ('아무 일 없이 거리를 걷거나 차로 돌아다니는 느슨한 장면.','다만 목표가 없어서, 새로움이 지나면 밋밋하다는 평가도 있어요.','단점: 목표가 없다','','BGM 톤 살짝 낮춤',('single',['목표 없음'])),
   ('내 집 앞에 차를 세우고 카메라가 뒤로 빠지는 엔딩 컷.','어떤 집을 잡을지 댓글로 알려 주세요. 다음 편은 99 Nights입니다.','어떤 집? 댓글로! 다음 편: 99 Nights','','BGM 페이드아웃, 마지막에 "딩" 한 번',('text',['댓글 → 다음 편'])),
  ],
  guide=[
   '집을 잡고 차를 타 장면에 합류하기까지 걸리는 시간을 스톱워치로 실측한다(대사의 "1분쯤"은 조사 노트 기준이므로, 실측값이 크게 다르면 자막을 실측으로 고친다).',
   '촬영 당일 Brookhaven RP의 현재 동접이 로블록스 화면에 보이면 캡처해 두고, 자막에는 촬영일 기준이라고 적는다.',
   '연구소, 유령의 집, 성 중 실제로 입장해 볼 수 있는 장소를 확인해 녹화한다(대사는 노트의 예시만 언급).',
   '직업 아이콘을 눌렀을 때 화면에 실제로 어떻게 보이는지 녹화한다.',
   '채팅창과 다른 플레이어 닉네임이 화면에 나오지 않게 가리거나 구도를 조정한다.',
  ]),
 dict(
  game='99 Nights in the Forest', title='99번의 밤을 버티는 법 30초 정리 | 99 Nights in the Forest',
  angle='낮과 밤의 반복 구조와 모닥불 규칙을 한 흐름으로 정리', color='#7b5ea7',
  hook='첫 3초: 어두운 숲에서 눈을 뜨는 1인칭 컷, 화면에 "99번의 밤"을 큰 글자로 띄운다. 버텨야 하는 횟수가 이 게임의 규칙이라는 점을 바로 보여 준다.',
  end='끝 장면: 모닥불 앞에서 캐릭터들이 모여 앉은 컷. 댓글 유도(몇 번째 밤까지 버틸지)와 다음 편 예고(Steal a Brainrot) 자막.',
  shots=[
   ('어두운 숲에서 눈을 뜨는 1인칭 컷, 화면 중앙에 큰 글자.','눈 떠보니 숲, 99번의 밤을 버텨야 해요.','99번의 밤을 버텨라','','낮은 드론음, 시작과 함께 "쿵"',('night',['99번의 밤'])),
   ('낮 시간에 나무와 음식을 줍고 건물에 들어가는 탐험 컷.','낮에는 재료를 모으고 건물을 찾아 생존자를 구해요.','낮: 탐험 · 채집 · 구조','','밝은 BGM, 줍는 소리',('list',['나무','음식','건물·생존자'])),
   ('캠프에서 멀어지는 컷, 하늘이 어두워지기 시작하는 장면.','그런데 너무 멀리 가면 밤에 갇힐 수 있어요.','너무 멀리 가면 밤에 갇힘','','BGM이 점점 낮아지며 긴장음 추가',('split',['캠프','먼 곳'])),
   ('저녁에 캠프로 돌아와 방어를 보강하고 장비를 제작하는 컷.','저녁엔 캠프로 돌아와 방어를 보강하고 장비를 만들어요.','저녁: 캠프 복귀 · 방어 · 제작','','망치질·제작 효과음',('list',['방어 보강','장비 제작'])),
   ('모닥불 클로즈업, 나무를 넣어 불을 유지하는 장면.','모닥불은 밤마다 꺼지면 안 돼요. 연료가 나무라서 여분을 챙기라는 조언이 있어요.','모닥불은 꺼지면 안 됨 · 연료=나무','','불 타는 소리, 연료 넣을 때 "틱"',('single',['모닥불'])),
   ('밤에 적이 다가오는 장면, 가능하면 초반 밤과 후반 밤의 적을 나란히 보여 준다.','밤이 갈수록 적은 무리가 커지고 빨라지고, 특수 능력을 가진 적도 나와요.','밤이 갈수록 적이 강해진다','','심장 박동 같은 저음, 적 등장 시 스팅어',('night',['적 무리'])),
   ('여러 명이 역할을 나눠 채집, 건설, 전투, 정찰을 하는 멀티 플레이 컷.','멀티가 더 수월해요. 채집, 건설, 전투, 정찰로 역할을 나눠요.','멀티: 역할 분담','','BGM 밝아짐, 역할 바뀔 때마다 틱',('split',['채집·건설','전투·정찰'])),
   ('모닥불 앞에 모여 있는 엔딩 컷.','몇 번째 밤까지 버틸까요? 댓글로 알려 주세요. 다음 편은 Steal a Brainrot.','몇 번째 밤까지? 다음 편: Steal a Brainrot','','BGM 페이드아웃, 불 소리만 남김',('text',['댓글 → 다음 편'])),
  ],
  guide=[
   '밤 번호나 날짜 표시 UI가 화면에 어떻게 나오는지 확인하고, 훅 컷에 실제 UI가 보이게 녹화한다.',
   '초반 밤과 후반 밤의 적이 어떻게 다른지 직접 확인해 나란히 보여 줄 컷을 확보한다(구체적인 적 이름이나 수는 대사에 쓰지 않음).',
   '모닥불에 나무를 넣는 조작과 연료가 줄어드는 표시가 있는지 확인하고 녹화한다.',
   '클래스(채집가, 전사, 건축가, 정찰병) 선택 화면을 확인해 멀티 컷에 활용할 수 있는지 본다.',
   '호러 요소가 강한 장면은 연령 표기와 썸네일 수위를 점검한다.',
  ]),
 dict(
  game='Steal a Brainrot', title='훔치고 지키는 타이쿤, Steal a Brainrot 방어 요약',
  angle='사는 법에서 훔치기와 방어까지, 지키는 요령 중심으로 요약', color='#3d85c6',
  hook='첫 3초: 내 기지의 브레인롯을 다른 플레이어가 가져가는 순간을 보여 주며 "내 브레인롯, 남이 훔쳐 갈 수 있어요"라고 말한다. 잃는 장면을 먼저 보여 주는 훅.',
  end='끝 장면: 미끼를 앞에, 값진 것을 뒤에 둔 완성된 기지 배치 컷. 댓글 유도(뭘 미끼로 둘지)와 다음에 볼 게임을 고르는 질문 자막.',
  shots=[
   ('남의 플레이어가 내 기지 슬롯의 브레인롯을 가져가는 장면(촬영용 계정 둘 사용).','내 브레인롯, 남이 훔쳐 갈 수 있어요.','내 브레인롯, 훔쳐 갈 수 있다?','','"휙" 효과음 + 경고음 한 번',('split',['내 기지','도둑'])),
   ('기지 가운데 컨베이어 벨트로 브레인롯이 흘러나오는 컷.','기지 가운데 컨베이어 벨트로 브레인롯이 흘러나와요.','컨베이어에서 브레인롯 구매','','컨베이어 소리, 가벼운 비트',('list',['받침대','컨베이어'])),
   ('돈으로 브레인롯을 사서 받침대에 올리는 컷, 수익이 오르는 표시.','돈으로 사서 받침대에 올리면 초당 돈이 나와요.','받침대에 올리면 초당 수익','','구매 시 "코인" 소리',('single',['받침대 수익'])),
   ('다른 플레이어 기지 슬롯에 닿아 훔치기 게이지가 차오르는 컷, 방해받아 초기화되는 컷.','남의 슬롯에 계속 닿아 있으면 훔치기 게이지가 차고, 방해받으면 초기화돼요.','훔치기 게이지 vs 방해','','게이지 차는 소리, 초기화 때 "뚝"',('split',['게이지 상승','초기화'])),
   ('레이저 장벽, 슬롯 잠금, NPC 경비, 방어막을 하나씩 보여 주는 컷.','막는 방법은 레이저 장벽, 슬롯 잠금, NPC 경비, 임시 방어막이에요.','방어: 장벽 · 잠금 · 경비 · 방어막','','항목마다 "딸깍" 소리',('list',['레이저 장벽','슬롯 잠금','NPC 경비'])),
   ('뒤쪽 장벽과 잠금 뒤에 값진 것, 앞에 싼 것을 두는 배치를 보여 주는 컷.','가이드는 값진 건 뒤쪽 장벽과 잠금 뒤에, 싼 건 앞에 미끼로 두라고 해요.','값진 건 뒤, 싼 건 앞에 미끼','공략: playnews.gg 가이드(2026년 7월판) 기준','BGM 살짝 가벼워짐, 배치 때 "툭"',('split',['앞: 미끼','뒤: 값진 것'])),
   ('리버스(초기화) 화면과 보상(영구 수익 배수, 업그레이드 토큰)이 보이는 컷.','초기화하면 브레인롯은 사라지지만 영구 수익 배수를 받아요.','리버스: 영구 배수 보상','리버스 설명: 조사 노트 기준','초기화 시 "슈웅", 보상 팝업음',('single',['리버스 보상'])),
   ('방어를 마친 기지를 위에서 내려다보는 엔딩 컷.','뭘 미끼로 둘까요? 댓글로 알려 주시고, 다음에 볼 게임도 골라 주세요.','뭘 미끼로? 다음에 볼 게임도!','','BGM 페이드아웃, 마지막에 "딩"',('text',['댓글 → 다음 게임 투표'])),
  ],
  guide=[
   '훔치기 장면은 촬영용 계정 둘로 직접 연출해 녹화한다(다른 사람의 기지를 무단으로 쓰지 않는다).',
   '훔치기 게이지가 화면 어디에 어떻게 표시되는지, 방해받았을 때 초기화되는 모습을 확인하고 녹화한다.',
   '방어 4종(레이저 장벽, 슬롯 잠금, NPC 경비, 임시 방어막)이 실제 화면에서 어떻게 보이는지 하나씩 확인한다.',
   '리버스 화면에서 보상이 어떻게 표시되는지 확인한다. 희귀도별 수익 수치는 가이드 안에서도 어긋난다고 해서 대사에 쓰지 않았으므로, 필요하면 촬영 화면에서 직접 확인한 값만 자막에 쓰고 촬영일을 적는다.',
   '가이드의 "2026년 7월판" 공략이 현재 게임 버전과 같은지 방어 항목이 화면에 있는지로 확인한다.',
  ]),
]

CPS_LO, CPS_HI, CPS_MID = 5.5, 6.5, 6.0
def nchars(s): return len(''.join(s.split()))   # 공백 제외 글자 수(문장부호 포함)
def rnd_up(x): return math.ceil(x*2)/2

for v in VIDEOS:
    t = 0.0
    v['timing'] = []
    for i, sh in enumerate(v['shots']):
        c = nchars(sh[1])
        d = 3.0 if i == 0 else max(2.5, round(c/CPS_MID*2)/2)
        v['timing'].append((t, t+d, c)); t += d
    v['total_chars'] = sum(x[2] for x in v['timing'])
    v['length'] = t
    v['est_lo'] = v['total_chars']/CPS_HI; v['est_hi'] = v['total_chars']/CPS_LO
    print(v["game"], v["total_chars"], v["length"])
    assert 25 <= v['length'] <= 40, (v['game'], v['length'])
    assert 6 <= len(v['shots']) <= 8
    print(v['game'], 'chars', v['total_chars'], 'len', v['length'], f"{v['est_lo']:.1f}-{v['est_hi']:.1f}")

def fmt_t(a): return f'{a:g}'

def sketch(kind, labels, sub, color):
    L = labels
    inner = ''
    if kind == 'wide':
        inner = "<div class=bd style='left:10%;width:22%;height:30%'></div><div class=bd style='left:38%;width:24%;height:42%'></div><div class=bd style='left:68%;width:22%;height:24%'></div>"
        inner += f"<div class=lab style='top:18%'>{e(L[0])}</div><div class=zoom></div>"
    elif kind == 'single':
        inner = f"<div class=circ></div><div class=lab style='top:62%'>{e(' / '.join(L))}</div>"
    elif kind == 'split':
        inner = f"<div class=half style='left:6%'><span>{e(L[0])}</span></div><div class=half style='right:6%'><span>{e(L[1])}</span></div>"
    elif kind == 'list':
        inner = ''.join(f"<div class=bar style='top:{14+i*17}%'><span>{e(t)}</span></div>" for i, t in enumerate(L))
    elif kind == 'night':
        inner = f"<div class=moon></div><div class=tri style='left:12%'></div><div class=tri style='left:42%;border-bottom-width:30px'></div><div class=tri style='left:72%'></div><div class=lab style='top:46%;color:#fff'>{e(L[0])}</div>"
    elif kind == 'text':
        inner = f"<div class=bigtext>{e(L[0])}</div>"
    bg = '#1c2233' if kind == 'night' else '#dfe6ee'
    return f"<div class=frame style='background:{bg}'>{inner}<div class=subband>{e(sub)}</div></div>"

CSS = BASE_CSS + """
.page { padding: 13mm 13mm 12mm 13mm; page-break-after: always; height: 297mm; position: relative; overflow: hidden; }
.page:last-child { page-break-after: auto; }
h1 { font-size: 22pt; margin: 0 0 2mm; color:#16324f; line-height:1.25; }
h2 { font-size: 13pt; margin: 0 0 2mm; color:#fff; padding: 2mm 3mm; border-radius: 1.5mm; }
h3 { font-size: 10.5pt; margin: 3mm 0 1mm; color:#16324f; }
.sub { color:#5a6577; font-size:9pt; margin-bottom:3mm; }
table { border-collapse: collapse; width:100%; }
th { background:#16324f; color:#fff; padding:1.3mm 2mm; text-align:left; font-weight:500; font-size:8.3pt; }
td { vertical-align: top; padding: 1.8mm 2mm; border-bottom:1px solid #d6dde6; font-size:8.3pt; }
table.ov td { font-size:9pt; padding:2.5mm 2mm; }
table.shots td { font-size:8.2pt; }
.tm { font-weight:700; font-size:9pt; color:#16324f; white-space:nowrap; }
.lbl { color:#6b7585; font-size:7.3pt; font-weight:700; margin-top:1mm; display:block; }
.nar { font-size:8.8pt; font-weight:500; }
.basis { color:#6b7585; font-size:7.3pt; }
.frame { position:relative; width:24mm; height:42.67mm; border:0.4mm solid #16324f; border-radius:1.2mm; overflow:hidden; }
.frame .subband { position:absolute; left:0; right:0; bottom:4%; background:rgba(0,0,0,.72); color:#fff; font-size:5.4pt; line-height:1.25; text-align:center; padding:0.6mm 0.8mm; }
.frame .lab { position:absolute; left:0; right:0; text-align:center; font-size:6pt; font-weight:700; color:#16324f; }
.bd { position:absolute; bottom:30%; background:#9fb0c4; border:0.2mm solid #5d6f86; }
.zoom { position:absolute; left:20%; right:20%; top:28%; bottom:32%; border:0.3mm dashed #e07a5f; }
.circ { position:absolute; left:28%; width:44%; top:24%; height:25%; border-radius:50%; background:#9fb0c4; border:0.2mm solid #5d6f86; }
.half { position:absolute; top:22%; width:41%; height:42%; background:#9fb0c4; border:0.2mm solid #5d6f86; display:flex; align-items:center; justify-content:center; text-align:center; font-size:5.6pt; font-weight:700; color:#16324f; }
.bar { position:absolute; left:10%; right:10%; height:13%; background:#9fb0c4; border:0.2mm solid #5d6f86; display:flex; align-items:center; justify-content:center; font-size:5.6pt; font-weight:700; color:#16324f; }
.moon { position:absolute; right:14%; top:8%; width:5mm; height:5mm; border-radius:50%; background:#f3e9b5; }
.tri { position:absolute; bottom:28%; width:0; height:0; border-left:12px solid transparent; border-right:12px solid transparent; border-bottom:40px solid #2f5d44; }
.bigtext { position:absolute; left:6%; right:6%; top:30%; text-align:center; font-size:8pt; font-weight:700; color:#16324f; }
.box { background:#f2f6fb; border:1px solid #cfdbea; border-radius:2mm; padding:2.5mm 3.5mm; margin:2.5mm 0; font-size:8.8pt; }
.warn { background:#fff6e5; border-color:#f0cf8a; }
ul { padding-left: 5mm; margin: 1mm 0; font-size:8.8pt; } li { margin: 0.8mm 0; }
.foot { position:absolute; bottom:6mm; left:13mm; right:13mm; font-size:7.3pt; color:#8a93a3; display:flex; justify-content:space-between; }
"""

def foot(i, tot, label): return f"<div class=foot><span>{label}</span><span>{i} / {tot}</span></div>"
pages = []

# 표지
ov = ''
for i, v in enumerate(VIDEOS, 1):
    ov += f"<tr><td class=tm>{i}편</td><td><b>{e(v['title'])}</b><br><span class=basis>게임: {e(v['game'])}</span></td><td>약 {v['length']:g}초<br><span class=basis>내레이션 추정 {v['est_lo']:.0f}~{v['est_hi']:.0f}초</span></td><td>{e(v['angle'])}</td><td>유튜브 쇼츠, 틱톡</td></tr>"
pages.append(f"""<div class=page>
<h1>로블록스 게임 숏츠 스토리보드</h1>
<div class=sub>3편 | 세로 9:16 | 편당 25~40초 | 게임 정보 출처: 게임 조사 노트(2026-10-15 정리), RoWatcher 2026-06-10 스냅샷(CSV)</div>
<h3>개요</h3>
<table class=ov><tr><th style="width:8%">편</th><th style="width:30%">제목</th><th style="width:14%">길이</th><th>앵글</th><th style="width:13%">플랫폼</th></tr>{ov}</table>
<h3>제작 순서와 선정 이유</h3>
<p style="font-size:9pt">키워드 분석 리포트의 우선순위(Brookhaven RP, 99 Nights in the Forest, Steal a Brainrot) 순서입니다. 선정 근거는 동접과 누적 방문수를 수요의 대리 지표로 쓴 것이며, 검색량은 확인하지 못했습니다.</p>
<h3>읽는 법</h3>
<ul>
<li>각 편은 샷 6~8개로 구성되고, 샷마다 시간 구간, 9:16 프레임 스케치, 촬영할 장면, 내레이션, 화면 자막, 효과음/BGM을 적었습니다.</li>
<li>프레임 스케치는 도형과 글자로 그린 구도 메모이며 실제 게임 화면이 아닙니다.</li>
<li>자막이나 대사에 쓴 숫자는 기준 시점·출처를 자막 아래 "기준"으로 함께 적었습니다.</li>
<li>직접 촬영해서 확인해야 하는 내용은 대사에 쓰지 않고, 각 편 마지막의 "촬영 가이드"에 모았습니다.</li>
<li>길이 추정은 내레이션 글자 수(공백 제외, 문장부호 포함)를 초당 {CPS_LO}~{CPS_HI}자로 나눈 <b>추정값</b>이며, 편집 후 실제 길이는 달라질 수 있습니다. 각 샷의 시간 구간은 초당 {CPS_MID:g}자 기준의 계획값입니다.</li>
</ul>
<div class='box warn'>게임 내용은 조사 노트와 CSV에 있는 것만 사용했고, 검색량·조회수·해시태그 사용량은 데이터가 없어 쓰지 않았습니다.</div>
</div>""")

for vi, v in enumerate(VIDEOS, 1):
    def shot_rows(idx):
        out = ''
        for i in idx:
            sh = v['shots'][i]; a, b, c = v['timing'][i]
            basis = f"<div class=basis>기준: {e(sh[3])}</div>" if sh[3] else ''
            out += f"""<tr>
<td style="width:11%"><div class=tm>샷 {i+1}</div><div class=tm style="font-weight:500">{fmt_t(a)}~{fmt_t(b)}초</div></td>
<td style="width:14%">{sketch(sh[5][0], sh[5][1], sh[2], v['color'])}</td>
<td style="width:30%"><span class=lbl style="margin-top:0">촬영 장면</span>{e(sh[0])}<span class=lbl>효과음/BGM</span>{e(sh[4])}</td>
<td><span class=lbl style="margin-top:0">내레이션 ({c}자)</span><div class=nar>{e(sh[1])}</div><span class=lbl>화면 자막</span>{e(sh[2])}{basis}</td></tr>"""
        return out
    n = len(v['shots'])
    split = 5
    head = f"<h2 style='background:{v['color']}'>{vi}편. {e(v['title'])}</h2>"
    th = "<tr><th>샷/시간</th><th>화면(9:16)</th><th>장면·사운드</th><th>내레이션·자막</th></tr>"
    pages.append(f"<div class=page>{head}<table class=shots>{th}{shot_rows(range(0,split))}</table></div>")
    gl = ''.join(f'<li>{e(g)}</li>' for g in v['guide'])
    pages.append(f"""<div class=page>{head}<table class=shots>{th}{shot_rows(range(split,n))}</table>
<h3>첫 3초 훅</h3><div class=box>{e(v['hook'])}</div>
<h3>끝 장면 (CTA / 다음 편 예고)</h3><div class=box>{e(v['end'])}</div>
<h3>촬영 가이드 (직접 확인하고 녹화할 것, 대사에는 쓰지 않음)</h3><ul>{gl}</ul>
<h3>길이 추정</h3><div class=box>내레이션 합계 <b>{v['total_chars']}자</b>(공백 제외). 초당 {CPS_HI}자면 약 {v['est_lo']:.1f}초, 초당 {CPS_LO}자면 약 {v['est_hi']:.1f}초로 <b>추정</b>됩니다. 샷 구성(첫 샷 3초 고정, 나머지 초당 {CPS_MID:g}자 기준)의 계획 길이는 약 {v['length']:g}초입니다. 실제 녹음·편집 후 달라질 수 있습니다.</div></div>""")

tot = len(pages)
pages = [p.replace('</div>', f"</div>", 0) for p in pages]
final = ''
for i, p in enumerate(pages, 1):
    idx = p.rfind('</div>')
    final += p[:idx] + foot(i, tot, '로블록스 게임 숏츠 스토리보드') + p[idx:]
doc = f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body>{final}</body></html>"
html_to_pdf(doc, f'{OUT}/storyboard.pdf', 'storyboard')
