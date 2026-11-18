import os, urllib.request, json, math, random

token = os.environ["GITHUB_TOKEN"]
query = '{"query":"{ viewer { contributionsCollection { totalCommitContributions } } }"}'
req = urllib.request.Request("https://api.github.com/graphql", data=query.encode(), headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
resp = urllib.request.urlopen(req)
n = json.loads(resp.read())["data"]["viewer"]["contributionsCollection"]["totalCommitContributions"]

level = min(1.0, n / 800.0)
hue = 210 - 175 * level
disk = "hsl(" + str(int(hue)) + " 100% " + str(int(55 + 15 * level)) + "%)"
hot = "hsl(" + str(int(max(0, hue - 25))) + " 100% " + str(int(72 + 15 * level)) + "%)"
dim = "hsl(" + str(int(hue)) + " 90% " + str(int(28 + 15 * level)) + "%)"

random.seed(42)
W = 800
H = 450
stars = ""
for i in range(90):
    stars = stars + '<circle cx="' + str(random.randint(0, W)) + '" cy="' + str(random.randint(0, H)) + '" r="1" fill="#fff" opacity="0.5"/>'

cx = 400
cy = 225
core_r = 34 + 26 * level
disk_rx = 150 + 170 * level
disk_ry = disk_rx * 0.28
sw = 3 + 9 * level

disk_path = "M " + str(cx + disk_rx) + "," + str(cy) + " A " + str(disk_rx) + "," + str(disk_ry) + " 0 1,0 " + str(cx - disk_rx) + "," + str(cy) + " A " + str(disk_rx) + "," + str(disk_ry) + " 0 1,0 " + str(cx + disk_rx) + "," + str(cy)

particles = ""
for i in range(4 + int(level * 5)):
    dur = 6 + i * 0.7
    begin = i * 0.9
    particles = particles + '<circle r="2" fill="' + hot + '"><animateMotion dur="' + str(dur) + 's" begin="-' + str(begin) + 's" repeatCount="indefinite" path="' + disk_path + '"/></circle>'

svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + str(W) + ' ' + str(H) + '" width="' + str(W) + '" height="' + str(H) + '">'
svg = svg + '<defs><radialGradient id="glow"><stop offset="0%" stop-color="' + hot + '" stop-opacity="0.8"/><stop offset="50%" stop-color="' + disk + '" stop-opacity="0.3"/><stop offset="100%" stop-color="#000" stop-opacity="0"/></radialGradient>'
svg = svg + '<linearGradient id="doppler" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="' + dim + '"/><stop offset="50%" stop-color="' + disk + '"/><stop offset="100%" stop-color="' + hot + '"/></linearGradient>'
svg = svg + '<filter id="blur"><feGaussianBlur stdDeviation="6"/></filter></defs>'
svg = svg + '<rect width="' + str(W) + '" height="' + str(H) + '" fill="#020204"/>'
svg = svg + stars
svg = svg + '<ellipse cx="' + str(cx) + '" cy="' + str(cy) + '" rx="' + str(disk_rx * 1.25) + '" ry="' + str(disk_ry * 2.2) + '" fill="url(#glow)"><animate attributeName="opacity" values="0.7;1;0.7" dur="5s" repeatCount="indefinite"/></ellipse>'
svg = svg + '<path d="M ' + str(cx - disk_rx) + ',' + str(cy) + ' A ' + str(disk_rx) + ',' + str(disk_rx * 0.55) + ' 0 0,1 ' + str(cx + disk_rx) + ',' + str(cy) + '" fill="none" stroke="url(#doppler)" stroke-width="' + str(sw * 0.8) + '" opacity="0.85"/>'
svg = svg + '<path d="M ' + str(cx - disk_rx * 0.75) + ',' + str(cy) + ' A ' + str(disk_rx * 0.75) + ',' + str(disk_rx * 0.42) + ' 0 0,0 ' + str(cx + disk_rx * 0.75) + ',' + str(cy) + '" fill="none" stroke="' + disk + '" stroke-width="' + str(sw * 0.6) + '" opacity="0.6"/>'
svg = svg + '<ellipse cx="' + str(cx) + '" cy="' + str(cy) + '" rx="' + str(disk_rx) + '" ry="' + str(disk_ry) + '" fill="none" stroke="url(#doppler)" stroke-width="' + str(sw) + '" filter="url(#blur)"/>'
svg = svg + particles
svg = svg + '<circle cx="' + str(cx) + '" cy="' + str(cy) + '" r="' + str(core_r) + '" fill="#000"/>'
svg = svg + '<circle cx="' + str(cx) + '" cy="' + str(cy) + '" r="' + str(core_r + 3) + '" fill="none" stroke="' + hot + '" stroke-width="2" stroke-dasharray="6 8"><animate attributeName="stroke-dashoffset" values="0;140" dur="4s" repeatCount="indefinite"/></circle>'
svg = svg + '<circle cx="' + str(cx) + '" cy="' + str(cy) + '" r="' + str(core_r + 6) + '" fill="none" stroke="' + disk + '" stroke-width="1" opacity="0.5"><animate attributeName="opacity" values="0.3;0.7;0.3" dur="3s" repeatCount="indefinite"/></circle>'
svg = svg + '<text x="' + str(cx) + '" y="' + str(H - 22) + '" fill="' + hot + '" font-family="monospace" font-size="15" text-anchor="middle">MASS: ' + str(n) + ' COMMITS ABSORBED</text>'
svg = svg + '</svg>'

os.makedirs("assets", exist_ok=True)
f = open("assets/blackhole.svg", "w")
f.write(svg)
f.close()
print("OK: " + str(n) + " commits")
