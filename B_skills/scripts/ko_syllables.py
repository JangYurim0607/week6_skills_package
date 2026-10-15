"""내레이션 길이 추정용 음절 수 계산기 (표준 라이브러리만).

규칙: 한글 음절 1자 = 1. 숫자는 한자어 수사로 읽는다고 보고(80=팔십) 음절 수를 센다. 라틴 문자 단어는
'모음 덩어리 수 + 끝이 자음이면 1'로 어림한다(한국어 외래어 발음 근사, 오차가 있다). 공백·문장부호는 세지 않는다.
따라서 결과는 어림값이고 실제 낭독 속도에 따라 달라진다.
"""
import re


def sino_syllables(n: int) -> int:
    if n == 0:
        return 1
    c = 0
    for div in (1000, 100, 10):
        d = (n // div) % 10
        if d:
            c += (1 if d > 1 else 0) + 1
    d = n % 10
    if d:
        c += 1
    return c


def latin_syllables(w: str) -> int:
    if w.isupper() and len(w) <= 3:
        return len(w)  # RP -> 알피
    groups = re.findall(r"[aeiouy]+", w.lower())
    n = max(1, len(groups))
    if w[-1].lower() not in "aeiouy":
        n += 1
    return n


def count(text: str) -> int:
    total = 0
    for tok in re.finditer(r"[가-힣]|\d+|[A-Za-z]+", text):
        s = tok.group(0)
        if re.match(r"[가-힣]", s):
            total += 1
        elif s.isdigit():
            total += sino_syllables(int(s))
        else:
            total += latin_syllables(s)
    return total


if __name__ == "__main__":
    import sys
    for line in sys.stdin:
        line = line.strip()
        if line:
            print(count(line), line)
