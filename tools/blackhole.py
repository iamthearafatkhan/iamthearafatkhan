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
random.seed(42)

W = 900
H = 450
cx = 450
cy = 210

# Generate starfield background
stars = ""
for i in range(130):
    sx = random.randint(20, W - 20)
    sy = random.randint(20, H - 30)
    sr = random.choice([0.6, 1.0, 1.4])
    so = format(random.uniform(0.3, 0.9), ".2f")
    stars += f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="#ffffff" opacity="{so}"/>'

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
  <!-- Deep Space Background Gradient -->
  <radialGradient id="space" cx="50%" cy="50%" r="70%">
    <stop offset="0%" stop-color="#120c24"/>
    <stop offset="100%" stop-color="#05020a"/>
  </radialGradient>

  <!-- Accretion Disk Plasma Gradient -->
  <linearGradient id="disk-grad" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#ff2200" stop-opacity="0.85"/>
    <stop offset="30%" stop-color="#ff7700" stop-opacity="0.95"/>
    <stop offset="50%" stop-color="#ffea75" stop-opacity="1"/>
    <stop offset="70%" stop-color="#ff7700" stop-opacity="0.95"/>
    <stop offset="100%" stop-color="#ff2200" stop-opacity="0.85"/>
  </linearGradient>

  <!-- Gravitational Lensing Top Arc Gradient -->
  <linearGradient id="lens-grad" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#ff5500" stop-opacity="0.7"/>
    <stop offset="50%" stop-color="#fff5cc" stop-opacity="1"/>
    <stop offset="100%" stop-color="#ff5500" stop-opacity="0.7"/>
  </linearGradient>

  <!-- Glow and Blur Filters -->
  <filter id="glow-heavy" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="16" result="blur"/>
    <feMerge>
      <feMergeNode in="blur"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>

  <filter id="glow-soft" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="6"/>
  </filter>
</defs>

<!-- Background -->
<rect width="{W}" height="{H}" fill="url(#space)"/>
{stars}

<!-- Outer Accretion Disk Glow Layers -->
<ellipse cx="{cx}" cy="{cy + 15}" rx="280" ry="70" fill="none" stroke="#ff4500" stroke-width="35" opacity="0.35" filter="url(#glow-heavy)"/>
<ellipse cx="{cx}" cy="{cy + 15}" rx="260" ry="55" fill="none" stroke="#ffaa00" stroke-width="20" opacity="0.5" filter="url(#glow-soft)"/>

<!-- Lensed Upper Ring (Light bending over the black hole shadow) -->
<path d="M {cx - 245} {cy + 15} C {cx - 245} {cy - 80}, {cx + 245} {cy - 80}, {cx + 245} {cy + 15}" fill="none" stroke="url(#lens-grad)" stroke-width="14" filter="url(#glow-soft)"/>
<path d="M {cx - 245} {cy + 15} C {cx - 245} {cy - 80}, {cx + 245} {cy - 80}, {cx + 245} {cy + 15}" fill="none" stroke="#ffffff" stroke-width="3" opacity="0.95"/>

<!-- Black Hole Event Horizon (Pure Black Core) -->
<circle cx="{cx}" cy="{cy + 15}" r="55" fill="#000000"/>

<!-- Photon Sphere / Inner Rim White-Hot Ring -->
<circle cx="{cx}" cy="{cy + 15}" r="57" fill="none" stroke="#ffeedd" stroke-width="4" filter="url(#glow-soft)" opacity="0.9"/>
<circle cx="{cx}" cy="{cy + 15}" r="56" fill="none" stroke="#ffffff" stroke-width="1.5" opacity="1"/>

<!-- Front Accretion Disk (Passing in front of the black hole) -->
<path d="M {cx - 285} {cy + 15} C {cx - 285} {cy + 80}, {cx + 285} {cy + 80}, {cx + 285} {cy + 15} C {cx + 285} {cy - 10}, {cx - 285} {cy - 10}, {cx - 285} {cy + 15} Z" fill="url(#disk-grad)" filter="url(#glow-soft)"/>
<path d="M {cx - 285} {cy + 15} C {cx - 285} {cy + 80}, {cx + 285} {cy + 80}, {cx + 285} {cy + 15}" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.85"/>

<!-- README Footer Text -->
<text x="{cx}" y="{H - 25}" fill="#ffcc88" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-weight="700" font-size="14" text-anchor="middle" letter-spacing="2.5">MASS: {n} COMMITS ABSORBED</text>
</svg>
'''

os.makedirs("assets", exist_ok=True)
with open("assets/blackhole.svg", "w") as out:
    out.write(svg)

print("OK: " + str(n) + " commits, gravity " + str(int(level * 100)) + "%")
