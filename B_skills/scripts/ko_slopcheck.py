#!/usr/bin/env python3
"""한국어 숏츠 대본용 슬롭 검사기 (표준 라이브러리만 사용).

사용: python3 ko_slopcheck.py script.md [--json]
출력: 금지 패턴 적중 목록, 문장 길이 통계, 슬롭 점수(0~100, 낮을수록 좋음).
이 점수는 AI 탐지기가 아니라 '형식적으로 검사 가능한 부분'만 본다.
"""
import argparse
import json
import re
import statistics
import sys

BANNED = {
    "보고서투 시작": [r"에 대해 알아보", r"소개해 드리", r"알아보겠습니다", r"살펴보겠습니다"],
    "접속어 남발": [r"결론적으로", r"더불어", r"이처럼", r"이에 따라", r"뿐만 아니라"],
    "빈 형용사": [r"다양한", r"다채로운", r"독특한", r"특별한 경험", r"다양하게"],
    "번역투": [r"가능합니다", r"의미가 있", r"라는 점에서", r"에 있어서", r"를 통해"],
    "광고 멘트": [r"지금 바로", r"놓치지 마", r"꼭 한번", r"확인해 보세요", r"구독과 좋아요"],
    "호명": [r"여러분"],
    "반전 문형": [r"가 아니라 .{1,20}(입니다|이에요|예요)", r"이 아니라 .{1,20}(입니다|이에요|예요)"],
}
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")
SCREEN_TAG = re.compile(r"\[화면[^\]]*\]")


def sentences(text: str):
    text = SCREEN_TAG.sub("", text)
    text = re.sub(r"^#.*$", "", text, flags=re.M)
    parts = re.split(r"(?<=[.!?。])\s+|\n+", text)
    return [p.strip(" -*>\t") for p in parts if len(p.strip(" -*>\t")) > 1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    text = open(args.path, encoding="utf-8").read()

    hits = []
    for cat, pats in BANNED.items():
        for p in pats:
            for m in re.finditer(p, text):
                hits.append({"category": cat, "pattern": p, "match": m.group(0)})

    sents = sentences(text)
    lens = [len(s) for s in sents] or [0]
    long_sents = [s for s in sents if len(s) > 45]
    emojis = len(EMOJI.findall(text))
    bangs = text.count("!")
    has_screen = len(SCREEN_TAG.findall(text))

    score = 0
    score += min(60, len(hits) * 8)
    score += min(15, len(long_sents) * 5)
    score += min(10, max(0, emojis - 1) * 2)
    score += min(10, max(0, bangs - 2) * 2)
    if lens and statistics.pstdev(lens) < 5 and len(lens) > 5:
        score += 5  # 문장 길이가 너무 균일함

    report = {
        "slop_score": min(100, score),
        "banned_hits": hits,
        "sentences": len(sents),
        "avg_len": round(statistics.mean(lens), 1),
        "long_sentences_over_45": long_sents,
        "emoji_count": emojis,
        "exclamations": bangs,
        "screen_tags": has_screen,
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"슬롭 점수: {report['slop_score']} / 100 (낮을수록 좋음)")
        print(f"문장 {report['sentences']}개, 평균 {report['avg_len']}자, 45자 초과 {len(long_sents)}개")
        print(f"이모지 {emojis}개, 느낌표 {bangs}개, [화면] 태그 {has_screen}개")
        for h in hits:
            print(f"  - [{h['category']}] {h['match']}")
        if not hits:
            print("  금지 패턴 적중 없음")
    return 0


if __name__ == "__main__":
    sys.exit(main())
