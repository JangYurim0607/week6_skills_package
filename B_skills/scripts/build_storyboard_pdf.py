#!/usr/bin/env python3
"""storyboard.pdf 생성. 데이터는 storyboard_data.py.

부산물: output/artifacts/slop/script_final.md (내레이션과 자막만 모은 검사용 파일)
        output/artifacts/storyboard_numbers.json (길이 추정 수치)
"""
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import storyboard_data as D  # noqa: E402
from ko_syllables import count  # noqa: E402
from pdf_common import BASE_CSS, render_pdf  # noqa: E402
from sketch import frame  # noqa: E402

OUT = HERE.parent / "output"
ART = OUT / "artifacts"
PLACEHOLDER = re.compile(r"\[입력\]|TODO|\bOO\b|OO ")


def esc(s):
    import html
    return html.escape(s)


def build_timeline(shots):
    t = 0.0
    out = []
    for s in shots:
        c = count(s["narr"])
        dur = max(2.5, math.ceil((c / 6.0 + 0.4) * 2) / 2)
        out.append(dict(s, syl=c, t0=t, t1=t + dur, dur=dur))
        t += dur
    return out, t


def main():
    eps = []
    script_lines = []
    problems = []
    for ep in D.EPISODES:
        shots, total_t = build_timeline(ep["shots"]())
        syl = sum(s["syl"] for s in shots)
        lo, hi = syl / 6.5, syl / 5.5
        # 검증
        assert 6 <= len(shots) <= 8, "샷 수 6~8"
        if not (25 <= lo and hi <= 40):
            problems.append(f"편{ep['no']} 내레이션 추정 {lo:.1f}~{hi:.1f}초가 25~40초를 벗어남")
        if not (25 <= total_t <= 40):
            problems.append(f"편{ep['no']} 타임라인 {total_t}초")
        for i, s in enumerate(shots, 1):
            if len(s["cap"]) > 2:
                problems.append(f"편{ep['no']} 샷{i} 자막 2줄 초과")
            for l in s["cap"]:
                if len(l.replace(" ", "")) > 14:
                    problems.append(f"편{ep['no']} 샷{i} 자막 줄이 14자(공백 제외) 초과: {l}")
            for fld in ("narr", "scene", "comp", "cam", "audio") + ("src",):
                if PLACEHOLDER.search(s.get(fld, "")):
                    problems.append(f"편{ep['no']} 샷{i} 빈칸 흔적 {fld}")
        eps.append(dict(ep, shot_list=shots, total_t=total_t, syl=syl, lo=lo, hi=hi))
        script_lines.append(f"# 편 {ep['no']}. {ep['game']}\n\n### 내레이션")
        script_lines += [f"- {s['narr']}" for s in shots]
        script_lines.append("\n### 자막")
        script_lines += [f"- {' / '.join(s['cap'])}" for s in shots]
        script_lines.append("")
    (ART / "slop").mkdir(parents=True, exist_ok=True)
    (ART / "slop" / "script_final.md").write_text("\n".join(script_lines), encoding="utf-8")
    (ART / "storyboard_numbers.json").write_text(json.dumps(
        [{"ep": e["no"], "syllables": e["syl"], "est_sec_low": round(e["lo"], 1), "est_sec_high": round(e["hi"], 1),
          "timeline_sec": e["total_t"], "per_shot": [{"syl": s["syl"], "t0": s["t0"], "t1": s["t1"]} for s in e["shot_list"]]}
         for e in eps], ensure_ascii=False, indent=2), encoding="utf-8")
    if problems:
        print("문제:", *problems, sep="\n  ")
        sys.exit(1)

    css = BASE_CSS + """
    .cover h1 { font-size: 24pt; }
    .sub { color: var(--mute); font-size: 10pt; margin-bottom: 10pt; }
    .ovr td, .ovr th { font-size: 8.6pt; }
    .ephead { display:flex; align-items:baseline; gap:8pt; border-bottom: 2pt solid var(--c); padding-bottom: 4pt; margin-bottom: 6pt; }
    .ephead .no { background: var(--c); color:#fff; padding: 1pt 8pt; border-radius: 3pt; font-weight: 800; font-size: 11pt; }
    .ephead h1 { font-size: 15pt; margin:0; }
    .ephead .g { color: var(--mute); font-size: 9pt; margin-left:auto; }
    .meta { display:grid; grid-template-columns: 1fr 1fr; gap: 3pt 12pt; font-size: 8.4pt; margin-bottom: 5pt; }
    .hook { border:1pt solid var(--c); background: color-mix(in srgb, var(--c) 6%, white); border-radius:4pt; padding: 5pt 8pt; font-size: 8.4pt; margin-bottom: 6pt; }
    .hook b.l { color: var(--c); }
    .hook .row { display:grid; grid-template-columns: 38pt 1fr; gap: 4pt; margin: 1.4pt 0; }
    .shot { display:grid; grid-template-columns: 31mm 1fr; gap: 3.5mm; padding: 2.2mm 0; border-bottom: .6pt solid var(--rule); break-inside: avoid; }
    .shot svg.frame { width: 31mm; height: auto; display:block; }
    .sh { display:flex; gap:6pt; align-items:center; font-weight:800; font-size:9pt; margin-bottom:2pt; }
    .sh .tt { background:var(--c); color:#fff; border-radius:3pt; padding:0 6pt; }
    .sh .tm { font-variant-numeric: tabular-nums; }
    .sh .pp { margin-left:auto; font-weight:600; color: var(--mute); font-size:8pt; }
    .f { display:grid; grid-template-columns: 30pt 1fr; gap:4pt; font-size:8.1pt; line-height:1.45; margin: 1.6pt 0; }
    .f .k { color: var(--mute); font-weight:700; }
    .narr { font-size: 9.3pt; font-weight: 600; background: var(--soft); border-left: 2.5pt solid var(--c); padding: 2pt 6pt; border-radius: 0 3pt 3pt 0; }
    .cap { font-weight: 700; }
    .legend { display:flex; gap: 10pt; font-size: 7.8pt; color: var(--mute); }
    ol.guide { padding-left: 15pt; font-size: 8.6pt; } ol.guide li { margin: 2.5pt 0; }
    table.mini th, table.mini td { font-size: 8pt; padding: 2.4pt 4pt; }
    """

    h = [f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>로블록스 숏츠 스토리보드</title><style>{css}</style></head><body>"]

    # ---------- 표지 겸 개요
    h.append("<div class='page cover'>")
    h.append("<h1>로블록스 숏츠 스토리보드 3편</h1>")
    h.append("<div class='sub'>세로 9:16 · 편당 25~40초 · 한국어 내레이션 · 플레이 화면 녹화형 · 기준일 2026-10-15</div>")
    h.append("<h2 style='margin-top:6pt'>한눈에 보기</h2>")
    h.append("<table class='ovr'><tr><th>편</th><th>게임 / 제목</th><th>앵글</th><th>올릴 플랫폼</th><th class='n'>샷</th><th class='n'>길이</th></tr>")
    for e in eps:
        h.append(
            f"<tr><td><b style='color:{e['color']}'>편 {e['no']}</b></td>"
            f"<td><b>{esc(e['game'])}</b><br>{esc(e['title'])}</td>"
            f"<td>{esc(e['angle'])}</td><td>{esc(e['platform'])}</td>"
            f"<td class='n'>{len(e['shot_list'])}</td>"
            f"<td class='n'>내레이션 추정 {e['lo']:.0f}~{e['hi']:.0f}초<br><span class='mute'>설계 타임라인 {e['total_t']:.1f}초</span></td></tr>")
    h.append("</table>")
    h.append("<p class='note'>길이는 모두 추정이다. 내레이션 글자 수(음절 어림)를 초당 6.5자와 5.5자로 나눈 범위이고, 설계 타임라인은 샷마다 음절 수 ÷ 6.0 + 0.4초 간격을 0.5초 단위로 올린 값이다. 실제 길이는 녹음 후 확정한다.</p>")

    h.append("<h2>공통 화면 설정</h2>")
    h.append("""<table class='mini'>
    <tr><th style='width:22%'>항목</th><th>설정</th></tr>
    <tr><td>프레임</td><td>세로 9:16, 1080×1920, 30fps. PC 16:9로 녹화하면 가운데를 세로로 잘라 쓰므로 중요한 요소를 화면 중앙에 둔다.</td></tr>
    <tr><td>자막</td><td>굵은 고딕, 흰 글씨에 검정 외곽선, 한 화면에 최대 2줄, 한 줄 12자 안팎. 핵심 단어만 노란색(#FFD400). 내레이션과 같은 타이밍에 띄운다.</td></tr>
    <tr><td>출처 줄</td><td>숫자나 게임 규칙이 나오는 샷에만 하단 안전 영역 바로 위에 작은 회색 글씨로 출처와 조사 시점을 넣는다.</td></tr>
    <tr><td>안전 영역</td><td>스케치의 점선은 상단 12%와 하단 20%다. 플랫폼 UI가 덮을 수 있다고 가정한 일반 기준이며 플랫폼별 실측은 하지 않았다.</td></tr>
    <tr><td>카메라</td><td>게임 안 3인칭 시점이 기본이다. 컷 하나는 3~6초, 전환은 하드컷. 줌은 편집에서 준다.</td></tr>
    <tr><td>색</td><td>게임 원본 색을 유지하고 필터는 쓰지 않는다. 편마다 포인트 색만 다르다(편 1 파랑, 편 2 분홍, 편 3 주황).</td></tr>
    <tr><td>소리</td><td>플랫폼 음원 라이브러리의 BGM을 쓰고 내레이션 아래에서 볼륨을 낮춘다. 유행 음원은 올리기 직전에 상승 중인지 확인한다.</td></tr>
    </table>""")
    h.append("<h2>사실 규칙과 읽는 법</h2><ul class='small' style='font-size:8.8pt'>")
    h.append("<li>게임 내용은 조사 노트(2026-10-15 정리)와 RoWatcher 2026-06-10 스냅샷 CSV에 있는 것만 썼다. 숫자가 나오는 샷에는 출처와 시점을 자막 아래 출처 줄로 붙였다.</li>")
    h.append("<li>직접 촬영해야 알 수 있는 내용은 대사에 쓰지 않고 편마다 '촬영 가이드'에 적었다. 이 문서에는 채워야 할 빈칸이 없다.</li>")
    h.append("<li>검색량, 조회수, 해시태그 사용량 데이터는 없다. 이 문서의 플랫폼 선택은 일반 숏폼 기준을 따른 가설이고, 성과 예측이 아니다.</li>")
    h.append(f"<li>Instagram Reels는 제외했다. 숏폼 기준 자료에서 Reels는 15~30초를 권하는데 이 3편은 내레이션 추정 {min(x['lo'] for x in eps):.0f}~{max(x['hi'] for x in eps):.0f}초다.</li>")
    h.append("<li>샷마다 '촬영 장면 설명'은 영상 생성용 프롬프트 대신 직접 플레이 화면을 녹화할 때 구도, 카메라, 장면을 적은 것이다.</li></ul>")
    h.append("<div class='legend' style='margin-top:6pt'><span>샷 목적 표기: 훅 → 배경 → 전개 → 결과 → 마무리(CTA)</span></div>")
    h.append("</div>")

    # ---------- 편별
    for e in eps:
        c = e["color"]
        st = f"style='--c:{c}'"
        sl = e["shot_list"]
        h_ = e["hook"]

        def shot_html(i, s):
            svg = frame(s["bg"], s["el"], s["cap"], s.get("src", ""), c, number=e["no"] * 10 + i)
            capt = " / ".join(esc(x) for x in s["cap"])
            srcl = f"<br><span class='mute'>출처 줄: {esc(s['src'])}</span>" if s.get("src") else "<br><span class='mute'>출처 줄: 없음(숫자 없음)</span>"
            return f"""<div class='shot'>{svg}<div>
            <div class='sh'><span class='tt'>샷 {i}</span><span class='tm'>{s['t0']:.1f}~{s['t1']:.1f}초</span><span class='pp'>{esc(s['purpose'])}</span></div>
            <div class='f'><span class='k'>장면</span><span><b>구도</b> {esc(s['comp'])}<br><b>카메라</b> {esc(s['cam'])}<br><b>장면</b> {esc(s['scene'])}</span></div>
            <div class='f'><span class='k'>내레이션</span><span class='narr'>{esc(s['narr'])}</span></div>
            <div class='f'><span class='k'>자막</span><span><span class='cap'>{capt}</span>{srcl}</span></div>
            <div class='f'><span class='k'>소리</span><span>{esc(s['audio'])}</span></div>
            </div></div>"""

        def head():
            return (f"<div class='ephead' {st}><span class='no'>편 {e['no']}</span><h1>{esc(e['title'])}</h1><span class='g'>{esc(e['game'])}</span></div>")

        # 페이지 A
        h.append(f"<div class='page' {st}>{head()}")
        h.append(f"<div class='meta'><div><b>앵글</b> {esc(e['angle'])}</div><div><b>플랫폼</b> {esc(e['platform'])}<br><span class='mute'>{esc(e['platform_why'])}</span></div></div>")
        h.append(f"""<div class='hook'><b class='l'>첫 3초 훅</b>
        <div class='row'><b>낭독</b><span>{esc(h_['line'])} <span class='mute'>({esc(h_['formula'])})</span></span></div>
        <div class='row'><b>화면</b><span>{esc(h_['visual'])}</span></div>
        <div class='row'><b>자막</b><span>{esc(h_['text'])}</span></div>
        <div class='row'><b>이유</b><span>{esc(h_['why'])}</span></div>
        <div class='row'><b>답</b><span>{esc(h_['pay'])}</span></div>
        <div class='row'><b>탈락</b><span class='mute'>{esc(h_['runner'])}</span></div></div>""")
        for i in range(3):
            h.append(shot_html(i + 1, sl[i]))
        h.append("</div>")
        # 페이지 B
        h.append(f"<div class='page' {st}>{head()}")
        for i in range(3, len(sl)):
            h.append(shot_html(i + 1, sl[i]))
        h.append("</div>")
        # 페이지 C
        h.append(f"<div class='page' {st}>{head()}")
        h.append("<h3>끝 장면</h3>")
        h.append(f"<p>{esc(e['ending'])}</p><p class='note'>반복 재생 연결: {esc(e['loop'])}</p>")
        h.append("<h3>촬영 가이드: 직접 확인하고 녹화할 것 (대사에는 쓰지 않았다)</h3><ol class='guide'>")
        for g in e["shoot_guide"]:
            h.append(f"<li>{esc(g)}</li>")
        h.append("</ol>")
        h.append("<h3>내레이션 길이 추정 <span class='pill warn'>추정값</span></h3>")
        h.append("<table class='mini'><tr><th>샷</th><th class='n'>음절 수(어림)</th><th class='n'>6.0자/초 기준</th><th>샷 구간</th></tr>")
        for i, s in enumerate(sl, 1):
            h.append(f"<tr><td>샷 {i}</td><td class='n'>{s['syl']}</td><td class='n'>{s['syl']/6.0:.1f}초</td><td>{s['t0']:.1f}~{s['t1']:.1f}초</td></tr>")
        h.append(f"<tr><td><b>합계</b></td><td class='n'><b>{e['syl']}</b></td><td class='n'><b>{e['syl']/6.0:.1f}초</b></td><td>{e['total_t']:.1f}초(간격 포함)</td></tr></table>")
        h.append(f"<p class='note'>내레이션 {e['syl']}자 ÷ 6.5~5.5자/초 = {e['lo']:.1f}~{e['hi']:.1f}초(추정). 글자 수는 공백과 문장부호를 빼고 한글 음절을 1로, 숫자는 한자어로 읽는다고 보고(80은 팔십), 영문 이름은 외래어 발음으로 어림해서 센 값이다. 실제 낭독 속도와 편집에 따라 달라진다.</p>")
        h.append("<h3>사실 근거표</h3><table class='mini'><tr><th>영상에 쓴 사실</th><th>조사 노트 위치</th><th>출처(조사 시점 2026-10)</th></tr>")
        for f in e["facts"]:
            h.append(f"<tr><td>{esc(f[0])}</td><td>{esc(f[1])}</td><td>{esc(f[2])}</td></tr>")
        h.append("</table></div>")

    # ---------- 마지막: 후처리와 구성 이유
    h.append("<div class='page'><h1 style='font-size:17pt'>후처리 체크리스트와 구성 이유</h1>")
    h.append("<h2>후처리 체크리스트</h2><ul>")
    for t in [
        "편마다 촬영 가이드의 항목을 모두 녹화한다. 확인 결과가 대사와 다르면 대사를 고친다.",
        "내레이션을 녹음하거나 TTS로 만든다. 녹음한 뒤 실제 길이가 25~40초인지 확인한다.",
        "편집 앱에서 샷 순서와 시간을 맞추고 자막을 입힌다. 한 화면 2줄 이하, 한 줄 12자 안팎을 지킨다.",
        "숫자가 나오는 샷마다 출처 줄을 넣고 사실 근거표와 대조한다.",
        "업로드 직전에 모든 수치가 노트의 값과 같은지, 게임이 업데이트로 규칙이 바뀌지 않았는지 다시 확인한다.",
        "채팅, 닉네임, 아바타 이름을 가린다.",
        "1080×1920, 30fps, 세로 9:16으로 내보낸다. 제목에는 한국어 키워드와 영문 게임명을 함께 쓴다(키워드 후보는 검증 전이다).",
        "올리는 시간은 일반 숏폼 기준(점심 12~3시, 저녁 7~9시대)을 첫 가설로 두고 직접 비교한다. 한국 시청자 기준으로 검증된 값이 아니다.",
    ]:
        h.append(f"<li style='list-style:none;margin-left:-10pt'>☐ {esc(t)}</li>")
    h.append("</ul><h2>이 구성을 고른 이유</h2><ul>")
    for t in [
        "세 편 모두 첫 샷에서 화면, 낭독, 자막이 동시에 나온다. 숏폼 기준 자료의 3초 규칙(시각, 음성, 텍스트 훅을 첫 1초에 함께)을 따랐다.",
        "한 샷에 한 가지만 말한다. 샷이 3~7초라서 자막을 읽는 시간이 확보된다.",
        "훅이 던진 질문의 답을 영상 중반(편 1은 3번 샷, 편 2는 4번 샷, 편 3은 5번 샷)에 분명히 말한다.",
        "마지막 샷이 요청하는 행동은 하나다. 편 1과 편 2는 다음 편 예고, 편 3은 댓글 하나다. 마지막 컷이 첫 컷과 이어져 반복 재생을 노린다.",
        "게임의 약점(편 1의 목표 부재)도 출처가 있는 사실이라 넣었다. 광고처럼 보이지 않게 하려는 선택이다.",
        "성과(조회수, 완주율)는 측정하지 않았다. 이 구성이 잘 먹힌다는 증거는 아직 없다.",
    ]:
        h.append(f"<li>{esc(t)}</li>")
    h.append("</ul></div></body></html>")

    out = OUT / "storyboard.pdf"
    render_pdf("".join(h), str(out))
    print("OK", out)
    for e in eps:
        print(f"편{e['no']} 음절 {e['syl']} 추정 {e['lo']:.1f}~{e['hi']:.1f}초 타임라인 {e['total_t']}초")


if __name__ == "__main__":
    main()
