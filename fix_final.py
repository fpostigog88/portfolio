with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove justify-content: space-between and gap from columns, use margin-top: auto on last card
# Left column
html = html.replace(
    '<div class="left-col" style="display:flex;flex-direction:column;gap:16px;justify-content:space-between;flex:0 0 280px;">',
    '<div class="left-col" style="display:flex;flex-direction:column;flex:0 0 280px;">'
)

# Center column
html = html.replace(
    '<div class="center-col" style="display:flex;flex-direction:column;gap:16px;justify-content:space-between;flex:1 1 0;">',
    '<div class="center-col" style="display:flex;flex-direction:column;flex:1 1 0;">'
)

# Right column
html = html.replace(
    '<div class="right-col" style="display:flex;flex-direction:column;gap:16px;justify-content:space-between;flex:0 0 280px;">',
    '<div class="right-col" style="display:flex;flex-direction:column;flex:0 0 280px;">'
)

# Add margin-bottom to all cards except the last one in each column
# For left column cards
html = html.replace(
    '<div class="card">\n      <div class="card-title">Work and Education</div>',
    '<div class="card" style="margin-bottom:16px;">\n      <div class="card-title">Work and Education</div>'
)

html = html.replace(
    '<div class="card">\n      <div class="card-title">AI & Cloud</div>',
    '<div class="card" style="margin-bottom:16px;">\n      <div class="card-title">AI & Cloud</div>'
)

# Productivity card (last in left column) gets margin-top: auto
html = html.replace(
    '<div class="card">\n      <div class="card-title">Productivity</div>',
    '<div class="card" style="margin-top:auto;">\n      <div class="card-title">Productivity</div>'
)

# Center column cards
html = html.replace(
    '<div class="project-card">\n      <div class="project-header">\n        <div class="project-title">⚙️ Autonomous Workflow Engine</div>',
    '<div class="project-card" style="margin-bottom:16px;">\n      <div class="project-header">\n        <div class="project-title">⚙️ Autonomous Workflow Engine</div>'
)

html = html.replace(
    '<div class="project-card">\n      <div class="project-header">\n        <div class="project-title">💰 FinanceApp</div>',
    '<div class="project-card" style="margin-bottom:16px;">\n      <div class="project-header">\n        <div class="project-title">💰 FinanceApp</div>'
)

# Live System Demo (last in center column) gets margin-top: auto
html = html.replace(
    '<div class="video-demo">\n      <div class="video-demo-header">',
    '<div class="video-demo" style="margin-top:auto;">\n      <div class="video-demo-header">'
)

# Right column cards
# Agent panel (first in right column)
html = html.replace(
    '<div class="agent-panel">\n      <div class="agent-panel-title">',
    '<div class="agent-panel" style="margin-bottom:16px;">\n      <div class="agent-panel-title">'
)

# Tech Stack (last in right column) gets margin-top: auto
html = html.replace(
    '<div class="card">\n      <div class="card-title">Tech Stack</div>',
    '<div class="card" style="margin-top:auto;">\n      <div class="card-title">Tech Stack</div>'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done! Final alignment fixes applied.")
