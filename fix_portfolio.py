import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove Infrastructure section
infra_start = content.find('    <div class="card">\n      <div class="card-title">Infrastructure</div>')
if infra_start != -1:
    infra_end = content.find('    <!-- Experience -->', infra_start)
    if infra_end != -1:
        content = content[:infra_start] + '    <!-- Experience -->' + content[infra_end + len('    <!-- Experience -->'):]

# 2. Add Local AI below AI & Cloud
ai_cloud_end = content.find('    </div>\n\n    <div class="card">\n      <div class="card-title">Productivity</div>')
if ai_cloud_end != -1:
    local_ai = '''\n    <div class="card">
      <div class="card-title">Local AI</div>
      <div class="logo-grid">
        <div class="logo-item">
          <img src="logo_llama.png" alt="llama.cpp" style="width:28px;height:28px;object-fit:contain;border-radius:6px;">
          llama.cpp
        </div>
        <div class="logo-item">
          <img src="logo_qwen.png" alt="Qwen" style="width:28px;height:28px;object-fit:contain;border-radius:6px;">
          Qwen
        </div>
      </div>
    </div>'''
    content = content[:ai_cloud_end + len('    </div>')] + local_ai + content[ai_cloud_end + len('    </div>'):]

# 3. Remove Local AI from right sidebar
right_local_start = content.find('    <div class="card">\n      <div class="card-title">Local AI</div>\n      <div class="logo-grid">\n        <div class="logo-item"><svg width="28" height="28" viewBox="0 0 24 24" fill="white"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" fill="#6b7280"/></svg>llama.cpp</div>')
if right_local_start != -1:
    right_local_end = content.find('    </div>\n  </div>', right_local_start)
    if right_local_end != -1:
        content = content[:right_local_start] + content[right_local_end + len('    </div>'):]

# 4. Add logos to Experience cards
content = content.replace(
    '    <div class="exp-card">\n      <div class="exp-company">Dell Technologies</div>',
    '    <div class="exp-card">\n      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">\n        <img src="logo_dell.png" alt="Dell" style="width:24px;height:24px;object-fit:contain;">\n        <div class="exp-company">Dell Technologies</div>\n      </div>'
)

content = content.replace(
    '    <div class="exp-card">\n      <div class="exp-company">ACHS (Hospital)</div>',
    '    <div class="exp-card">\n      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">\n        <img src="logo_acgs.png" alt="ACHS" style="width:24px;height:24px;object-fit:cover;border-radius:4px;">\n        <div class="exp-company">ACHS (Hospital)</div>\n      </div>'
)

content = content.replace(
    '    <div class="exp-card">\n      <div class="exp-company">Moller y Perez-Cotapos</div>',
    '    <div class="exp-card">\n      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">\n        <img src="logo_moller.png" alt="Moller" style="width:24px;height:24px;object-fit:contain;">\n        <div class="exp-company">Moller y Perez-Cotapos</div>\n      </div>'
)

content = content.replace(
    '    <div class="exp-card">\n      <div class="exp-company">University of Michigan</div>',
    '    <div class="exp-card">\n      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">\n        <img src="https://upload.wikimedia.org/wikipedia/commons/f/fb/Michigan_Wolverines_logo.svg" alt="Michigan" style="width:24px;height:24px;object-fit:contain;">\n        <div class="exp-company">University of Michigan</div>\n      </div>'
)

content = content.replace(
    '    <div class="exp-card">\n      <div class="exp-company">Universidad Catolica de Chile</div>',
    '    <div class="exp-card">\n      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">\n        <img src="logo_uc.png" alt="UC" style="width:24px;height:24px;object-fit:contain;">\n        <div class="exp-company">Universidad Catolica de Chile</div>\n      </div>'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
