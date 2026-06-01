import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Make left column even wider - 320px
html = html.replace(
    'grid-template-columns: 300px 1fr 280px;',
    'grid-template-columns: 320px 1fr 260px;'
)

# 2. Make logo items bigger in left column
html = html.replace(
    '.logo-item {\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  gap: 6px;\n  padding: 12px 4px;\n  background: var(--bg-elevated);\n  border: 1px solid var(--border);\n  border-radius: 8px;\n  font-size: 0.65rem;\n  font-weight: 600;\n  color: var(--text-secondary);\n  transition: all 0.2s;\n  text-align: center;\n}',
    '.logo-item {\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  gap: 6px;\n  padding: 14px 4px;\n  background: var(--bg-elevated);\n  border: 1px solid var(--border);\n  border-radius: 8px;\n  font-size: 0.65rem;\n  font-weight: 600;\n  color: var(--text-secondary);\n  transition: all 0.2s;\n  text-align: center;\n  min-height: 64px;\n  justify-content: center;\n}'
)

# Make logo images bigger
html = html.replace(
    '.logo-item img {\n  width: 28px;\n  height: 28px;\n  object-fit: contain;\n}',
    '.logo-item img {\n  width: 32px;\n  height: 32px;\n  object-fit: contain;\n}'
)

# 3. Remove project metrics from both project cards
# Remove metrics from Autonomous Workflow
old_aw_metrics = '''      <div class="project-metrics">
        <div class="project-metric"><span class="project-metric-value">Automation</span> • Android • Workflow • Execution</div>
      </div>
      <div class="project-links">'''

# But we already removed project-links. Let me find what's currently there
old_aw = '''    <div class="project-card">
      <div class="project-header">
        <div class="project-title">⚙️ Autonomous Workflow Engine</div>
        <span class="project-badge badge-green">Production</span>
      </div>
      <div class="project-desc">From PC orchestration to Android task execution. Automates repeatable mobile workflows using ADB control, scheduling logic, and execution monitoring.</div>
      <div class="project-metrics">
        <div class="project-metric"><span class="project-metric-value">Automation</span> • Android • Workflow • Execution</div>
      </div>
    </div>'''

new_aw = '''    <div class="project-card">
      <div class="project-header">
        <div class="project-title">⚙️ Autonomous Workflow Engine</div>
        <span class="project-badge badge-green">Production</span>
      </div>
      <div class="project-desc">From PC orchestration to Android task execution. Automates repeatable mobile workflows using ADB control, scheduling logic, and execution monitoring.</div>
    </div>'''

html = html.replace(old_aw, new_aw)

# Remove metrics from FinanceApp
old_fa = '''    <div class="project-card">
      <div class="project-header">
        <div class="project-title">💰 FinanceApp</div>
        <span class="project-badge badge-green">Production</span>
      </div>
      <div class="project-desc">Personal finance intelligence with Plaid integration, automated categorization, anomaly detection, multi-bank aggregation. Encrypted local storage.</div>
      <div class="project-metrics">
        <div class="project-metric"><span class="project-metric-value">Multi-bank</span> sync</div>
        <div class="project-metric"><span class="project-metric-value">Anomaly</span> detection</div>
        <div class="project-metric"><span class="project-metric-value">Fernet</span> encrypted</div>
      </div>
    </div>'''

new_fa = '''    <div class="project-card">
      <div class="project-header">
        <div class="project-title">💰 FinanceApp</div>
        <span class="project-badge badge-green">Production</span>
      </div>
      <div class="project-desc">Personal finance intelligence with Plaid integration, automated categorization, anomaly detection, multi-bank aggregation. Encrypted local storage.</div>
    </div>'''

html = html.replace(old_fa, new_fa)

# 4. Make sure all 5 Work & Education logos are same size by ensuring consistent styling
# The logo-item style already applies. Let's just make sure the GitHub logo uses same size

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done! Final fixes applied.")
