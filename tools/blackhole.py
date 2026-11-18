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
random.seed(7)

W, H = 900, 506
cx, cy = 450, 250
R = 50 + 22 * level
disk_rx = 380 + 80 * level
disk_ry = 28 + 8 * level
dome_h = 110 + 50 * level

f = lambda v: format(v, ".1f")

stars = ""
for i in range(130):
    sx = random.randint(0, W)
    sy = random.randint(0, H)
    sr = random.choice([0.3, 0.6, 0.9, 1.2])
    so = format(random.uniform(0.15, 0.75), ".2f")
    stars += f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="#fff" opacity="{so}"/>'

def dome_ribbon(h, foot_offset):
    x1 = cx - disk_rx + foot_offset
    x2 = cx + disk_rx - foot_offset
    yb = cy + 8
    return f"M {f(x1)} {f(yb)} C {f(cx - 120)} {f(yb - h * 1.4)} {f(cx + 120)} {f(yb - h * 1.4)} {f(x2)} {f(yb)}"

dome_ribbons = ""
num_ribbons = 12 + int(level * 8)
for i in range(num_ribbons):
    t = i / num_ribbons
    h = dome_h * (0.3 + 0.7 * (1 - t))
    foot = 20 + t * 60
    col = ["#ffffff", "#f5e7c4", "#e8d2a8", "#d9b277", "#c9a06a"][i % 5]
    op = format(0.15 + 0.6 * (1 - t), ".2f")
    dash = format(20 + i * 8, ".0f") + " " + format(180 + i * 12, ".0f")
    dur = format(7 + i * 0.6, ".1f")
    sw = format(0.8 + (1 - t) * 1.5, ".1f")
    p = dome_ribbon(h, foot)
    dome_ribbons += f'<path d="{p}" fill="none" stroke="{col}" stroke-width="{sw}" opacity="{op}" stroke-dasharray="{dash}" filter="url(#soft)"><animate attributeName="stroke-dashoffset" from="0" to="-480" dur="{dur}s" repeatCount="indefinite"/></path>'

disk_rings = ""
num_rings = 8 + int(level * 6)
for i in range(num_rings):
    t = i / num_rings
    rx = disk_rx * (0.5 + 0.5 * t)
    ry = disk_ry * (0.5 + 0.5 * t)
    col = ["#fffdf5", "#e8d2a8", "#c9a06a", "#ffffff"][i % 4]
    op = format(0.2 + 0.5 * (1 - abs(t - 0.5) * 2), ".2f")
    dash = format(30 + i * 10, ".0f") + " " + format(200 + i * 15, ".0f")
    dur = format(5 + i * 0.8, ".1f")
    to = 800 if i % 2 == 0 else -800
    disk_rings += f'<ellipse cx="{cx}" cy="{cy + 35}" rx="{f(rx)}" ry="{f(ry)}" fill="none" stroke="{col}" stroke-width="{f(0.8 + (1-t) * 1.2)}" opacity="{op}" stroke-dasharray="{dash}"><animate attributeName="stroke-dashoffset" from="0" to="{to}" dur="{dur}s" repeatCount="indefinite"/></ellipse>'

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
<radialGradient id="glow">
<stop offset="0%" stop-color="#ffe9c2" stop-opacity="{f(0.3 + 0.25 * level)}"/>
<stop offset="50%" stop-color="#c98a4a" stop-opacity="0.12"/>
<stop offset="100%" stop-color="#000" stop-opacity="0"/>
</radialGradient>
<linearGradient id="doppler" x1="0" y1="0" x2="1" y2="0">
<stop offset="0%" stop-color="#6b4a30" stop-opacity="0.4"/>
<stop offset="30%" stop-color="#e8d2a8"/>
<stop offset="50%" stop-color="#fffdf6"/>
<stop offset="70%" stop-color="#e8d2a8"/>
<stop offset="100%" stop-color="#6b4a30" stop-opacity="0.4"/>
</linearGradient>
<filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="1.2"/></filter>
<filter id="big" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="8"/></filter>
</defs>
<rect width="{W}" height="{H}" fill="#04030a"/>
{stars}
<g transform="rotate(-5 {cx} {cy})">
<ellipse cx="{cx}" cy="{f(cy - 20)}" rx="{f(disk_rx * 0.9)}" ry="{f(dome_h * 0.8)}" fill="url(#glow)"><animate attributeName="opacity" values="0.7;1;0.7" dur="6s" repeatCount="indefinite"/></ellipse>
{dome_ribbons}
<ellipse cx="{cx}" cy="{cy + 35}" rx="{f(disk_rx)}" ry="{f(disk_ry)}" fill="url(#doppler)" opacity="0.85" filter="url(#big)"/>
{disk_rings}
<circle cx="{cx}" cy="{cy}" r="{f(R + 6)}" fill="none" stroke="#ffe9c0" stroke-width="1.5" opacity="0.6"/>
<circle cx="{cx}" cy="{cy}" r="{f(R + 3)}" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.8"/>
<circle cx="{cx}" cy="{cy}" r="{f(R)}" fill="#000000"/>
<ellipse cx="{cx}" cy="{cy + 35}" rx="{f(disk_rx * 0.95)}" ry="{f(disk_ry * 0.9)}" fill="none" stroke="#ffffff" stroke-width="1.5" opacity="0.7" filter="url(#soft)"/>
</g>
<text x="{cx}" y="{H - 18}" fill="#e6d5ac" font-family="monospace" font-size="14" text-anchor="middle" letter-spacing="3">MASS: {n} COMMITS ABSORBED</text>
</svg>'''

os.makedirs("assets", exist_ok=True)
out = open("assets/blackhole.svg", "w")
out.write(svg)
out.close()
print("OK: " + str(n) + " commits, gravity " + str(int(level * 100)) + "%")
