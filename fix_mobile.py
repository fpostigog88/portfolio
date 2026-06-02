#!/usr/bin/env python3
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Make project cards in center column grow to fill space
# Add flex: 1 to project cards so they expand equally
content = content.replace(
    '<div class="project-card">',
    '<div class="project-card" style="flex:1;display:flex;flex-direction:column;">'
)

# 2. Fix video container to grow and fill remaining space
content = content.replace(
    '<div class="video-demo">',
    '<div class="video-demo" style="flex:1;display:flex;flex-direction:column;">'
)

# 3. Fix video player to fill the container
content = content.replace(
    '<div class="video-demo-player">',
    '<div class="video-demo-player" style="flex:1;display:flex;flex-direction:column;">'
)

# 4. Fix mobile responsiveness - change .main media queries to use flex-direction
# instead of grid-template-columns since .main uses display: flex
old_media = """@media (max-width: 1024px) {
  .main { grid-template-columns: 1fr 1fr; }
    .hero-inner { grid-template-columns: 1fr; }
    .hero-right { text-align: left; }
    .hero-stats { grid-template-columns: repeat(4, 1fr); }
    .exp-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 768px) {
  .main { grid-template-columns: 1fr; }
    .hero h1 { font-size: 2rem; }
    .hero-stats { grid-template-columns: 1fr 1fr; }
    .logo-grid { grid-template-columns: repeat(4, 1fr); }
    .ecosystem-grid { grid-template-columns: 1fr 1fr; }
    .hero-ctas { flex-direction: column; }
    .exp-grid { grid-template-columns: 1fr; }
}"""

new_media = """@media (max-width: 1024px) {
  .main { flex-direction: column; }
  .left-col, .right-col, .center-col { flex: 1 1 auto !important; width: 100% !important; }
  .hero-inner { grid-template-columns: 1fr; }
  .hero-right { text-align: left; }
  .hero-stats { grid-template-columns: repeat(4, 1fr); }
  .exp-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 768px) {
  .main { flex-direction: column; padding: 16px; }
  .left-col, .right-col, .center-col { flex: 1 1 auto !important; width: 100% !important; }
  .hero { padding: 32px 16px; }
  .hero h1 { font-size: 2rem; }
  .hero-stats { grid-template-columns: 1fr 1fr; }
  .logo-grid { grid-template-columns: repeat(4, 1fr); }
  .ecosystem-grid { grid-template-columns: 1fr 1fr; }
  .hero-ctas { flex-direction: column; }
  .exp-grid { grid-template-columns: 1fr; }
  .experience-section { padding: 0 16px 32px; }
  .footer { padding: 24px 16px; }
  .video-demo iframe { height: 200px; }
}"""

content = content.replace(old_media, new_media)

# 5. Add responsive iframe sizing for video
content = content.replace(
    'height="270"',
    'height="270" style="width:100%;"'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed mobile responsiveness and project card sizing")
