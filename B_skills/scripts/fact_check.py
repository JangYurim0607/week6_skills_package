#!/usr/bin/env python3
"""대본의 숫자가 조사 노트나 CSV에 있는 값인지 대조한다(구현이 단순해서 숫자만 본다).

anti-ai-slop 스킬의 '검토자' 단계가 하는 '지어낸 구체값 찾기'를 스크립트로 옮긴 것이다.
사용: python3 fact_check.py script.md ../data/game_notes.md ../data/roblox_games.csv
"""
import re
import sys

KO_NUM = {"한": "1", "두": "2", "세": "3", "네": "4", "다섯": "5", "여섯": "6", "일곱": "7", "여덟": "8", "아홉": "9", "열": "10"}


def tokens(text):
    t = text.replace(",", "")
    return set(re.findall(r"\d+(?:\.\d+)?", t))


def main(script, *refs):
    allowed = set()
    for r in refs:
        allowed |= tokens(open(r, encoding="utf-8").read())
    text = open(script, encoding="utf-8").read()
    body = "\n".join(l for l in text.splitlines() if not l.startswith("#"))
    found = {}
    for line in body.splitlines():
        for n in tokens(line):
            found.setdefault(n, []).append(line.strip()[:50])
        # 한글 수사 + 단위 (네 마리, 다섯 단계)
        for m in re.finditer(r"(네|다섯)\s?(마리|단계)", line):
            found.setdefault(KO_NUM[m.group(1)], []).append(line.strip()[:50])
    bad = 0
    for n, ctx in sorted(found.items(), key=lambda kv: float(kv[0])):
        ok = n in allowed
        bad += (not ok)
        print(f"{'OK ' if ok else 'NO '} {n:>6}  x{len(ctx)}  {ctx[0]}")
    print(f"\n숫자 {len(found)}종, 노트/CSV에 없는 값 {bad}개")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
