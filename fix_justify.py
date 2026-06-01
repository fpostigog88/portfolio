with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove margin-bottom and margin-top inline styles from all column cards
# Left column cards
html = html.replace(
    '<div class="card" style="margin-bottom:16px;">\n      <div class="card-title">Work and Education</div>',
    '<div class="card">\n      <div class="card-title">Work and Education</div>'
)

html = html.replace(
    '<div class="card" style="margin-bottom:16px;">\n      <div class="card-title">AI & Cloud</div>',
    '<div class="card">\n      <div class="card-title">AI & Cloud</div>'
)

html = html.replace(
    '<div class="card" style="margin-top:auto;">\n      <div class="card-title">Productivity</div>',
    '<div class="card">\n      <div class="card-title">Productivity</div>'
)

# Center column cards
html = html.replace(
    '<div class="project-card" style="margin-bottom:16px;">\n      <div class="project-header">\n        <div class="project-title">⚙️ Autonomous Workflow Engine</div>',
    '<div class="project-card">\n      <div class="project-header">\n        <div class="project-title">⚙️ Autonomous Workflow Engine</div>'
)

html = html.replace(
    '<div class="project-card" style="margin-bottom:16px;">\n      <div class="project-header">\n        <div class="project-title">💰 FinanceApp</div>',
    '<div class="project-card">\n      <div class="project-header">\n        <div class="project-title">💰 FinanceApp</div>'
)

html = html.replace(
    '<div class="video-demo" style="margin-top:auto;">\n      <div class="video-demo-header">',
    '<div class="video-demo">\n      <div class="video-demo-header">'
)

# Right column cards
html = html.replace(
    '<div class="agent-panel" style="margin-bottom:16px;">\n      <div class="agent-panel-title">',
    '<div class="agent-panel">\n      <div class="agent-panel-title">'
)

html = html.replace(
    '<div class="card" style="margin-top:auto;">\n      <div class="card-title">Tech Stack</div>',
    '<div class="card">\n      <div class="card-title">Tech Stack</div>'
)

# Add justify-content: space-between and gap back to columns
html = html.replace(
    '<div class="left-col" style="display:flex;flex-direction:column;flex:0 0 280px;">',
    '<div class="left-col" style="display:flex;flex-direction:column;gap:16px;justify-content:space-between;flex:0 0 280px;">'
)

html = html.replace(
    '<div class="center-col" style="display:flex;flex-direction:column;flex:1 1 0;">',
    '<div class="center-col" style="display:flex;flex-direction:column;gap:16px;justify-content:space-between;flex:1 1 0;">'
)

html = html.replace(
    '<div class="right-col" style="display:flex;flex-direction:column;flex:0 0 280px;">',
    '<div class="right-col" style="display:flex;flex-direction:column;gap:16px;justify-content:space-between;flex:0 0 280px;">'
)

# Wrap iframe in a container with max-height to prevent overflow
html = html.replace(
    '<iframe width="100%" height="120" src="https://www.youtube-nocookie.com/embed/yAfvXZR69eY" title="Autonomous Workflow Engine Demo" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen style="border-radius:8px;max-width:480px;margin:0 auto;display:block;"></iframe>',
    '<div style="max-height:120px;overflow:hidden;border-radius:8px;"><iframe width="100%" height="120" src="https://www.youtube-nocookie.com/embed/yAfvXZR69eY" title="Autonomous Workflow Engine Demo" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen style="border-radius:8px;max-width:480px;margin:0 auto;display:block;"></iframe></div>'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done! Justify-content approach with gap and max-height wrapper applied.")
