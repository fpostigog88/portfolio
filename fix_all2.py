import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Increase left column width from 260px to 300px
html = html.replace(
    'grid-template-columns: 260px 1fr 300px;',
    'grid-template-columns: 300px 1fr 280px;'
)

# Also increase left column card padding
html = html.replace(
    '.card {\n  background: var(--bg-card);\n  border: 1px solid var(--border);\n  border-radius: 12px;\n  padding: 20px;\n  margin-bottom: 16px;\n}',
    '.card {\n  background: var(--bg-card);\n  border: 1px solid var(--border);\n  border-radius: 12px;\n  padding: 24px;\n  margin-bottom: 16px;\n}'
)

# 2. Donna: remove "Life & travel planning", keep just "Personal Advisor"
html = html.replace(
    '<div class="agent-desc">Personal Advisor — Life & travel planning</div>',
    '<div class="agent-desc">Personal Advisor</div>'
)

# 3. Add GitHub logo to Work & Education section (replace Hermes/OpenClaw or add)
# Looking at the current Work & Education: Dell, Moller, Michigan, UC Chile
# We need to add GitHub. Let's make it 5 items or replace one. User said "missing github logo"
# Let's add GitHub to the Work & Education grid (make it 5 items in a row, or adjust grid)
old_work_ed = '''    <!-- Work Logos -->
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

new_work_ed = '''    <!-- Work Logos -->
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
        <div class="logo-item">
          <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" alt="GitHub" onerror="this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#181717\\'>GH</div>GitHub'">
          GitHub
        </div>
      </div>
    </div>'''

html = html.replace(old_work_ed, new_work_ed)

# Also adjust logo-grid for 5 items to look good
# Change grid to repeat(5, 1fr) for Work & Education
# But we need to target only that specific card. Let's add a class.
# Instead, let's just change the global logo-grid to handle 5 items
html = html.replace(
    '.logo-grid {\n  display: grid;\n  grid-template-columns: repeat(4, 1fr);\n  gap: 8px;\n}',
    '.logo-grid {\n  display: grid;\n  grid-template-columns: repeat(4, 1fr);\n  gap: 8px;\n}\n.logo-grid-5 {\n  grid-template-columns: repeat(5, 1fr);\n}'
)

# Add class to Work & Education logo-grid
html = html.replace(
    '<div class="card-title">Work & Education</div>\n      <div class="logo-grid">',
    '<div class="card-title">Work & Education</div>\n      <div class="logo-grid logo-grid-5">'
)

# 4. Split Moller into 4 individual blocks
old_moller = '''    <div class="exp-card">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <img src="logo_moller.png" alt="Moller" style="width:24px;height:24px;object-fit:contain;">
        <div class="exp-company">Moller y Perez-Cotapos</div>
      </div>
      <div class="exp-role">Associate Manager — Real Estate Business Development (2018–2020)</div>
      <div class="exp-desc">Led team of 7 analysts. Acquired 10 properties worth $64.6M. 22 investment projects, +60% business unit profit. Automated forecasting models (+50% accuracy, -25% execution time).</div>
      <div><span class="exp-tag">Real Estate</span><span class="exp-tag">Leadership</span></div>
      <div class="exp-role" style="margin-top:10px;">Head of Real Estate Business Development (2017–2018)</div>
      <div class="exp-desc">Acquired 9 properties for $57M. Closed 8 fund deals for $40M at 11% ROI. Evaluated 1.2K properties worth $4.2B.</div>
      <div><span class="exp-tag">Strategy</span><span class="exp-tag">Negotiation</span></div>
      <div class="exp-role" style="margin-top:10px;">Real Estate Product Manager (2014–2017)</div>
      <div class="exp-desc">+25% monthly sales via cross-functional execution. Resolved permitting bottlenecks. Managed construction contracts for cost/quality.</div>
      <div><span class="exp-tag">Product</span><span class="exp-tag">Operations</span></div>
      <div class="exp-role" style="margin-top:10px;">Development Engineer — Real Estate Division (2012–2014)</div>
      <div class="exp-desc">Market research and financial modeling on hundreds of properties yearly.</div>
      <div><span class="exp-tag">Analysis</span></div>
    </div>'''

new_moller = '''    <div class="exp-card">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <img src="logo_moller.png" alt="Moller" style="width:24px;height:24px;object-fit:contain;">
        <div class="exp-company">Moller y Perez-Cotapos</div>
      </div>
      <div class="exp-role">Associate Manager — Real Estate Business Development (2018–2020)</div>
      <div class="exp-desc">Led team of 7 analysts. Acquired 10 properties worth $64.6M. 22 investment projects, +60% business unit profit. Automated forecasting models (+50% accuracy, -25% execution time).</div>
      <div><span class="exp-tag">Real Estate</span><span class="exp-tag">Leadership</span></div>
    </div>
    <div class="exp-card">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <img src="logo_moller.png" alt="Moller" style="width:24px;height:24px;object-fit:contain;">
        <div class="exp-company">Moller y Perez-Cotapos</div>
      </div>
      <div class="exp-role">Head of Real Estate Business Development (2017–2018)</div>
      <div class="exp-desc">Acquired 9 properties for $57M. Closed 8 fund deals for $40M at 11% ROI. Evaluated 1.2K properties worth $4.2B.</div>
      <div><span class="exp-tag">Strategy</span><span class="exp-tag">Negotiation</span></div>
    </div>
    <div class="exp-card">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <img src="logo_moller.png" alt="Moller" style="width:24px;height:24px;object-fit:contain;">
        <div class="exp-company">Moller y Perez-Cotapos</div>
      </div>
      <div class="exp-role">Real Estate Product Manager (2014–2017)</div>
      <div class="exp-desc">+25% monthly sales via cross-functional execution. Resolved permitting bottlenecks. Managed construction contracts for cost/quality.</div>
      <div><span class="exp-tag">Product</span><span class="exp-tag">Operations</span></div>
    </div>
    <div class="exp-card">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <img src="logo_moller.png" alt="Moller" style="width:24px;height:24px;object-fit:contain;">
        <div class="exp-company">Moller y Perez-Cotapos</div>
      </div>
      <div class="exp-role">Development Engineer — Real Estate Division (2012–2014)</div>
      <div class="exp-desc">Market research and financial modeling on hundreds of properties yearly.</div>
      <div><span class="exp-tag">Analysis</span></div>
    </div>'''

html = html.replace(old_moller, new_moller)

# 5. Remove project links (tech tags) from Autonomous Workflow and FinanceApp
# Remove the entire project-links div from Autonomous Workflow
old_aw_links = '''      <div class="project-links">
        <span class="project-link link-secondary">Python</span>
        <span class="project-link link-secondary">ADB</span>
        <span class="project-link link-secondary">Android</span>
      </div>
    </div>

    <div class="project-card">
      <div class="project-header">
        <div class="project-title">💰 FinanceApp</div>'''

new_aw_links = '''    </div>

    <div class="project-card">
      <div class="project-header">
        <div class="project-title">💰 FinanceApp</div>'''

html = html.replace(old_aw_links, new_aw_links)

# Remove project-links from FinanceApp
old_fa_links = '''      <div class="project-links">
        <span class="project-link link-secondary">Python</span>
        <span class="project-link link-secondary">SQLite</span>
        <span class="project-link link-secondary">Plaid API</span>
      </div>
    </div>

  </div>'''

new_fa_links = '''    </div>

  </div>'''

html = html.replace(old_fa_links, new_fa_links)

# 6. Remove "View Projects" button from hero
html = html.replace(
    '<a href="#projects" class="hero-cta hero-cta-secondary">💼 View Projects</a>\n      </div>',
    '</div>'
)

# 7. Ensure hero stats are same size - they're already grid 1fr 1fr, should be fine
# But let's make the stat values more consistent
# (already done in previous commits)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done! All changes applied.")
