import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Change Claire's description to "Automation and Workflows"
html = html.replace(
    '<div class="agent-desc">Walmart shopping automation</div>',
    '<div class="agent-desc">Automation and Workflows</div>'
)

# 2. Remove WhatsApp from hero contact links
# Find the WhatsApp link in hero-contact-links and remove it
whatsapp_pattern = r'\s*<a href="https://wa\.me/[^"]*" class="hero-contact-link"[^>]*>\s*<svg[^>]*>.*?</svg>\s*WhatsApp\s*</a>'
html = re.sub(whatsapp_pattern, '', html, flags=re.DOTALL)

# 3. Change "7 ML Models" to "90%+ Forecast Accuracy"
html = html.replace(
    '<div class="hero-stat-value">7</div>\n          <div class="hero-stat-label">ML Models</div>',
    '<div class="hero-stat-value">90%+</div>\n          <div class="hero-stat-label">Forecast Accuracy</div>'
)

# 4. Fix video demo - reduce size, make white background
# Change the .video-demo style to white background
old_video_demo = '''.video-demo {
  background: linear-gradient(135deg, #1a1a2e 0%, #2d2d44 100%);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
  color: white;
}'''
new_video_demo = '''.video-demo {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
  color: var(--text);
}'''
html = html.replace(old_video_demo, new_video_demo)

# Change video demo header title color
old_video_title = '''.video-demo-title {
  font-size: 1rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
}'''
new_video_title = '''.video-demo-title {
  font-size: 1rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text);
}'''
html = html.replace(old_video_title, new_video_title)

# Change badge to dark text
old_badge = '''.video-demo-badge {
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 0.65rem;
  font-weight: 700;
  background: rgba(74, 222, 128, 0.12);
  color: #4ade80;
  border: 1px solid rgba(74, 222, 128, 0.2);
}'''
new_badge = '''.video-demo-badge {
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 0.65rem;
  font-weight: 700;
  background: rgba(5, 150, 105, 0.08);
  color: var(--success);
  border: 1px solid rgba(5, 150, 105, 0.15);
}'''
html = html.replace(old_badge, new_badge)

# Change video demo player to smaller, white background
old_player = '''.video-demo-player {
  background: rgba(0, 0, 0, 0.3);
  border: 2px dashed rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  padding: 32px;
  text-align: center;
  margin-bottom: 14px;
}'''
new_player = '''.video-demo-player {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px;
  text-align: center;
  margin-bottom: 14px;
}'''
html = html.replace(old_player, new_player)

# Change video demo text to dark
old_video_text = '''.video-demo-text {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 14px;
}'''
new_video_text = '''.video-demo-text {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: 14px;
}'''
html = html.replace(old_video_text, new_video_text)

# Change video demo icon
old_video_icon = '''.video-demo-icon {
  font-size: 2.5rem;
  margin-bottom: 10px;
  color: var(--accent-light);
}'''
new_video_icon = '''.video-demo-icon {
  font-size: 1.5rem;
  margin-bottom: 8px;
  color: var(--accent);
}'''
html = html.replace(old_video_icon, new_video_icon)

# Change the YouTube link to embed iframe
old_video_content = '''<div class="video-demo-player">
        <div class="video-demo-icon">▶</div>
        <div class="video-demo-text">Autonomous Workflow Engine — PC-to-Android task execution</div>
        <a href="https://youtu.be/yAfvXZR69eY?si=4VnpACzK_T6NtFm-" target="_blank" class="video-demo-btn">
          <span>▶</span> Watch Demo
        </a>
      </div>'''

new_video_content = '''<div class="video-demo-player">
        <div class="video-demo-text">Autonomous Workflow Engine — PC-to-Android task execution</div>
        <iframe width="100%" height="280" src="https://www.youtube-nocookie.com/embed/yAfvXZR69eY" title="Autonomous Workflow Engine Demo" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen style="border-radius:8px;max-width:480px;margin:0 auto;display:block;"></iframe>
      </div>'''
html = html.replace(old_video_content, new_video_content)

# 5. Combine AI & Cloud with Local AI, add Hermes and OpenClaw
# Remove the separate Local AI card
old_local_ai = '''    <div class="card">
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

new_ai_cloud = '''    <div class="card">
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

# Remove old AI & Cloud
old_ai_cloud = '''    <div class="card">
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
      </div>
    </div>
    <div class="card">
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

html = html.replace(old_ai_cloud, new_ai_cloud)

# 6. Update Work & Education logos - add Moller and UC, fix Hermes
old_work_ed = '''    <!-- Work Logos -->
    <div class="card">
      <div class="card-title">Work & Education</div>
      <div class="logo-grid">
        <div class="logo-item">
          <img src="https://upload.wikimedia.org/wikipedia/commons/4/48/Dell_Logo.svg" alt="Dell" onerror="this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#007db8\\'>D</div>Dell'">
          Dell
        </div>
        <div class="logo-item">
          <img src="https://upload.wikimedia.org/wikipedia/commons/f/fb/Michigan_Wolverines_logo.svg" alt="Michigan" onerror="this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#ffcb05;color:#00274c\\'>M</div>Michigan'">
          Michigan
        </div>
        <div class="logo-item">
          <div class="logo-placeholder" style="background:#4f46e5">H</div>
          Hermes
        </div>
        <div class="logo-item">
          <img src="logo_openclaw.webp" alt="Claw" style="width:28px;height:28px;object-fit:contain;border-radius:6px;">
          Claw
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
      </div>
    </div>'''

html = html.replace(old_work_ed, new_work_ed)

# 7. Fix Personal Advisor to use "D" initial like others
old_advisor = '''        <li class="agent-item">
          <div>
            <div class="agent-name"><img src="logo_advisor.webp" alt="Personal Advisor" style="width:20px;height:20px;object-fit:cover;border-radius:50%;display:inline-block;vertical-align:middle;margin-right:8px;">Personal Advisor</div>
            <div class="agent-desc">Life & travel planning</div>
          </div>
          <span class="agent-status status-active">Active</span>
        </li>'''

new_advisor = '''        <li class="agent-item">
          <div>
            <div class="agent-name"><span class="agent-icon" style="background:#db2777">D</span>Donna</div>
            <div class="agent-desc">Personal Advisor — Life & travel planning</div>
          </div>
          <span class="agent-status status-active">Active</span>
        </li>'''

html = html.replace(old_advisor, new_advisor)

# 8. Remove duplicate Dell experience below Productivity
old_exp_left = '''    <!-- Experience -->
    <div class="card">
      <div class="card-title">Experience</div>
      <div class="exp-item">
        <div class="exp-company">Dell Technologies</div>
        <div class="exp-role">Sr. Advisor — AI/ML (2023–Present)</div>
        <div class="exp-desc">$16B Lead Price Plan (500K+ SKUs/LOC). Margin leakage to 0.3%.</div>
        <span class="exp-tag">AI/ML</span><span class="exp-tag">Pricing</span>
      </div>
    </div>

  </div>'''

new_exp_left = '''  </div>'''

html = html.replace(old_exp_left, new_exp_left)

# 9. Update bottom experience with all Moller positions
old_bottom_exp = '''    <div class="exp-card">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <img src="logo_moller.png" alt="Moller" style="width:24px;height:24px;object-fit:contain;">
        <div class="exp-company">Moller y Perez-Cotapos</div>
      </div>
      <div class="exp-role">Associate Manager — Real Estate (2012–2020)</div>
      <div class="exp-desc">Acquired $100M+ in assets. Led team of 7 analysts. +60% business unit profits. 22 new projects with investment funds.</div>
      <div><span class="exp-tag">Real Estate</span><span class="exp-tag">Leadership</span></div>
    </div>'''

new_moller_exp = '''    <div class="exp-card">
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

html = html.replace(old_bottom_exp, new_moller_exp)

# 10. Remove WhatsApp from footer
old_footer_whatsapp = '''    <a href="https://wa.me/17344507404" class="hero-contact-link" target="_blank" title="Send WhatsApp">
      <svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
      WhatsApp
    </a>'''

html = html.replace(old_footer_whatsapp, '')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done! Changes applied.")
