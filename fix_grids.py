with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Make main grid wider side columns (280px), narrower middle, smaller gap
html = html.replace(
    '''.main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 0;
  display: grid;
  grid-template-columns: 220px 1fr 220px;
  gap: 24px;
  align-items: start;
}''',
    '''.main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 0;
  display: grid;
  grid-template-columns: 280px 1fr 280px;
  gap: 16px;
  align-items: start;
}'''
)

# 2. Work & Education: 2x2 grid
old_work_grid = '''    <!-- Work Logos -->
    <div class="card">
      <div class="card-title">Work & Education</div>
      <div class="logo-grid">'''
new_work_grid = '''    <!-- Work Logos -->
    <div class="card">
      <div class="card-title">Work & Education</div>
      <div class="logo-grid" style="grid-template-columns:repeat(2,1fr);gap:10px;">'''
html = html.replace(old_work_grid, new_work_grid)

# 3. AI & Cloud: remove OpenClaw, make 2x3 grid
old_ai = '''    <!-- Tech Logos -->
    <div class="card">
      <div class="card-title">AI & Cloud</div>
      <div class="logo-grid">
        <div class="logo-item">
          <img src="https://upload.wikimedia.org/wikipedia/commons/4/4d/OpenAI_Logo.svg" alt="OpenAI" onerror="this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#10a37f\\'>O</div>OpenAI'">
          OpenAI
        </div>
        <div class="logo-item">
          <img src="logo_claude.png" alt="Claude" style="width:28px;height:28px;object-fit:contain;border-radius:6px;">
          Claude
        </div>
        <div class="logo-item">
          <img src="logo_fireworks.png" alt="Fireworks" style="width:28px;height:28px;object-fit:contain;border-radius:6px;">
          Fireworks
        </div>
        <div class="logo-item">
          <img src="logo_llama.png" alt="llama.cpp" style="width:28px;height:28px;object-fit:contain;border-radius:6px;">
          llama.cpp
        </div>
        <div class="logo-item">
          <img src="logo_qwen.png" alt="Qwen" style="width:28px;height:28px;object-fit:contain;border-radius:6px;">
          Qwen
        </div>
        <div class="logo-item">
          <img src="logo_advisor.webp" alt="Hermes" style="width:28px;height:28px;object-fit:contain;border-radius:6px;">
          Hermes
        </div>
        <div class="logo-item">
          <img src="logo_openclaw.webp" alt="OpenClaw" style="width:28px;height:28px;object-fit:contain;border-radius:6px;">
          OpenClaw
        </div>
      </div>
    </div>'''

new_ai = '''    <!-- Tech Logos -->
    <div class="card">
      <div class="card-title">AI & Cloud</div>
      <div class="logo-grid" style="grid-template-columns:repeat(3,1fr);gap:8px;">
        <div class="logo-item">
          <img src="https://upload.wikimedia.org/wikipedia/commons/4/4d/OpenAI_Logo.svg" alt="OpenAI" onerror="this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#10a37f\\'>O</div>OpenAI'">
          OpenAI
        </div>
        <div class="logo-item">
          <img src="logo_claude.png" alt="Claude" style="width:28px;height:28px;object-fit:contain;border-radius:6px;">
          Claude
        </div>
        <div class="logo-item">
          <img src="logo_fireworks.png" alt="Fireworks" style="width:28px;height:28px;object-fit:contain;border-radius:6px;">
          Fireworks
        </div>
        <div class="logo-item">
          <img src="logo_llama.png" alt="llama.cpp" style="width:28px;height:28px;object-fit:contain;border-radius:6px;">
          llama.cpp
        </div>
        <div class="logo-item">
          <img src="logo_qwen.png" alt="Qwen" style="width:28px;height:28px;object-fit:contain;border-radius:6px;">
          Qwen
        </div>
        <div class="logo-item">
          <img src="logo_advisor.webp" alt="Hermes" style="width:28px;height:28px;object-fit:contain;border-radius:6px;">
          Hermes
        </div>
      </div>
    </div>'''

html = html.replace(old_ai, new_ai)

# 4. Tech Stack: 2x2 grid
old_tech = '''    <div class="card">
      <div class="card-title">Tech Stack</div>
      <div class="logo-grid">
        <div class="logo-item"><img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" alt="Python" onerror="this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#3776ab\\'>Py</div>Python'">Python</div>
        <div class="logo-item"><img src="https://upload.wikimedia.org/wikipedia/commons/9/97/Sqlite-square-icon.svg" alt="SQLite" onerror="this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#003b57\\'>SQL</div>SQLite'">SQLite</div>
        <div class="logo-item"><img src="https://upload.wikimedia.org/wikipedia/commons/4/4e/Docker_%28container_engine%29_logo.svg" alt="Docker" onerror="this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#2496ed\\'>Do</div>Docker'">Docker</div>
        <div class="logo-item"><img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" alt="GitHub" onerror="this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#181717\\'>GH</div>GitHub'">GitHub</div>
      </div>
    </div>'''

new_tech = '''    <div class="card">
      <div class="card-title">Tech Stack</div>
      <div class="logo-grid" style="grid-template-columns:repeat(2,1fr);gap:10px;">
        <div class="logo-item"><img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" alt="Python" onerror="this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#3776ab\\'>Py</div>Python'">Python</div>
        <div class="logo-item"><img src="https://upload.wikimedia.org/wikipedia/commons/9/97/Sqlite-square-icon.svg" alt="SQLite" onerror="this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#003b57\\'>SQL</div>SQLite'">SQLite</div>
        <div class="logo-item"><img src="https://upload.wikimedia.org/wikipedia/commons/4/4e/Docker_%28container_engine%29_logo.svg" alt="Docker" onerror="this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#2496ed\\'>Do</div>Docker'">Docker</div>
        <div class="logo-item"><img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" alt="GitHub" onerror="this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#181717\\'>GH</div>GitHub'">GitHub</div>
      </div>
    </div>'''

html = html.replace(old_tech, new_tech)

# 5. Productivity: also 2x2 to be consistent
old_prod = '''    <div class="card">
      <div class="card-title">Productivity</div>
      <div class="logo-grid">
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
        <div class="logo-item">
          <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" alt="Python" onerror="this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#3776ab\\'>Py</div>Python'">
          Python
        </div>
      </div>
    </div>'''

html = html.replace(old_prod, new_prod)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done! Logo grids and column widths adjusted.")
