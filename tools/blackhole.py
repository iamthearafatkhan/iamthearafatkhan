import os, urllib.request, json, traceback, random

USER = "iamthearafatkhan"
FALLBACK = 418

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
random.seed(11)

W, H = 900, 506
cx, cy = 450, 252
R = 54 + 26 * level
dome_h = 140 + 70 * level
wing_rx = 400 + 70 * level
band_dy = 30 + 8 * level
band_tilt = 13 + 5 * level

stars = ""
for i in range(140):
    sx = random.randint(0, W)
    sy = random.randint(0, H)
    sr = random.choice([0.4, 0.6, 0.9])
    so = format(random.uniform(0.12, 0.7), ".2f")
    stars += f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="#fff" opacity="{so}"/>'

def dome_arch(h, foot_in, y_off):
    x1 = cx - wing_rx + foot_in
    x2 = cx + wing_rx - foot_in
    yb = cy + y_off
    return f"M {x1:.1f} {yb:.1f} C {cx - 150:.1f} {yb - h:.1f} {cx + 150:.1f} {yb - h:.1f} {x2:.1f} {yb:.1f}"

dome_fill = dome_arch(dome_h, 0, 10) + f" L {cx + wing_rx - 60:.1f} {cy + 26:.1f} " + dome_arch(dome_h * 0.55, 60, 26).replace("M", "C", 0)
dome_inner = dome_arch(dome_h * 0.52, 70, 26)
dome_shape = dome_arch(dome_h, 0, 10) + f" L {cx + wing_rx:.1f} {cy + 10:.1f} " + dome_inner.replace("M", "L", 1)

dome_streaks = ""
k = 7 + int(level * 6)
for i in range(k):
    h = dome_h * (0.5 + 0.5 * i / (k - 1))
    fin = 10 + i * 8
    col = ["#ffffff", "#f5e7c4", "#d9b277", "#fffaf0"][i % 4]
    op = format(0.18 + 0.5 * i / k, ".2f")
    dash = format(30 + i * 12, ".0f") + " " + format(240 + i * 18, ".0f")
    dur = format(9 + i * 0.8, ".1f")
    dome_streaks += f'<path d="{dome_arch(h, fin, 10)}" fill="none" stroke="{col}" stroke-width="{format(1 + (i % 3) * 0.7, ".1f")}" opacity="{op}" stroke-dasharray="{dash}" filter="url(#soft)"><animate attributeName="stroke-dashoffset" from="0" to="-540" dur="{dur}s" repeatCount="indefinite"/></path>'

band_top = f"M {cx - wing_rx:.1f} {cy + band_dy + band_tilt:.1f} L {cx + wing_rx:.1f} {cy + band_dy - band_tilt:.1f}"
band_bot = f"M {cx + wing_rx:.1f} {cy + band_dy + 40 - band_tilt:.1f} L {cx - wing_rx:.1f} {cy + band_dy + 40 + band_tilt:.1f}"
band_shape = band_top + " L " + f"{cx + wing_rx:.1f} {cy + band_dy + 40 - band_tilt:.1f} L {cx - wing_rx:.1f} {cy + band_dy + 40 + band_tilt:.1f} Z"

band_streaks = ""
for i in range(5 + int(level * 4)):
    yb = band_dy + 4 + i * 7
    col = ["#fffdf5", "#e9d3a6", "#c9a06a", "#ffffff"][i % 4]
    op = format(0.25 + 0.4 * (i % 3) / 3, ".2f")
    dash = format(50 + i * 15, ".0f") + " " + format(300 + i * 25, ".0f")
    dur = format(7 + i * 1.1, ".1f")
    band_streaks += f'<path d="M {cx - wing_rx:.1f} {cy + yb + band_tilt:.1f} L {cx + wing_rx:.1f} {cy + yb - band_tilt:.1f}" fill="none" stroke="{col}" stroke-width="{format(1 + (i % 2), ".1f")}" opacity="{op}" stroke-dasharray="{dash}"><animate attributeName="stroke-dashoffset" from="0" to="700" dur="{dur}s" repeatCount="indefinite"/></path>'

lower_arc = f"M {cx - 190:.1f} {cy + R + 14:.1f} C {cx - 70:.1f} {cy + R + 46:.1f} {cx + 70:.1f} {cy + R + 46:.1f} {cx + 190:.1f} {cy + R + 14:.1f}"

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
<linearGradient id="domeg" x1="0" y1="0" x2="0" y2="1">
<stop offset="0%" stop-color="#fffaf0"/><stop offset="45%" stop-color="#f3e0bb"/><stop offset="100%" stop-color="#caa06a" stop-opacity="0.55"/>
</linearGradient>
<linearGradient id="bandg" x1="0" y1="0" x2="1" y2="0">
<stop offset="0%" stop-color="#8a6a4a" stop-opacity="0.5"/><stop offset="30%" stop-color="#e8d2a8"/><stop offset="50%" stop-color="#fffdf6"/><stop offset="70%" stop-color="#e8d2a8"/><stop offset="100%" stop-color="#8a6a4a" stop-opacity="0.5"/>
</linearGradient>
<radialGradient id="glow">
<stop offset="0%" stop-color="#ffe9c2" stop-opacity="{format(0.35 + 0.3 * level, ".2f")}"/><stop offset="55%" stop-color="#c98a4a" stop-opacity="0.18"/><stop offset="100%" stop-color="#000" stop-opacity="0"/>
</radialGradient>
<filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="1.6"/></filter>
<filter id="big" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="14"/></filter>
</defs>
<rect width="{W}" height="{H}" fill="#04030a"/>
{stars}
<g transform="rotate(-7 {cx} {cy})">
<ellipse cx="{cx}" cy="{cy - 30}" rx="{wing_rx * 1.15:.0f}" ry="{dome_h * 0.95:.0f}" fill="url(#glow)"><animate attributeName="opacity" values="0.75;1;0.75" dur="6s" repeatCount="indefinite"/></ellipse>
<ellipse cx="{cx}" cy="{cy + 12}" rx="{wing_rx:.0f}" ry="{34 + 12 * level:.0f}" fill="url(#bandg)" opacity="0.5" filter="url(#big)"/>
<path d="{dome_shape}" fill="url(#domeg)" opacity="0.92"/>
{dome_streaks}
<path d="{dome_arch(dome_h, 0, 10)}" fill="none" stroke="#ffffff" stroke-width="1.6" opacity="0.85" filter="url(#soft)"/>
<path d="{lower_arc}" fill="none" stroke="#f0dcb0" stroke-width="2" opacity="0.4" filter="url(#soft)"/>
<circle cx="{cx}" cy="{cy}" r="{R + 10:.1f}" fill="none" stroke="#ffe9c0" stroke-width="1" opacity="0.5" stroke-dasharray="2 7"><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="40s" repeatCount="indefinite"/></circle>
<circle cx="{cx}" cy="{cy}" r="{R:.1f}" fill="#000000"/>
<path d="{band_shape}" fill="url(#bandg)"/>
<path d="{band_top}" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.9" filter="url(#soft)"/>
{band_streaks}
</g>
<text x="{cx}" y="{H - 18}" fill="#e6d5ac" font-family="monospace" font-size="14" text-anchor="middle" letter-spacing="3">MASS: {n} COMMITS ABSORBED</text>
</svg>'''

os.makedirs("assets", exist_ok=True)
f = open("assets/blackhole.svg", "w")
f.write(svg)
f.close()
print("OK: " + str(n) + " commits, gravity " + str(int(level * 100)) + "%")
