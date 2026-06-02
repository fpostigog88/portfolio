import sys

with open('C:/Users/cadel/deep_council_final/es/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove GA script
old_ga = '<script async src="https://www.googletagmanager.com/gtag/js?id=G-QNWVGSNNHS"></script>\n<script>\n  window.dataLayer = window.dataLayer || [];\n  function gtag(){dataLayer.push(arguments);}\n  gtag(\'js\', new Date());\n  gtag(\'config\', \'G-QNWVGSNNHS\');\n</script>'
content = content.replace(old_ga, '<!-- Google Analytics removed -->')

# 2. Remove cookie banner
old_banner = '<div class="cookie-banner" id="cookie-banner">\n  <div class="cookie-banner-content">\n    <p>Este sitio usa Google Analytics para entender c\u00f3mo los visitantes encuentran el portafolio. <a href="https://policies.google.com/technologies/cookies" target="_blank">Saber m\u00e1s</a></p>\n    <div class="cookie-banner-actions">\n      <button class="cookie-btn cookie-btn-accept" onclick="acceptCookies()">Aceptar</button>\n      <button class="cookie-btn cookie-btn-dismiss" onclick="dismissCookies()">Rechazar</button>\n    </div>\n  </div>\n</div>\n</div>\n\n<!-- Cookie Consent Banner -->\n<div id="cookie-banner" class="cookie-banner cookie-hidden">\n  <p>This site uses Google Analytics to understand how visitors find the portfolio. <a href="https://policies.google.com/technologies/cookies" target="_blank">Learn more</a></p>\n  <div style="display:flex;gap:8px;">\n    <button class="cookie-btn cookie-btn-accept" onclick="acceptCookies()">Accept</button>\n    <button class="cookie-btn cookie-btn-dismiss" onclick="dismissCookies()">Decline</button>\n  </div>\n</div>\n\n<script>\n  // Cookie consent logic\n  function acceptCookies() {\n    localStorage.setItem(\'cookie_consent\', \'accepted\');\n    document.getElementById(\'cookie-banner\').classList.add(\'cookie-hidden\');\n  }\n  function dismissCookies() {\n    localStorage.setItem(\'cookie_consent\', \'declined\');\n    document.getElementById(\'cookie-banner\').classList.add(\'cookie-hidden\');\n  }\n  // Show banner if not yet decided\n  if (!localStorage.getItem(\'cookie_consent\')) {\n    document.getElementById(\'cookie-banner\').classList.remove(\'cookie-hidden\');\n  }\n</script>\n\n'
content = content.replace(old_banner, '\n')

# 3. Fix video
old_video = '<iframe src="https://www.youtube.com/embed/..." title="Demo de ejecuci\u00f3n de tareas PC-a-Android" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen=""></iframe>\n        </div>\n        <div class="video-demo-text">Demo de ejecuci\u00f3n de tareas PC-a-Android</div>'
new_video = '<iframe src="https://www.youtube.com/embed/..." title="Demo de ejecuci\u00f3n de tareas PC-a-Android" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen="" style="width:100%;height:300px;border:0;"></iframe>\n        </div>'
content = content.replace(old_video, new_video)

# 4. Fix CSS
content = content.replace('\n\n:root {', ':root {')
content = content.replace('    --bg: #faf9f7;', '  --bg: #faf9f7;')

# 5. Fix CSS - agent
old_agent_css = '.agent-name {\n  font-weight: 600;\n  display: flex;\n  align-items: center;\n  gap: 8px;\n  margin-bottom: 2px;\n}'
new_agent_css = '.agent-name {\n  font-weight: 600;\n  margin-bottom: 2px;\n}'
content = content.replace(old_agent_css, new_agent_css)

old_desc_css = '.agent-desc {\n  font-size: 0.7rem;\n  color: var(--text-muted);\n  margin-left: 30px;\n  margin-top: 2px;\n}'
new_desc_css = '.agent-desc {\n  font-size: 0.7rem;\n  color: var(--text-muted);\n  margin-top: 2px;\n}'
content = content.replace(old_desc_css, new_desc_css)

# 6. Change title
content = content.replace('Capacidades de Flujo de IA', 'Capacidades SMART')

# 7. Replace old agent list with new SMART layout
old_agents = '''      <ul class="agent-list">
        <li class="agent-item">
          <div class="agent-info">
            <div class="agent-name"><span class="agent-icon" style="background:#4f46e5">S</span>Coordinaci\u00f3n Sistemas</div>
            <div class="agent-desc">Supervisi\u00f3n, enrutamiento y confiabilidad</div>
          </div>
          <span class="agent-status status-active">Activo</span>
        </li>
        <li class="agent-item">
          <div class="agent-info">
            <div class="agent-name"><span class="agent-icon" style="background:#059669">F</span>An\u00e1lisis Financiero</div>
            <div class="agent-desc">Seguimiento, clasificaci\u00f3n, revisi\u00f3n anomal\u00edas</div>
          </div>
          <span class="agent-status status-active">Activo</span>
        </li>
        <li class="agent-item">
          <div class="agent-info">
            <div class="agent-name"><span class="agent-icon" style="background:#7c3aed">R</span>S\u00edntesis de Investigaci\u00f3n</div>
            <div class="agent-desc">Investigaci\u00f3n de mercado, t\u00e9cnica y estrat\u00e9gica</div>
          </div>
          <span class="agent-status status-active">Activo</span>
        </li>
        <li class="agent-item">
          <div class="agent-info">
            <div class="agent-name"><span class="agent-icon" style="background:#ea580c">A</span>Automatizaci\u00f3n Flujos</div>
            <div class="agent-desc">Ejecuci\u00f3n de tareas repetibles</div>
          </div>
          <span class="agent-status status-active">Activo</span>
        </li>
        <li class="agent-item">
          <div class="agent-info">
            <div class="agent-name"><span class="agent-icon" style="background:#0891b2">M</span>Monitoreo Mercado</div>
            <div class="agent-desc">Se\u00f1ales, briefings y listas de seguimiento</div>
          </div>
          <span class="agent-status status-active">Activo</span>
        </li>
        <li class="agent-item">
          <div class="agent-info">
            <div class="agent-name"><span class="agent-icon" style="background:#db2777">D</span>Soporte Decisiones</div>
            <div class="agent-desc">Prompts de planificaci\u00f3n y soporte siguiente paso</div>
          </div>
          <span class="agent-status status-active">Activo</span>
        </li>
      </ul>'''

new_agents = '''      <ul class="agent-list">
        <li class="agent-item">
          <div class="agent-info" style="display:flex;align-items:center;gap:8px;">
            <span class="agent-icon" style="background:#4f46e5">S</span>
            <div>
              <div class="agent-name">Coordinaci\u00f3n Sistemas</div>
              <div class="agent-desc">Supervisi\u00f3n, enrutamiento y confiabilidad</div>
            </div>
          </div>
          <span class="agent-status status-active">Activo</span>
        </li>
        <li class="agent-item">
          <div class="agent-info" style="display:flex;align-items:center;gap:8px;">
            <span class="agent-icon" style="background:#0891b2">M</span>
            <div>
              <div class="agent-name">Monitoreo Mercado</div>
              <div class="agent-desc">Se\u00f1ales, briefings y listas de seguimiento</div>
            </div>
          </div>
          <span class="agent-status status-active">Activo</span>
        </li>
        <li class="agent-item">
          <div class="agent-info" style="display:flex;align-items:center;gap:8px;">
            <span class="agent-icon" style="background:#ea580c">A</span>
            <div>
              <div class="agent-name">Automatizaci\u00f3n Flujos</div>
              <div class="agent-desc">Ejecuci\u00f3n de tareas repetibles</div>
            </div>
          </div>
          <span class="agent-status status-active">Activo</span>
        </li>
        <li class="agent-item">
          <div class="agent-info" style="display:flex;align-items:center;gap:8px;">
            <span class="agent-icon" style="background:#7c3aed">R</span>
            <div>
              <div class="agent-name">S\u00edntesis de Investigaci\u00f3n</div>
              <div class="agent-desc">Investigaci\u00f3n de mercado, t\u00e9cnica y estrat\u00e9gica</div>
            </div>
          </div>
          <span class="agent-status status-active">Activo</span>
        </li>
        <li class="agent-item">
          <div class="agent-info" style="display:flex;align-items:center;gap:8px;">
            <span class="agent-icon" style="background:#db2777">T</span>
            <div>
              <div class="agent-name">Soporte T\u00e1ctico de Decisiones</div>
              <div class="agent-desc">Prompts de planificaci\u00f3n y soporte siguiente paso</div>
            </div>
          </div>
          <span class="agent-status status-active">Activo</span>
        </li>
      </ul>'''

content = content.replace(old_agents, new_agents)

with open('C:/Users/cadel/deep_council_final/es/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done!')
