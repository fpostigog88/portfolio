import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Make main grid align to top and expand middle column
html = html.replace(
    '''.main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px;
  display: grid;
  grid-template-columns: 320px 1fr 260px;
  gap: 24px;
}''',
    '''.main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px;
  display: grid;
  grid-template-columns: 280px 1fr 280px;
  gap: 24px;
  align-items: start;
}'''
)

# Also make left/right columns use flex to distribute cards evenly
old_left_col = '''  <!-- LEFT COLUMN -->
  <div class="left-col">'''
new_left_col = '''  <!-- LEFT COLUMN -->
  <div class="left-col" style="display:flex;flex-direction:column;gap:16px;">'''
html = html.replace(old_left_col, new_left_col)

old_right_col = '''  <!-- RIGHT COLUMN -->
  <div class="right-col">'''
new_right_col = '''  <!-- RIGHT COLUMN -->
  <div class="right-col" style="display:flex;flex-direction:column;gap:16px;">'''
html = html.replace(old_right_col, new_right_col)

# Remove margin-bottom from cards inside left/right since gap handles it
# But keep margin-bottom for center column cards
# Actually, let's just remove margin-bottom from cards in left/right columns by targeting them
# Since the columns have inline styles now, we can use CSS selectors, but inline is easier
# Let's just remove margin-bottom from .card and let the gap handle it
html = html.replace(
    '''.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 16px;
}''',
    '''.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 16px;
}
.left-col .card, .right-col .card {
  margin-bottom: 0;
}'''
)

# 2. Work & Education: remove GitHub, keep Dell, Moller, Michigan, UC Chile (4 items)
old_work = '''    <!-- Work Logos -->
    <div class="card">
      <div class="card-title">Work & Education</div>
      <div class="logo-grid logo-grid-5">
        <div class="logo-item">
          <img src="https://upload.wikimedia.org/wikipedia/commons/4/48/Dell_Logo.svg" alt="Dell" onerror="this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#007db8\\'>D</div>Dell'">
          Dell
        </div>
        <div class="logo-item">
          <img src="logo_moller.png" alt="Moller" style="width:28px;height:28px;object-fit:contain;border-radius:6px;">
          Moller
        </div>
        <div class="logo-item">
          <img src="https://upload.wikimedia.org/wikipedia/commons/f/fb/Michigan_Wolverines_logo.svg" alt="Michigan" onerror="this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#ffcb05;color:#00274c\\'>M</div>Michigan'">
          Michigan
        </div>
        <div class="logo-item">
          <img src="logo_uc.png" alt="UC" style="width:28px;height:28px;object-fit:contain;border-radius:6px;">
          UC Chile
        </div>
        <div class="logo-item">
          <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" alt="GitHub" onerror="this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#181717\\'>GH</div>GitHub'">
          GitHub
        </div>
      </div>
    </div>'''

new_work = '''    <!-- Work Logos -->
    <div class="card">
      <div class="card-title">Work & Education</div>
      <div class="logo-grid">
        <div class="logo-item">
          <img src="https://upload.wikimedia.org/wikipedia/commons/4/48/Dell_Logo.svg" alt="Dell" onerror="this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#007db8\\'>D</div>Dell'">
          Dell
        </div>
        <div class="logo-item">
          <img src="logo_moller.png" alt="Moller" style="width:28px;height:28px;object-fit:contain;border-radius:6px;">
          Moller
        </div>
        <div class="logo-item">
          <img src="https://upload.wikimedia.org/wikipedia/commons/f/fb/Michigan_Wolverines_logo.svg" alt="Michigan" onerror="this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#ffcb05;color:#00274c\\'>M</div>Michigan'">
          Michigan
        </div>
        <div class="logo-item">
          <img src="logo_uc.png" alt="UC" style="width:28px;height:28px;object-fit:contain;border-radius:6px;">
          UC Chile
        </div>
      </div>
    </div>'''

html = html.replace(old_work, new_work)

# 3. AI & Cloud: remove PowerBI, keep OpenAI, Claude, Fireworks, llama.cpp, Qwen, Hermes, OpenClaw
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
          <img src="https://upload.wikimedia.org/wikipedia/commons/c/cf/New_Power_BI_Logo.svg" alt="PowerBI" onerror="this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#f2c811;color:#000\\'>P</div>PowerBI'">
          PowerBI
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
        <div class="logo-item">
          <div class="logo-placeholder" style="background:#f2c811;color:#000">P</div>
          PowerBI
        </div>
      </div>
    </div>'''

# Wait, the user wants PowerBI in Productivity, not in AI & Cloud. Let me fix this.
new_ai = '''    <!-- Tech Logos -->
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

html = html.replace(old_ai, new_ai)

# 4. Productivity: remove PPT and Word, add PowerBI, keep Excel and Python
old_prod = '''    <div class="card">
      <div class="card-title">Productivity</div>
      <div class="logo-grid">
        <div class="logo-item">
          <img src="logo_excel.png" alt="Excel" style="width:28px;height:28px;object-fit:contain;border-radius:6px;">
          Excel
        </div>
        <div class="logo-item">
          <img src="logo_powerpoint.png" alt="PPT" style="width:28px;height:28px;object-fit:contain;border-radius:6px;">
          PPT
        </div>
        <div class="logo-item">
          <img src="logo_word.png" alt="Word" style="width:28px;height:28px;object-fit:contain;border-radius:6px;">
          Word
        </div>
        <div class="logo-item">
          <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" alt="Python" onerror="this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#3776ab\\'>Py</div>Python'">
          Python
        </div>
      </div>
    </div>'''

new_prod = '''    <div class="card">
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

html = html.replace(old_prod, new_prod)

# 5. Tech Stack: add real GitHub logo
old_tech = '''    <div class="card">
      <div class="card-title">Tech Stack</div>
      <div class="logo-grid">
        <div class="logo-item"><img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" alt="Python" onerror="this.style.display='none';this.parentNode.innerHTML='<div class='logo-placeholder' style='background:#3776ab'>Py</div>Python'">Python</div>
        <div class="logo-item"><img src="https://upload.wikimedia.org/wikipedia/commons/9/97/Sqlite-square-icon.svg" alt="SQLite" onerror="this.style.display='none';this.parentNode.innerHTML='<div class='logo-placeholder' style='background:#003b57'>SQL</div>SQLite'">SQLite</div>
        <div class="logo-item"><img src="https://upload.wikimedia.org/wikipedia/commons/4/4e/Docker_%28container_engine%29_logo.svg" alt="Docker" onerror="this.style.display='none';this.parentNode.innerHTML='<div class='logo-placeholder' style='background:#2496ed'>Do</div>Docker'">Docker</div>
        <div class="logo-item"><div class="logo-placeholder" style="background:#181717">GH</div>GitHub</div>
      </div>
    </div>'''

new_tech = '''    <div class="card">
      <div class="card-title">Tech Stack</div>
      <div class="logo-grid">
        <div class="logo-item"><img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" alt="Python" onerror="this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#3776ab\\'>Py</div>Python'">Python</div>
        <div class="logo-item"><img src="https://upload.wikimedia.org/wikipedia/commons/9/97/Sqlite-square-icon.svg" alt="SQLite" onerror="this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#003b57\\'>SQL</div>SQLite'">SQLite</div>
        <div class="logo-item"><img src="https://upload.wikimedia.org/wikipedia/commons/4/4e/Docker_%28container_engine%29_logo.svg" alt="Docker" onerror="this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#2496ed\\'>Do</div>Docker'">Docker</div>
        <div class="logo-item"><img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" alt="GitHub" onerror="this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#181717\\'>GH</div>GitHub'">GitHub</div>
      </div>
    </div>'''

html = html.replace(old_tech, new_tech)

# 6. Fix Experience cards - use correct titles from resume and make them aligned
# Make exp-grid use align-items: stretch (default) and add consistent card styling
html = html.replace(
    '''.exp-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}''',
    '''.exp-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  align-items: stretch;
}
.exp-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
}
.exp-card > div:last-child {
  margin-top: auto;
}'''
)

# Remove old .exp-card CSS since we replaced it
html = html.replace(
    '''.exp-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
}
.exp-card .exp-company { font-size: 0.85rem; }
.exp-card .exp-role { font-size: 0.75rem; margin-bottom: 6px; }
.exp-card .exp-desc { font-size: 0.7rem; margin-bottom: 8px; }''',
    '''.exp-card .exp-company { font-size: 0.85rem; }
.exp-card .exp-role { font-size: 0.75rem; margin-bottom: 6px; }
.exp-card .exp-desc { font-size: 0.7rem; margin-bottom: 8px; }'''
)

# 7. Update Dell experience with correct title from resume
old_dell_exp = '''    <div class="exp-card">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <img src="logo_dell.png" alt="Dell" style="width:24px;height:24px;object-fit:contain;">
        <div class="exp-company">Dell Technologies</div>
      </div>
      <div class="exp-role">Sr. Advisor — AI/ML (2023–Present)</div>
      <div class="exp-desc">$16B Lead Price Plan (90%+ accuracy). Margin Leakage AI — 7 cross-referenced ML models. Saved 120+ hours/quarter.</div>
      <div><span class="exp-tag">AI/ML</span><span class="exp-tag">Pricing</span></div>
    </div>'''

new_dell_exp = '''    <div class="exp-card">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <img src="logo_dell.png" alt="Dell" style="width:24px;height:24px;object-fit:contain;">
        <div class="exp-company">Dell Technologies</div>
      </div>
      <div class="exp-role">Lead — Analytics, AI & Program Strategy (2023–2026)</div>
      <div class="exp-desc">Led digital transformation from 2-person 80-hour process to 1-person streamlined operation. $16B+ enterprise server revenue with 90%+ forecast accuracy. Built AI-enabled forecasting models and executive reporting ecosystems.</div>
      <div><span class="exp-tag">AI/ML</span><span class="exp-tag">Strategy</span></div>
    </div>'''

html = html.replace(old_dell_exp, new_dell_exp)

# 8. Update ACHS experience with correct description from resume
old_acgs_exp = '''    <div class="exp-card">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <img src="logo_acgs.png" alt="ACHS" style="width:24px;height:24px;object-fit:cover;border-radius:4px;">
        <div class="exp-company">ACHS (Hospital)</div>
      </div>
      <div class="exp-role">Commercial Head (2020–2021)</div>
      <div class="exp-desc">+20% sales, -60% invoice time. Data analytics dashboard (-90% reporting time).</div>
      <div><span class="exp-tag">Strategy</span><span class="exp-tag">Analytics</span></div>
    </div>'''

new_acgs_exp = '''    <div class="exp-card">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <img src="logo_acgs.png" alt="ACHS" style="width:24px;height:24px;object-fit:cover;border-radius:4px;">
        <div class="exp-company">ACHS (Hospital)</div>
      </div>
      <div class="exp-role">Commercial Head (2020–2021)</div>
      <div class="exp-desc">Redesigned data-driven commercial workflows and customer engagement increasing sales 20%. Built commercial performance dashboards and operational analytics reducing reporting effort by 90%.</div>
      <div><span class="exp-tag">Strategy</span><span class="exp-tag">Analytics</span></div>
    </div>'''

html = html.replace(old_acgs_exp, new_acgs_exp)

# 9. Update Moller cards with correct titles from resume
old_moller1 = '''    <div class="exp-card">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <img src="logo_moller.png" alt="Moller" style="width:24px;height:24px;object-fit:contain;">
        <div class="exp-company">Moller y Perez-Cotapos</div>
      </div>
      <div class="exp-role">Associate Manager — Real Estate Business Development (2018–2020)</div>
      <div class="exp-desc">Led team of 7 analysts. Acquired 10 properties worth $64.6M. 22 investment projects, +60% business unit profit. Automated forecasting models (+50% accuracy, -25% execution time).</div>
      <div><span class="exp-tag">Real Estate</span><span class="exp-tag">Leadership</span></div>
    </div>'''

new_moller1 = '''    <div class="exp-card">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <img src="logo_moller.png" alt="Moller" style="width:24px;height:24px;object-fit:contain;">
        <div class="exp-company">Moller y Perez-Cotapos</div>
      </div>
      <div class="exp-role">Associate Manager — Real Estate Business Development (2018–2020)</div>
      <div class="exp-desc">Led team of 7 analysts. Acquired 10 properties worth $64.6M. 22 investment projects, +60% business unit profit. Automated forecasting models (+50% accuracy, -25% execution time).</div>
      <div><span class="exp-tag">Real Estate</span><span class="exp-tag">Leadership</span></div>
    </div>'''

# Already correct, keep it
html = html.replace(old_moller1, new_moller1)

old_moller2 = '''    <div class="exp-card">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <img src="logo_moller.png" alt="Moller" style="width:24px;height:24px;object-fit:contain;">
        <div class="exp-company">Moller y Perez-Cotapos</div>
      </div>
      <div class="exp-role">Head of Real Estate Business Development (2017–2018)</div>
      <div class="exp-desc">Acquired 9 properties for $57M. Closed 8 fund deals for $40M at 11% ROI. Evaluated 1.2K properties worth $4.2B.</div>
      <div><span class="exp-tag">Strategy</span><span class="exp-tag">Negotiation</span></div>
    </div>'''

new_moller2 = '''    <div class="exp-card">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <img src="logo_moller.png" alt="Moller" style="width:24px;height:24px;object-fit:contain;">
        <div class="exp-company">Moller y Perez-Cotapos</div>
      </div>
      <div class="exp-role">Head of Real Estate Business Development (2017–2018)</div>
      <div class="exp-desc">Developed and presented strategy to board of directors, acquired 9 properties for $57M. Closed 8 fund deals for $40M at 11% ROI. Evaluated 1.2K properties worth $4.2B.</div>
      <div><span class="exp-tag">Strategy</span><span class="exp-tag">Negotiation</span></div>
    </div>'''

html = html.replace(old_moller2, new_moller2)

old_moller3 = '''    <div class="exp-card">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <img src="logo_moller.png" alt="Moller" style="width:24px;height:24px;object-fit:contain;">
        <div class="exp-company">Moller y Perez-Cotapos</div>
      </div>
      <div class="exp-role">Real Estate Product Manager (2014–2017)</div>
      <div class="exp-desc">+25% monthly sales via cross-functional execution. Resolved permitting bottlenecks. Managed construction contracts for cost/quality.</div>
      <div><span class="exp-tag">Product</span><span class="exp-tag">Operations</span></div>
    </div>'''

new_moller3 = '''    <div class="exp-card">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <img src="logo_moller.png" alt="Moller" style="width:24px;height:24px;object-fit:contain;">
        <div class="exp-company">Moller y Perez-Cotapos</div>
      </div>
      <div class="exp-role">Real Estate Product Manager (2014–2017)</div>
      <div class="exp-desc">Directed cross-functional execution across sales, marketing, construction, and development. +25% monthly sales. Resolved permitting bottlenecks. Negotiated construction contracts for cost/quality.</div>
      <div><span class="exp-tag">Product</span><span class="exp-tag">Operations</span></div>
    </div>'''

html = html.replace(old_moller3, new_moller3)

old_moller4 = '''    <div class="exp-card">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <img src="logo_moller.png" alt="Moller" style="width:24px;height:24px;object-fit:contain;">
        <div class="exp-company">Moller y Perez-Cotapos</div>
      </div>
      <div class="exp-role">Development Engineer — Real Estate Division (2012–2014)</div>
      <div class="exp-desc">Market research and financial modeling on hundreds of properties yearly.</div>
      <div><span class="exp-tag">Analysis</span></div>
    </div>'''

new_moller4 = '''    <div class="exp-card">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <img src="logo_moller.png" alt="Moller" style="width:24px;height:24px;object-fit:contain;">
        <div class="exp-company">Moller y Perez-Cotapos</div>
      </div>
      <div class="exp-role">Development Engineer — Real Estate Division (2012–2014)</div>
      <div class="exp-desc">Conducted market research and financial modeling on hundreds of properties yearly.</div>
      <div><span class="exp-tag">Analysis</span></div>
    </div>'''

html = html.replace(old_moller4, new_moller4)

# 10. Update education cards with correct text from resume
old_michigan = '''    <div class="exp-card">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/f/fb/Michigan_Wolverines_logo.svg" alt="Michigan" style="width:24px;height:24px;object-fit:contain;">
        <div class="exp-company">University of Michigan</div>
      </div>
      <div class="exp-role">MBA, Ross School of Business (2023)</div>
      <div class="exp-desc">Dean's Fellowship (Full-Tuition Merit Scholarship). Focus on strategy and operations.</div>
      <div><span class="exp-tag">MBA</span></div>
    </div>'''

new_michigan = '''    <div class="exp-card">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/f/fb/Michigan_Wolverines_logo.svg" alt="Michigan" style="width:24px;height:24px;object-fit:contain;">
        <div class="exp-company">University of Michigan</div>
      </div>
      <div class="exp-role">MBA, Stephen M. Ross School of Business (2023)</div>
      <div class="exp-desc">Awarded Dean's Fellowship (Merit Full-Tuition Scholarship). Focus on strategy and operations.</div>
      <div><span class="exp-tag">MBA</span></div>
    </div>'''

html = html.replace(old_michigan, new_michigan)

old_uc = '''    <div class="exp-card">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <img src="logo_uc.png" alt="UC" style="width:24px;height:24px;object-fit:contain;">
        <div class="exp-company">Universidad Catolica de Chile</div>
      </div>
      <div class="exp-role">BBA, Honors Scholarship (2012)</div>
      <div class="exp-desc">Graduated top 11%. Teaching assistant. Mentorship.</div>
      <div><span class="exp-tag">BBA</span></div>
    </div>'''

new_uc = '''    <div class="exp-card">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <img src="logo_uc.png" alt="UC" style="width:24px;height:24px;object-fit:contain;">
        <div class="exp-company">Universidad Catolica de Chile</div>
      </div>
      <div class="exp-role">BBA, Honors Scholarship (2012)</div>
      <div class="exp-desc">Awarded Honors Scholarship. Graduated top 11%. Teaching assistant and mentorship.</div>
      <div><span class="exp-tag">BBA</span></div>
    </div>'''

html = html.replace(old_uc, new_uc)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done! Layout and content fixes applied.")
