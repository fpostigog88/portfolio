with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Change main grid to stretch so all columns have same height
html = html.replace(
    '''.main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 0;
  display: grid;
  grid-template-columns: 280px 1fr 280px;
  gap: 16px;
  align-items: start;
}''',
    '''.main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 0;
  display: grid;
  grid-template-columns: 280px 1fr 280px;
  gap: 16px;
  align-items: stretch;
}'''
)

# 2. Center column also needs flex display
old_center_col = '''  <!-- CENTER COLUMN -->
  <div class="center-col">'''
new_center_col = '''  <!-- CENTER COLUMN -->
  <div class="center-col" style="display:flex;flex-direction:column;gap:16px;">'''
html = html.replace(old_center_col, new_center_col)

# 3. Remove margin-bottom from cards inside columns since gap handles it
html = html.replace(
    '''.project-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
  transition: all 0.2s;
}''',
    '''.project-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 0;
  transition: all 0.2s;
}'''
)

html = html.replace(
    '''.video-demo {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
  color: var(--text);
}''',
    '''.video-demo {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 0;
  color: var(--text);
}'''
)

# 4. Reduce project card padding to make them more compact
html = html.replace(
    '''.project-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 0;
  transition: all 0.2s;
}''',
    '''.project-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px 20px;
  margin-bottom: 0;
  transition: all 0.2s;
}'''
)

# 5. Reduce video demo padding
html = html.replace(
    '''.video-demo {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 0;
  color: var(--text);
}''',
    '''.video-demo {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 12px 16px;
  margin-bottom: 0;
  color: var(--text);
}'''
)

# 6. Reduce video player padding
html = html.replace(
    '''.video-demo-player {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px;
  text-align: center;
  margin-bottom: 14px;
}''',
    '''.video-demo-player {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 12px;
  text-align: center;
  margin-bottom: 0;
}'''
)

# 7. Reduce project desc margin
html = html.replace(
    '''.project-desc {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: 12px;
  line-height: 1.5;
}''',
    '''.project-desc {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: 0;
  line-height: 1.5;
}'''
)

# 8. Project title color to accent-dark
html = html.replace(
    '''.project-title {
  font-size: 1rem;
  font-weight: 700;
}''',
    '''.project-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--accent-dark);
}'''
)

# 9. Change "&" to "and" in agent panel title
html = html.replace(
    '<span><span class="agent-live"></span> 6-Agent AI Ecosystem</span>',
    '<span><span class="agent-live"></span> 6-Agent AI Ecosystem</span>'
)

# Actually, the agent panel title is "6-Agent AI Ecosystem" - let me check if there's an &
# Looking at the screenshot, the title shows "6-AGENT AI ECOSYSTEM" - no & in there
# But the user said "chnge the '&' to 'and'" - maybe they mean the Work & Education title?
# Let me change "Work & Education" to "Work and Education"
html = html.replace(
    '<div class="card-title">Work & Education</div>',
    '<div class="card-title">Work and Education</div>'
)

# 10. Center-align agent icon vertically with name and desc
# Change agent-name to align items center
html = html.replace(
    '''.agent-name {
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 2px;
}''',
    '''.agent-name {
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 2px;
}'''
)

# The agent-icon is already centered with flex. The issue might be that the agent-item uses align-items: flex-start
# Let me change it to align-items: center
html = html.replace(
    '''.agent-item {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid var(--border);
  font-size: 0.8rem;
}''',
    '''.agent-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid var(--border);
  font-size: 0.8rem;
}'''
)

# 11. Remove gap from agent-list to make it more compact
# Actually, the agent items already have padding. Let me reduce the agent-panel padding
html = html.replace(
    '''.agent-panel {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
}''',
    '''.agent-panel {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 0;
}'''
)

# 12. Make agent desc have less margin
html = html.replace(
    '''.agent-desc {
  font-size: 0.7rem;
  color: var(--text-muted);
  margin-left: 30px;
}''',
    '''.agent-desc {
  font-size: 0.7rem;
  color: var(--text-muted);
  margin-left: 30px;
  margin-top: 2px;
}'''
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done! Alignment, spacing, and color fixes applied.")
