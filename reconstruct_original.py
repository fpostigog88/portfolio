with open('portfolio_v2_light.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix corrupted img tags with duplicate content
# The pattern is: onerror="...">D</div>Dell'">D</div>Dell'">
# We need to restore to: onerror="...">Dell

# Fix Dell
html = html.replace(
    "onerror=\"this.style.display='none';this.parentNode.innerHTML='<div class='logo-placeholder' style='background:#007db8'>D</div>Dell'\">D</div>Dell'\">",
    "onerror=\"this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#007db8\\'>D</div>Dell'\">"
)

# Fix Michigan
html = html.replace(
    "onerror=\"this.style.display='none';this.parentNode.innerHTML='<div class='logo-placeholder' style='background:#ffcb05;color:#00274c'>M</div>Michigan'\">M</div>Michigan'\">",
    "onerror=\"this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#ffcb05;color:#00274c\\'>M</div>Michigan'\">"
)

# Fix OpenAI
html = html.replace(
    "onerror=\"this.style.display='none';this.parentNode.innerHTML='<div class='logo-placeholder' style='background:#10a37f'>O</div>OpenAI'\">O</div>OpenAI'\">",
    "onerror=\"this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#10a37f\\'>O</div>OpenAI'\">"
)

# Fix Claude
html = html.replace(
    "onerror=\"this.style.display='none';this.parentNode.innerHTML='<div class='logo-placeholder' style='background:#cc785c'>C</div>Claude'\">C</div>Claude'\">",
    "onerror=\"this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#cc785c\\'>C</div>Claude'\">"
)

# Fix PowerBI
html = html.replace(
    "onerror=\"this.style.display='none';this.parentNode.innerHTML='<div class='logo-placeholder' style='background:#f2c811;color:#000'>P</div>PowerBI'\">P</div>PowerBI'\">",
    "onerror=\"this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#f2c811;color:#000\\'>P</div>PowerBI'\">"
)

# Fix Excel
html = html.replace(
    "onerror=\"this.style.display='none';this.parentNode.innerHTML='<div class='logo-placeholder' style='background:#217346'>E</div>Excel'\">E</div>Excel'\">",
    "onerror=\"this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#217346\\'>E</div>Excel'\">"
)

# Fix PPT
html = html.replace(
    "onerror=\"this.style.display='none';this.parentNode.innerHTML='<div class='logo-placeholder' style='background:#d24726'>P</div>PPT'\">P</div>PPT'\">",
    "onerror=\"this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#d24726\\'>P</div>PPT'\">"
)

# Fix Word
html = html.replace(
    "onerror=\"this.style.display='none';this.parentNode.innerHTML='<div class='logo-placeholder' style='background:#2b579a'>W</div>Word'\">W</div>Word'\">",
    "onerror=\"this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#2b579a\\'>W</div>Word'\">"
)

# Fix Python
html = html.replace(
    "onerror=\"this.style.display='none';this.parentNode.innerHTML='<div class='logo-placeholder' style='background:#3776ab'>Py</div>Python'\">Py</div>Python'\">",
    "onerror=\"this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#3776ab\\'>Py</div>Python'\">"
)

# Fix Linux
html = html.replace(
    "onerror=\"this.style.display='none';this.parentNode.innerHTML='<div class='logo-placeholder' style='background:#fcc624;color:#000'>L</div>Linux'\">L</div>Linux'\">",
    "onerror=\"this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#fcc624;color:#000\\'>L</div>Linux'\">"
)

# Fix Windows
html = html.replace(
    "onerror=\"this.style.display='none';this.parentNode.innerHTML='<div class='logo-placeholder' style='background:#0078d4'>W</div>Windows'\">W</div>Windows'\">",
    "onerror=\"this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#0078d4\\'>W</div>Windows'\">"
)

# Fix SQLite
html = html.replace(
    "onerror=\"this.style.display='none';this.parentNode.innerHTML='<div class='logo-placeholder' style='background:#003b57'>SQL</div>SQLite'\">SQL</div>SQLite'\">",
    "onerror=\"this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#003b57\\'>SQL</div>SQLite'\">"
)

# Fix Docker
html = html.replace(
    "onerror=\"this.style.display='none';this.parentNode.innerHTML='<div class='logo-placeholder' style='background:#2496ed'>Do</div>Docker'\">Do</div>Docker'\">",
    "onerror=\"this.style.display='none';this.parentNode.innerHTML='<div class=\\'logo-placeholder\\' style=\\'background:#2496ed\\'>Do</div>Docker'\">"
)

with open('portfolio_v2_light.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Fixed corrupted file')
