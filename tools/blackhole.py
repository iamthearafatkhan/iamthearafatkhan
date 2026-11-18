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
H = 460
cx = 450
cy = 220

# Generate starfield background
stars = ""
for i in range(120):
    sx = random.randint(20, W - 20)
    sy = random.randint(20, H - 30)
    sr = random.choice([0.5, 0.9, 1.3])
    so = format(random.uniform(0.2, 0.8), ".2f")
    dur = format(random.uniform(2.0, 5.0), ".1f")
    stars += f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="#ffffff" opacity="{so}"><animate attributeName="opacity" values="{so};0.1;{so}" dur="{dur}s" repeatCount="indefinite"/></circle>'

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
  <!-- Deep Space Background -->
  <radialGradient id="space" cx="50%" cy="50%" r="70%">
    <stop offset="0%" stop-color="#150d2a"/>
    <stop offset="100%" stop-color="#030108"/>
  </radialGradient>

  <!-- Accretion Disk Plasma Gradient -->
  <linearGradient id="disk-grad" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#991100" stop-opacity="0.8"/>
    <stop offset="25%" stop-color="#ff4500" stop-opacity="0.95"/>
    <stop offset="50%" stop-color="#ffea75" stop-opacity="1"/>
    <stop offset="75%" stop-color="#ff6600" stop-opacity="0.95"/>
    <stop offset="100%" stop-color="#991100" stop-opacity="0.8"/>
  </linearGradient>

  <!-- Gravitational Lensing Arch Gradient -->
  <linearGradient id="lens-grad" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#ff4500" stop-opacity="0.6"/>
    <stop offset="30%" stop-color="#ffaa33" stop-opacity="0.9"/>
    <stop offset="50%" stop-color="#ffffff" stop-opacity="1"/>
    <stop offset="70%" stop-color="#ffaa33" stop-opacity="0.9"/>
    <stop offset="100%" stop-color="#ff4500" stop-opacity="0.6"/>
  </linearGradient>

  <!-- Glow Filters -->
  <filter id="glow-heavy" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="18" result="blur"/>
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

<!-- Outer Accretion Disk Ambient Glow -->
<ellipse cx="{cx}" cy="{cy}" rx="300" ry="75" fill="none" stroke="#ff3300" stroke-width="40" opacity="0.3" filter="url(#glow-heavy)"/>
<ellipse cx="{cx}" cy="{cy}" rx="270" ry="60" fill="none" stroke="#ff9900" stroke-width="25" opacity="0.45" filter="url(#glow-soft)"/>

<!-- GROUP: Animated Accretion Elements (SMIL Animation for GitHub compatibility) -->
<g>
  <animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="20s" repeatCount="indefinite"/>
  
  <!-- Rear Accretion Disk Details (Swirling Plasma Texture) -->
  <path d="M {cx - 260} {cy} C {cx - 260} {cy + 40}, {cx + 260} {cy + 40}, {cx + 260} {cy}" fill="none" stroke="#ffeedd" stroke-width="3" stroke-dasharray="15 35" opacity="0.6"/>
</g>

<!-- Lensed Upper Ring (The characteristic Einstein Ring bending light over the top) -->
<path d="M {cx - 235} {cy} C {cx - 235} {cy - 95}, {cx + 235} {cy - 95}, {cx + 235} {cy}" fill="none" stroke="url(#lens-grad)" stroke-width="16" filter="url(#glow-soft)"/>
<path d="M {cx - 235} {cy} C {cx - 235} {cy - 95}, {cx + 235} {cy - 95}, {cx + 235} {cy}" fill="none" stroke="#ffffff" stroke-width="3.5" opacity="0.95"/>

<!-- Black Hole Event Horizon (Pure Black Core) -->
<circle cx="{cx}" cy="{cy}" r="52" fill="#000000"/>

<!-- Photon Sphere / Inner Rim White-Hot Ring (Pulsing via SMIL) -->
<g>
  <animate attributeName="opacity" values="0.85;1;0.85" dur="4s" repeatCount="indefinite"/>
  <circle cx="{cx}" cy="{cy}" r="54" fill="none" stroke="#ffeedd" stroke-width="4" filter="url(#glow-soft)" opacity="0.9"/>
  <circle cx="{cx}" cy="{cy}" r="53" fill="none" stroke="#ffffff" stroke-width="2" opacity="1"/>
</g>

<!-- Front Accretion Disk (Passing in front of the black hole shadow) -->
<path d="M {cx - 290} {cy} C {cx - 290} {cy + 90}, {cx + 290} {cy + 90}, {cx + 290} {cy} C {cx + 290} {cy - 12}, {cx - 290} {cy - 12}, {cx - 290} {cy} Z" fill="url(#disk-grad)" filter="url(#glow-soft)"/>
<path d="M {cx - 290} {cy} C {cx - 290} {cy + 90}, {cx + 290} {cy + 90}, {cx + 290} {cy}" fill="none" stroke="#ffffff" stroke-width="2.5" opacity="0.9"/>

<!-- README Footer Text -->
<text x="{cx}" y="{H - 22}" fill="#ffcc88" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-weight="700" font-size="14" text-anchor="middle" letter-spacing="2.5">MASS: {n} COMMITS ABSORBED</text>
</svg>
'''

os.makedirs("assets", exist_ok=True)
with open("assets/blackhole.svg", "w") as out:
    out.write(svg)

print("OK: " + str(n) + " commits rendered successfully!")
