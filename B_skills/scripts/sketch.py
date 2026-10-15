"""9:16 프레임 스케치(SVG) 생성기. 도형과 글자만 쓴다. 좌표계는 90 x 160."""
import html

FONT = "'Noto Sans CJK JP','Noto Sans CJK KR',sans-serif"


def _e(s):
    return html.escape(str(s), quote=True)


def rect(x, y, w, h, fill, rx=0, stroke=None, sw=0.6, dash=None, op=1):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    if dash:
        st += f' stroke-dasharray="{dash}"'
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" opacity="{op}"{st}/>'


def circ(cx, cy, r, fill, stroke=None, sw=0.6, op=1):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" opacity="{op}"{st}/>'


def ell(cx, cy, rx, ry, fill, stroke=None, sw=0.6):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}"{st}/>'


def poly(pts, fill, stroke=None, sw=0.6):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    p = " ".join(f"{a},{b}" for a, b in pts)
    return f'<polygon points="{p}" fill="{fill}"{st}/>'


def line(x1, y1, x2, y2, c="#111", w=0.8, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"{d}/>'


def text(x, y, s, size=5, fill="#111", anchor="middle", weight=700, stroke=None):
    st = ""
    if stroke:
        st = f' stroke="{stroke}" stroke-width="{size*0.22:.2f}" paint-order="stroke" stroke-linejoin="round"'
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}" font-family="{FONT}"{st}>{_e(s)}</text>')


def arrow(x1, y1, x2, y2, c="#111", w=1.0):
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    h = 3.2
    p1 = (x2 - h * math.cos(a - 0.5), y2 - h * math.sin(a - 0.5))
    p2 = (x2 - h * math.cos(a + 0.5), y2 - h * math.sin(a + 0.5))
    return line(x1, y1, x2, y2, c, w) + poly([(x2, y2), p1, p2], c)


def house(x, y, s, c="#f4a261"):
    return (rect(x, y + 0.42 * s, s, 0.58 * s, c, 0.5, "#7c4a1d", 0.5)
            + poly([(x - 0.08 * s, y + 0.44 * s), (x + 0.5 * s, y), (x + 1.08 * s, y + 0.44 * s)], "#c0392b", "#7c1d12", 0.5)
            + rect(x + 0.4 * s, y + 0.62 * s, 0.2 * s, 0.38 * s, "#fef3c7", 0.3))


def car(x, y, s, c="#ef4444"):
    return (rect(x, y + 0.35 * s, s, 0.38 * s, c, 1.2, "#111", 0.5)
            + rect(x + 0.2 * s, y + 0.1 * s, 0.6 * s, 0.32 * s, c, 1.4, "#111", 0.5)
            + rect(x + 0.3 * s, y + 0.16 * s, 0.4 * s, 0.18 * s, "#bae6fd", 0.6)
            + circ(x + 0.22 * s, y + 0.76 * s, 0.12 * s, "#111") + circ(x + 0.78 * s, y + 0.76 * s, 0.12 * s, "#111"))


def scooter(x, y, s, c="#10b981"):
    return (line(x + 0.1 * s, y + 0.8 * s, x + 0.9 * s, y + 0.8 * s, c, 1.6)
            + line(x + 0.85 * s, y + 0.8 * s, x + 0.75 * s, y + 0.1 * s, "#111", 0.9)
            + line(x + 0.65 * s, y + 0.1 * s, x + 0.9 * s, y + 0.1 * s, "#111", 0.9)
            + circ(x + 0.15 * s, y + 0.88 * s, 0.1 * s, "#111") + circ(x + 0.85 * s, y + 0.88 * s, 0.1 * s, "#111"))


def heli(x, y, s, c="#3b82f6"):
    return (ell(x + 0.45 * s, y + 0.55 * s, 0.4 * s, 0.25 * s, c, "#111", 0.5)
            + line(x + 0.8 * s, y + 0.5 * s, x + 1.1 * s, y + 0.4 * s, "#111", 0.9)
            + line(x + 0.05 * s, y + 0.18 * s, x + 0.95 * s, y + 0.18 * s, "#111", 0.8)
            + line(x + 0.5 * s, y + 0.18 * s, x + 0.5 * s, y + 0.32 * s, "#111", 0.8))


def egg(x, y, s, c="#fef3c7", crack=False):
    out = ell(x, y, 0.34 * s, 0.46 * s, c, "#92400e", 0.6)
    if crack:
        out += poly([(x - 0.3 * s, y - 0.05 * s), (x - 0.15 * s, y - 0.18 * s), (x, y - 0.02 * s), (x + 0.15 * s, y - 0.18 * s), (x + 0.3 * s, y - 0.05 * s)], "none", "#92400e", 0.7)
    return out


def pet(x, y, s, c="#f9a8d4", glow=None):
    out = ""
    if glow:
        out += circ(x, y, 0.62 * s, glow, op=0.35)
    out += (poly([(x - 0.34 * s, y - 0.28 * s), (x - 0.22 * s, y - 0.62 * s), (x - 0.06 * s, y - 0.34 * s)], c, "#111", 0.4)
            + poly([(x + 0.34 * s, y - 0.28 * s), (x + 0.22 * s, y - 0.62 * s), (x + 0.06 * s, y - 0.34 * s)], c, "#111", 0.4)
            + circ(x, y, 0.4 * s, c, "#111", 0.5)
            + circ(x - 0.14 * s, y - 0.04 * s, 0.05 * s, "#111") + circ(x + 0.14 * s, y - 0.04 * s, 0.05 * s, "#111"))
    return out


def tree(x, y, s, c="#15803d"):
    return (rect(x - 0.06 * s, y + 0.6 * s, 0.12 * s, 0.4 * s, "#78350f")
            + poly([(x - 0.4 * s, y + 0.7 * s), (x, y), (x + 0.4 * s, y + 0.7 * s)], c, "#052e16", 0.4))


def fire(x, y, s, big=1.0):
    k = s * big
    return (line(x - 0.4 * k, y + 0.5 * k, x + 0.4 * k, y + 0.3 * k, "#78350f", 1.4)
            + line(x - 0.4 * k, y + 0.3 * k, x + 0.4 * k, y + 0.5 * k, "#78350f", 1.4)
            + poly([(x - 0.28 * k, y + 0.38 * k), (x - 0.18 * k, y - 0.1 * k), (x, y + 0.12 * k), (x + 0.06 * k, y - 0.4 * k), (x + 0.3 * k, y + 0.38 * k)], "#f59e0b", "#b45309", 0.5)
            + poly([(x - 0.12 * k, y + 0.38 * k), (x, y + 0.08 * k), (x + 0.14 * k, y + 0.38 * k)], "#fde68a"))


def moon(x, y, r, c="#fef9c3", bg="#14213d"):
    return circ(x, y, r, c) + circ(x + r * 0.45, y - r * 0.2, r * 0.85, bg)


def sun(x, y, r):
    out = circ(x, y, r, "#fbbf24")
    import math
    for i in range(8):
        a = i * math.pi / 4
        out += line(x + 1.3 * r * math.cos(a), y + 1.3 * r * math.sin(a), x + 1.8 * r * math.cos(a), y + 1.8 * r * math.sin(a), "#fbbf24", 0.8)
    return out


def person(x, y, s, c="#60a5fa", down=False):
    if down:
        return (rect(x - 0.5 * s, y + 0.5 * s, s, 0.28 * s, c, 0.8, "#111", 0.4) + circ(x - 0.62 * s, y + 0.62 * s, 0.22 * s, "#fde68a", "#111", 0.4))
    return (circ(x, y, 0.22 * s, "#fde68a", "#111", 0.4) + rect(x - 0.22 * s, y + 0.24 * s, 0.44 * s, 0.5 * s, c, 0.8, "#111", 0.4)
            + line(x - 0.12 * s, y + 0.74 * s, x - 0.12 * s, y + 1.0 * s, "#111", 0.9) + line(x + 0.12 * s, y + 0.74 * s, x + 0.12 * s, y + 1.0 * s, "#111", 0.9))


def coin(x, y, r, cross=False):
    out = circ(x, y, r, "#fbbf24", "#92400e", 0.6) + text(x, y + r * 0.35, "$", r * 1.1, "#92400e")
    if cross:
        out += line(x - r * 1.2, y - r * 1.2, x + r * 1.2, y + r * 1.2, "#dc2626", 1.6) + line(x - r * 1.2, y + r * 1.2, x + r * 1.2, y - r * 1.2, "#dc2626", 1.6)
    return out


def grid(x, y, cols, rows, cell, gap, c="#fff", op=0.9):
    out = ""
    for r in range(rows):
        for k in range(cols):
            out += rect(x + k * (cell + gap), y + r * (cell + gap), cell, cell, c, 1.2, "#334155", 0.4, op=op)
            out += circ(x + k * (cell + gap) + cell / 2, y + r * (cell + gap) + cell * 0.38, cell * 0.17, "#64748b")
            out += rect(x + k * (cell + gap) + cell * 0.25, y + r * (cell + gap) + cell * 0.62, cell * 0.5, cell * 0.2, "#94a3b8", 0.8)
    return out


def star(x, y, r, c="#fde047"):
    import math
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    return poly(pts, c, "#a16207", 0.3)


def eyes(x, y):
    return circ(x - 1.6, y, 0.9, "#ef4444") + circ(x + 1.6, y, 0.9, "#ef4444")


def tag(x, y, w, h, s, fill="#111", fg="#fff", size=3.6):
    return rect(x, y, w, h, fill, 1.2) + text(x + w / 2, y + h * 0.68, s, size, fg)


def frame(bg, elements, cap, src="", accent="#2563eb", number=1):
    """bg: 배경 SVG 조각(문자열), elements: 문자열 리스트. cap: 자막 줄 리스트, src: 출처 줄."""
    out = [f'<svg viewBox="0 0 90 160" xmlns="http://www.w3.org/2000/svg" class="frame">']
    out.append('<defs><clipPath id="c%d"><rect width="90" height="160" rx="3"/></clipPath></defs>' % number)
    out.append(f'<g clip-path="url(#c{number})">')
    out.append(bg)
    out.extend(elements)
    # 플랫폼 UI 안전 영역 표시 (상단 12%, 하단 20%)
    out.append(rect(0, 0, 90, 19, "#000", op=0.10))
    out.append(rect(0, 128, 90, 32, "#000", op=0.10))
    out.append(line(0, 19, 90, 19, "#fff", 0.3, "1.5 1.5"))
    out.append(line(0, 128, 90, 128, "#fff", 0.3, "1.5 1.5"))
    # 자막
    n = len(cap)
    for i, l in enumerate(cap):
        y = 112 - (n - 1 - i) * 8.2
        out.append(text(45, y, l, 6.6, "#fff", "middle", 800, stroke="#000"))
    if src:
        out.append(text(45, 124.5, src, 3.1, "#e5e7eb", "middle", 500, stroke="#111"))
    out.append("</g>")
    out.append(f'<rect x="0.3" y="0.3" width="89.4" height="159.4" rx="3" fill="none" stroke="#9ca3af" stroke-width="0.6"/>')
    out.append("</svg>")
    return "".join(out)
