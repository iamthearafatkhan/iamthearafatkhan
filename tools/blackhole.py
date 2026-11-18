import os, urllib.request, json, math, random

TOKEN = os.environ["GITHUB_TOKEN"]
Q = {"query": "{ viewer { contributionsCollection { totalCommitContributions } } }"}
req = urllib.request.Request("https://api.github.com/graphql",
        data=json.dumps(Q).encode(),
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
N = json.load(urllib.request.urlopen(req))["data"]["viewer"]["contributionsCollection"]["totalCommitContributions"]

level = min(1.0, N / 800.0)                 # 0..1 mass (800 commits = full blaze)
hue   = 210 - 175 * level                   # cold blue  ->  hot orange-gold
disk  = f"hsl({hue:.0f} 100% {55+15*level:.0f}%)"
hot   = f"hsl({max(0,hue-25):.0f} 100% {72+15*level:.0f}%)"
dim   = f"hsl({hue:.0f} 90% {28+15*level:.0f}%)"

random.seed(42)                             # stable starfield
W, H = 800, 450
stars = "".join(
    f'<circle cx="{random.randint(0,W)}" cy="{random.randint(0,H)}" r="{random.choice([0.5,0.8,1.1]):.1f}" fill="#fff" opacity="{random.uniform(0.2,0.8):.2f}"/>'
    for _ in range(90))

cx, cy   = 400, 225
core_r   = 34 + 26 * level                  # shadow grows with mass
disk_rx  = 150 + 170 * level                # disk grows with mass
disk_ry  = disk_rx * 0.28
sw       = 3 + 9 * level                    # disk thickness grows

disk_path = (f"M {cx+disk_rx:.1f},{cy} A {disk_rx:.1f},{disk_ry:.1f} 0 1,0 {cx-disk_rx:.1f},{cy} "
             f"A {disk_rx:.1f},{disk_ry:.1f} 0 1,0 {cx+disk_rx:.1f},{cy}")

particles = ""
for i in range(4 + int(level * 5)):         # more mass -> more orbiting hot spots
    dur, begin = 6 + i * 0.7, i * 0.9
    particles += (f'<circle r="{1.5+2*level:.1f}" fill="{hot}">'
                  f'<animateMotion dur="{dur}s" begin="-{begin}s" repeatCount="indefinite" path="{disk_path}"/>'
                  f'</circle>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
  <radialGradient id="glow">
    <stop offset="0%"  stop-color="{hot}"  stop-opacity="{0.35+0.45*level:.2f}"/>
    <stop offset="45%" stop-color="{disk}" stop-opacity="{0.12+0.3*level:.2f}"/>
    <stop offset="100%" stop-color="#000" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="doppler" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%"  stop-color="{dim}"/>
    <stop offset="50%" stop-color="{disk}"/>
    <stop offset="100%" stop-color="{hot}"/>
  </linearGradient>
  <filter id="blur"><feGaussianBlur stdDeviation="{4+6*level:.1f}"/></filter>
  <filter id="soft"><feGaussianBlur stdDeviation="2"/></filter>
</defs>

<rect width="{W}" height="{H}" fill="#020204"/>
{stars}

<!-- outer glow -->
<ellipse cx="{cx}" cy="{cy}" rx="{disk_rx*1.25:.0f}" ry="{disk_ry*2.2:.0f}" fill="url(#glow)">
  <animate attributeName="opacity" values="0.7;1;0.7" dur="5s" repeatCount="indefinite"/>
</ellipse>

<!-- gravitational lensing: far side of disk bent ABOVE the shadow -->
<path d="M {cx-disk_rx:.0f},{cy} A {disk_rx:.0f},{disk_rx*0.55:.0f} 0 0,1 {cx+disk_rx:.0f},{cy}"
      fill="none" stroke="url(#doppler)" stroke-width="{sw*0.8:.1f}" opacity="0.85" filter="url(#soft)">
  <animate attributeName="opacity" values="0.6;0.95;0.6" dur="4s" repeatCount="indefinite"/>
</path>
<!-- lensing: far side bent BELOW the shadow -->
<path d="M {cx-disk_rx*0.75:.0f},{cy} A {disk_rx*0.75:.0f},{disk_rx*0.42:.0f} 0 0,0 {cx+disk_rx*0.75:.0f},{cy}"
      fill="none" stroke="{disk}" stroke-width="{sw*0.6:.1f}" opacity="0.6" filter="url(#soft)"/>

<!-- accretion disk -->
<ellipse cx="{cx}" cy="{cy}" rx="{disk_rx:.0f}" ry="{disk_ry:.0f}" fill="none"
         stroke="url(#doppler)" stroke-width="{sw:.1f}" filter="url(#blur)" opacity="0.9"/>
<ellipse cx="{cx}" cy="{cy}" rx="{disk_rx:.0f}" ry="{disk_ry:.0f}" fill="none"
         stroke="{hot}" stroke-width="{max(1,sw*0.35):.1f}" opacity="0.9"/>

<!-- orbiting hot spots -->
<g>{particles}</g>

<!-- event horizon shadow -->
<circle cx="{cx}" cy="{cy}" r="{core_r:.1f}" fill="#000"/>

<!-- photon ring (swirling) -->
<circle cx="{cx}" cy="{cy}" r="{core_r+3:.1f}" fill="none" stroke="{hot}" stroke-width="2" stroke-dasharray="6 8">
  <animate attributeName="stroke-dashoffset" values="0;140" dur="4s" repeatCount="indefinite"/>
</circle>
<circle cx="{cx}" cy="{cy}" r="{core_r+6:.1f}" fill="none" stroke="{disk}" stroke-width="1" opacity="0.5">
  <animate attributeName="opacity" values="0.3;0.7;0.3" dur="3s" repeatCount="indefinite"/>
</circle>

<text x="{cx}" y="{H-22}" fill="{hot}" font-family="monospace" font-size="15" text-anchor="middle" letter-spacing="3">
  MASS: {N} COMMITS ABSORBED · GRAVITY {level*100:.0f}%
</text>
</svg>'''

os.makedirs("assets", exist_ok=True)
open("assets/blackhole.svg", "w").write(svg)
print(f"OK: {N} commits -> gravity level {level:.2f}")
