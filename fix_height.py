with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add height: 100% to main grid and columns
html = html.replace(
    '''.main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 0;
  display: grid;
  grid-template-columns: 280px 1fr 280px;
  gap: 16px;
  align-items: stretch;
}''',
    '''.main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 0;
  display: grid;
  grid-template-columns: 280px 1fr 280px;
  gap: 16px;
  align-items: stretch;
  min-height: 500px;
}'''
)

# 2. Add height: 100% to all columns
html = html.replace(
    '<div class="left-col" style="display:flex;flex-direction:column;gap:16px;">',
    '<div class="left-col" style="display:flex;flex-direction:column;gap:16px;height:100%;">'
)

html = html.replace(
    '<div class="center-col" style="display:flex;flex-direction:column;gap:16px;">',
    '<div class="center-col" style="display:flex;flex-direction:column;gap:16px;height:100%;">'
)

html = html.replace(
    '<div class="right-col" style="display:flex;flex-direction:column;gap:16px;">',
    '<div class="right-col" style="display:flex;flex-direction:column;gap:16px;height:100%;">'
)

# 3. Add flex-grow: 1 to the last card in each column
# Left column: Productivity card
html = html.replace(
    '<div class="card" style="margin-top:auto;">\n      <div class="card-title">Productivity</div>',
    '<div class="card" style="margin-top:auto;flex-grow:1;">\n      <div class="card-title">Productivity</div>'
)

# Center column: Live System Demo
html = html.replace(
    '<div class="video-demo" style="margin-top:auto;">',
    '<div class="video-demo" style="margin-top:auto;flex-grow:1;">'
)

# Right column: Tech Stack
html = html.replace(
    '<div class="card" style="margin-top:auto;">\n      <div class="card-title">Tech Stack</div>',
    '<div class="card" style="margin-top:auto;flex-grow:1;">\n      <div class="card-title">Tech Stack</div>'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done! Height and flex-grow fixes applied.")
