with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Move video demo to bottom, projects to top in center column
old_center = '''  <!-- CENTER COLUMN -->
  <div class="center-col">

    <!-- Video Demo -->
    <div class="video-demo">
      <div class="video-demo-header">
        <div class="video-demo-title">🎬 Live System Demo</div>
        <div class="video-demo-badge">Production</div>
      </div>
      <div class="video-demo-player">
        <div class="video-demo-text">Autonomous Workflow Engine — PC-to-Android task execution</div>
        <iframe width="100%" height="280" src="https://www.youtube-nocookie.com/embed/yAfvXZR69eY" title="Autonomous Workflow Engine Demo" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen style="border-radius:8px;max-width:480px;margin:0 auto;display:block;"></iframe>
      </div>
    </div>

    <!-- Projects -->
    <div class="project-card">
      <div class="project-header">
        <div class="project-title">⚙️ Autonomous Workflow Engine</div>
        <span class="project-badge badge-green">Production</span>
      </div>
      <div class="project-desc">From PC orchestration to Android task execution. Automates repeatable mobile workflows using ADB control, scheduling logic, and execution monitoring.</div>
    </div>

    <div class="project-card">
      <div class="project-header">
        <div class="project-title">💰 FinanceApp</div>
        <span class="project-badge badge-green">Production</span>
      </div>
      <div class="project-desc">Personal finance intelligence with Plaid integration, automated categorization, anomaly detection, multi-bank aggregation. Encrypted local storage.</div>
    </div>

  </div>'''

new_center = '''  <!-- CENTER COLUMN -->
  <div class="center-col">

    <!-- Projects -->
    <div class="project-card">
      <div class="project-header">
        <div class="project-title">⚙️ Autonomous Workflow Engine</div>
        <span class="project-badge badge-green">Production</span>
      </div>
      <div class="project-desc">From PC orchestration to Android task execution. Automates repeatable mobile workflows using ADB control, scheduling logic, and execution monitoring.</div>
    </div>

    <div class="project-card">
      <div class="project-header">
        <div class="project-title">💰 FinanceApp</div>
        <span class="project-badge badge-green">Production</span>
      </div>
      <div class="project-desc">Personal finance intelligence with Plaid integration, automated categorization, anomaly detection, multi-bank aggregation. Encrypted local storage.</div>
    </div>

    <!-- Video Demo -->
    <div class="video-demo">
      <div class="video-demo-header">
        <div class="video-demo-title">🎬 Live System Demo</div>
        <div class="video-demo-badge">Production</div>
      </div>
      <div class="video-demo-player">
        <div class="video-demo-text">Autonomous Workflow Engine — PC-to-Android task execution</div>
        <iframe width="100%" height="280" src="https://www.youtube-nocookie.com/embed/yAfvXZR69eY" title="Autonomous Workflow Engine Demo" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen style="border-radius:8px;max-width:480px;margin:0 auto;display:block;"></iframe>
      </div>
    </div>

  </div>'''

html = html.replace(old_center, new_center)

# 2. Remove Python from Productivity
old_prod = '''    <div class="card">
      <div class="card-title">Productivity</div>
      <div class="logo-grid" style="grid-template-columns:repeat(2,1fr);gap:10px;">
        <div class="logo-item">
          <img src="logo_excel.png" alt="Excel" style="width:28px;height:28px;object-fit:contain;border-radius:6px;">
          Excel
        </div>
        <div class="logo-item">
          <img src="https://upload.wikimedia.org/wikipedia/commons/c/cf/New_Power_BI_Logo.svg" alt="PowerBI" onerror="this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#f2c811;color:#000\\'>P</div>PowerBI'">
          PowerBI
        </div>
        <div class="logo-item">
          <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" alt="Python" onerror="this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#3776ab\\'>Py</div>Python'">
          Python
        </div>
      </div>
    </div>'''

new_prod = '''    <div class="card">
      <div class="card-title">Productivity</div>
      <div class="logo-grid" style="grid-template-columns:repeat(2,1fr);gap:10px;">
        <div class="logo-item">
          <img src="logo_excel.png" alt="Excel" style="width:28px;height:28px;object-fit:contain;border-radius:6px;">
          Excel
        </div>
        <div class="logo-item">
          <img src="https://upload.wikimedia.org/wikipedia/commons/c/cf/New_Power_BI_Logo.svg" alt="PowerBI" onerror="this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#f2c811;color:#000\\'>P</div>PowerBI'">
          PowerBI
        </div>
      </div>
    </div>'''

html = html.replace(old_prod, new_prod)

# 3. Update all card titles to use accent-dark color and larger font
# The agent-panel-title uses var(--accent-dark) which is #8a6d4a
# Update card-title to match
html = html.replace(
    '''.card-title {
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}''',
    '''.card-title {
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--accent-dark);
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}'''
)

# 4. Update the Experience section title to be larger and accent-dark
html = html.replace(
    '<div class="card-title" style="margin-bottom:16px;">Experience</div>',
    '<div class="card-title" style="margin-bottom:16px;font-size:1rem;color:var(--accent-dark);">Experience</div>'
)

# 5. Update video-demo-title to also use accent-dark
html = html.replace(
    '''.video-demo-title {
  font-size: 1rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text);
}''',
    '''.video-demo-title {
  font-size: 1rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--accent-dark);
}'''
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done! Projects moved to top, video to bottom, Python removed, titles styled.")
