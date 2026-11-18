import os, urllib.request, json, traceback, random

USER = "iamthearafatkhan"
FALLBACK = 419

def get_commits():
    try:
        token = os.environ["GITHUB_TOKEN"]
        q = '{ user(login: "' + USER + '") { contributionsCollection { totalCommitContributions } } }'
        body = json.dumps({"query": q}).encode()
        req = urllib.request.Request("https://api.github.com/graphql", data=body, headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
        data = json.loads(urllib.request.urlopen(req, timeout=20).read())
        return int(data["data"]["user"]["contributionsCollection"]["totalCommitContributions"])
    except Exception:
        traceback.print_exc()
        return FALLBACK

n = get_commits()
level = min(1.0, n / 800.0)
random.seed(3)

W, H = 900, 506
cx, cy = 450, 246
R   = 52 + 24 * level
BW  = 350 + 70 * level
BT  = 26 + 10 * level
cyb = cy + 0.30 * R + BT
BWd = BW * 0.94
foot = cyb - 2
hi  = foot - (cy - R - 8)
ho  = hi + 70 + 45 * level

f = lambda v: format(v, ".1f")

stars = ""
for i in range(140):
    sx = random.randint(0, W)
    sy = random.randint(0, H)
    sr = random.choice([0.4, 0.6, 0.9])
    so = format(random.uniform(0.12, 0.7), ".2f")
    stars += f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="#fff" opacity="{so}"/>'

def arch(x1, y1, x2, y2, h):
    return f"M {f(x1)} {f(y1)} C {f(x1 + (x2 - x1) * 0.25)} {f(y1 - h * 1.33)} {f(x2 - (x2 - x1) * 0.25)} {f(y2 - h * 1.33)} {f(x2)} {f(y2)}"

def arch_back(x1, y1, x2, y2, h):
    return f"C {f(x2 - (x2 - x1) * 0.25)} {f(y2 - h * 1.33)} {f(x1 + (x2 - x1) * 0.25)} {f(y1 - h * 1.33)} {f(x1)} {f(y1)}"

dome = arch(cx - BWd, foot, cx + BWd, foot, ho) + " " + arch_back(cx - BWd, foot, cx + BWd, foot, hi) + " Z"

dome_streaks = ""
k = 6 + int(level * 5)
for i in range(k):
    h = hi + (ho - hi) * (i + 1) / (k + 1)
    t = 14 + i * 9
    col = ["#ffffff", "#f5e7c4", "#d9b277", "#fffaf0"][i % 4]
    op = format(0.2 + 0.5 * i / k, ".2f")
    dash = format(26 + i * 10, ".0f") + " " + format(210 + i * 16, ".0f")
    dur = format(8 + i * 0.9, ".1f")
    p = arch(cx - BWd + t, foot + t * 0.12, cx + BWd - t, foot + t * 0.12, h)
    dome_streaks += f'<path d="{p}" fill="none" stroke="{col}" stroke-width="{f(1 + (i % 3) * 0.6)}" opacity="{op}" stroke-dasharray="{dash}" filter="url(#soft)"><animate attributeName="stroke-dashoffset" from="0" to="-520" dur="{dur}s" repeatCount="indefinite"/></path>'

band_streaks = ""
kb = 6 + int(level * 5)
for i in range(kb):
    y = cyb - BT + 5 + i * (BT * 1.8 / kb)
    dy = (y - cyb) / BT
    if abs(dy) >= 1:
        continue
    hw = BW * (1 - dy * dy) ** 0.5
    col = ["#fffdf5", "#e9d3a6", "#c9a06a", "#ffffff"][i % 4]
    op = format(0.25 + 0.45 * (i % 3) / 2, ".2f")
    dash = format(40 + i * 14, ".0f") + " " + format(260 + i * 22, ".0f")
    dur = format(6 + i * 1.0, ".1f")
    to = 900 if i % 2 == 0 else -900
    p = f"M {f(cx - hw)} {f(y)} Q {cx} {f(y + 3)} {f(cx + hw)} {f(y)}"
    band_streaks += f'<path d="{p}" fill="none" stroke="{col}" stroke-width="{f(1 + (i % 2))}" opacity="{op}" stroke-dasharray="{dash}"><animate attributeName="stroke-dashoffset" from="0" to="{to}" dur="{dur}s" repeatCount="indefinite"/></path>'

top_edge = f"M {f(cx - BW)} {f(cyb - BT)} A {f(BW)} {f(BT)} 0 0 1 {f(cx + BW)} {f(cyb - BT)}"
low_arc = f"M {f(cx - BW * 0.5)} {f(cy + R * 1.05)} Q {cx} {f(cy + R * 1.05 + 20)} {f(cx + BW * 0.5)} {f(cy + R * 1.05)}"

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
<linearGradient id="domeg" x1="0" y1="0" x2="0" y2="1">
<stop offset="0%" stop-color="#fffaf0"/><stop offset="55%" stop-color="#f0dcb0"/><stop offset="100%" stop-color="#b98a5a" stop-opacity="0.5"/>
</linearGradient>
<linearGradient id="bandg" x1="0" y1="0" x2="1" y2="0">
<stop offset="0%" stop-color="#6b4a30" stop-opacity="0.25"/><stop offset="28%" stop-color="#e8d2a8"/><stop offset="50%" stop-color="#fffdf6"/><stop offset="72%" stop-color="#e8d2a8"/><stop offset="100%" stop-color="#6b4a30" stop-opacity="0.25"/>
</linearGradient>
<radialGradient id="glow">
<stop offset="0%" stop-color="#ffe9c2" stop-opacity="{f(0.4 + 0.3 * level)}"/><stop offset="55%" stop-color="#c98a4a" stop-opacity="0.15"/><stop offset="100%" stop-color="#000" stop-opacity="0"/>
</radialGradient>
<filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="1.6"/></filter>
<filter id="big" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="10"/></filter>
</defs>
<rect width="{W}" height="{H}" fill="#04030a"/>
{stars}
<g transform="rotate(-6 {cx} {cy})">
<ellipse cx="{cx}" cy="{f(cy - R * 0.3)}" rx="{f(BW * 0.85)}" ry="{f(hi * 1.15)}" fill="url(#glow)"><animate attributeName="opacity" values="0.7;1;0.7" dur="6s" repeatCount="indefinite"/></ellipse>
<path d="{dome}" fill="url(#domeg)" opacity="0.9" filter="url(#soft)"/>
{dome_streaks}
<path d="{arch(cx - BWd, foot, cx + BWd, foot, ho)}" fill="none" stroke="#ffffff" stroke-width="1.5" opacity="0.85" filter="url(#soft)"/>
<path d="{low_arc}" fill="none" stroke="#d9b277" stroke-width="2" opacity="0.3" filter="url(#soft)"/>
<circle cx="{cx}" cy="{cy}" r="{f(R + 7)}" fill="none" stroke="#ffcf8a" stroke-width="1" opacity="0.35"/>
<circle cx="{cx}" cy="{cy}" r="{f(R + 2)}" fill="none" stroke="#ffe9c0" stroke-width="2" opacity="0.7"/>
<circle cx="{cx}" cy="{cy}" r="{f(R)}" fill="#000000"/>
<ellipse cx="{cx}" cy="{f(cyb)}" rx="{f(BW)}" ry="{f(BT)}" fill="url(#bandg)" opacity="0.95" filter="url(#soft)"/>
<ellipse cx="{f(cx - BW * 0.12)}" cy="{f(cyb - BT * 0.15)}" rx="95" ry="24" fill="#ffffff" opacity="0.35" filter="url(#big)"/>
{band_streaks}
<path d="{top_edge}" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.9" filter="url(#soft)"/>
</g>
<text x="{cx}" y="{H - 18}" fill="#e6d5ac" font-family="monospace" font-size="14" text-anchor="middle" letter-spacing="3">MASS: {n} COMMITS ABSORBED</text>
</svg>'''

os.makedirs("assets", exist_ok=True)
out = open("assets/blackhole.svg", "w")
out.write(svg)
out.close()
print("OK: " + str(n) + " commits, gravity " + str(int(level * 100)) + "%")
