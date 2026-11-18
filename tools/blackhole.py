import os, urllib.request, json, traceback, random

USER = "iamthearafatkhan"
FALLBACK = 414

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

W = 900
H = 520
cx = 450
cy = 260
core_r = 30 + 24 * level
disk_rx = 150 + 170 * level
disk_ry = disk_rx * 0.27
sw = 4 + 10 * level
top_ry = disk_rx * 0.52
bot_ry = disk_rx * 0.33

f = lambda v: format(v, ".1f")

stars = ""
for i in range(150):
    sx = random.randint(0, W)
    sy = random.randint(0, H)
    sr = random.choice([0.4, 0.7, 1.0, 1.3])
    so = format(random.uniform(0.15, 0.85), ".2f")
    if i < 25:
        td = format(random.uniform(2.5, 6.0), ".1f")
        stars = stars + '<circle cx="' + str(sx) + '" cy="' + str(sy) + '" r="' + str(sr) + '" fill="#fff" opacity="' + so + '"><animate attributeName="opacity" values="' + so + ';0.1;' + so + '" dur="' + td + 's" repeatCount="indefinite"/></circle>'
    else:
        stars = stars + '<circle cx="' + str(sx) + '" cy="' + str(sy) + '" r="' + str(sr) + '" fill="#fff" opacity="' + so + '"/>'

disk_path = "M " + f(cx + disk_rx) + "," + f(cy) + " A " + f(disk_rx) + "," + f(disk_ry) + " 0 1,0 " + f(cx - disk_rx) + "," + f(cy) + " A " + f(disk_rx) + "," + f(disk_ry) + " 0 1,0 " + f(cx + disk_rx) + "," + f(cy)
top_halo = "M " + f(cx - disk_rx) + "," + f(cy) + " A " + f(disk_rx) + "," + f(top_ry) + " 0 0,1 " + f(cx + disk_rx) + "," + f(cy)
bot_halo = "M " + f(cx - disk_rx) + "," + f(cy) + " A " + f(disk_rx) + "," + f(bot_ry) + " 0 0,0 " + f(cx + disk_rx) + "," + f(cy)

disk_parts = ""
for i in range(5 + int(level * 7)):
    dur = format(6 + i * 0.6, ".1f")
    begin = format(i * 0.8, ".1f")
    disk_parts = disk_parts + '<circle r="' + f(1.5 + 2 * level) + '" fill="#fff">'
    disk_parts = disk_parts + '<animateMotion dur="' + dur + 's" begin="-' + begin + 's" repeatCount="indefinite" path="' + disk_path + '"/>'
    disk_parts = disk_parts + '<animate attributeName="opacity" values="1;0.2;1" dur="' + dur + 's" repeatCount="indefinite"/></circle>'

halo_parts = ""
for i in range(3):
    dur = format(7 + i * 1.3, ".1f")
    begin = format(i * 2.1, ".1f")
    halo_parts = halo_parts + '<circle r="1.8" fill="#ffd27f"><animateMotion dur="' + dur + 's" begin="-' + begin + 's" repeatCount="indefinite" path="' + top_halo + '"/></circle>'

svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + str(W) + ' ' + str(H) + '" width="' + str(W) + '" height="' + str(H) + '">'
svg = svg + '<defs>'
svg = svg + '<radialGradient id="corona"><stop offset="0%" stop-color="#ffffff" stop-opacity="' + f(0.25 + 0.35 * level) + '"/><stop offset="35%" stop-color="#ff6a00" stop-opacity="' + f(0.35 + 0.3 * level) + '"/><stop offset="70%" stop-color="#c40000" stop-opacity="0.25"/><stop offset="100%" stop-color="#000" stop-opacity="0"/></radialGradient>'
svg = svg + '<linearGradient id="doppler" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#5a0f00"/><stop offset="40%" stop-color="#ff6a00"/><stop offset="75%" stop-color="#ffc36b"/><stop offset="100%" stop-color="#ffffff"/></linearGradient>'
svg = svg + '<linearGradient id="halog" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#ff6a00"/><stop offset="50%" stop-color="#ffffff"/><stop offset="100%" stop-color="#ff6a00"/></linearGradient>'
svg = svg + '<filter id="b8" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="8"/></filter>'
svg = svg + '<filter id="b3" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="3"/></filter>'
svg = svg + '<filter id="b15" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="1.5"/></filter>'
svg = svg + '</defs>'
svg = svg + '<rect width="' + str(W) + '" height="' + str(H) + '" fill="#030308"/>'
svg = svg + stars
svg = svg + '<ellipse cx="' + str(cx) + '" cy="' + str(cy) + '" rx="' + f(disk_rx * 1.35) + '" ry="' + f(disk_ry * 3.2) + '" fill="url(#corona)"><animate attributeName="opacity" values="0.75;1;0.75" dur="5s" repeatCount="indefinite"/></ellipse>'
svg = svg + '<path d="' + bot_halo + '" fill="none" stroke="url(#halog)" stroke-width="' + f(sw * 0.5) + '" opacity="0.85" filter="url(#b15)"/>'
svg = svg + '<ellipse cx="' + str(cx) + '" cy="' + str(cy) + '" rx="' + f(disk_rx) + '" ry="' + f(disk_ry) + '" fill="none" stroke="url(#doppler)" stroke-width="' + f(sw * 2.4) + '" opacity="0.45" filter="url(#b8)"/>'
svg = svg + '<ellipse cx="' + str(cx) + '" cy="' + str(cy) + '" rx="' + f(disk_rx) + '" ry="' + f(disk_ry) + '" fill="none" stroke="url(#doppler)" stroke-width="' + f(sw) + '" filter="url(#b3)"/>'
svg = svg + '<ellipse cx="' + str(cx) + '" cy="' + str(cy) + '" rx="' + f(disk_rx * 0.93) + '" ry="' + f(disk_ry * 0.93) + '" fill="none" stroke="#fff3d6" stroke-width="' + f(sw * 0.4) + '" opacity="0.9"/>'
svg = svg + disk_parts
svg = svg + halo_parts
svg = svg + '<path d="' + top_halo + '" fill="none" stroke="url(#halog)" stroke-width="' + f(sw * 0.6) + '" filter="url(#b15)"><animate attributeName="opacity" values="0.7;1;0.7" dur="4s" repeatCount="indefinite"/></path>'
svg = svg + '<circle cx="' + str(cx) + '" cy="' + str(cy) + '" r="' + f(core_r + 9) + '" fill="none" stroke="#ffffff" stroke-width="1" opacity="0.25"/>'
svg = svg + '<circle cx="' + str(cx) + '" cy="' + str(cy) + '" r="' + f(core_r) + '" fill="#000"/>'
svg = svg + '<circle cx="' + str(cx) + '" cy="' + str(cy) + '" r="' + f(core_r + 2.5) + '" fill="none" stroke="#ffffff" stroke-width="2.5" filter="url(#b15)"/>'
svg = svg + '<circle cx="' + str(cx) + '" cy="' + str(cy) + '" r="' + f(core_r + 2.5) + '" fill="none" stroke="#fff" stroke-width="4" stroke-dasharray="70 400" opacity="0.9"><animateTransform attributeName="transform" type="rotate" from="0 ' + str(cx) + ' ' + str(cy) + '" to="360 ' + str(cx) + ' ' + str(cy) + '" dur="6s" repeatCount="indefinite"/></circle>'
svg = svg + '<text x="' + str(cx) + '" y="' + str(H - 24) + '" fill="#ffffff" font-family="monospace" font-size="15" text-anchor="middle" letter-spacing="3">MASS: ' + str(n) + ' COMMITS ABSORBED · GRAVITY ' + str(int(level * 100)) + '%</text>'
svg = svg + '</svg>'

os.makedirs("assets", exist_ok=True)
out = open("assets/blackhole.svg", "w")
out.write(svg)
out.close()
print("OK: " + str(n) + " commits, gravity " + str(int(level * 100)) + "%")
