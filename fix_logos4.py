with open('portfolio_v2_light.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Direct replacements for remaining img tags
html = html.replace(
    '<img src="https://upload.wikimedia.org/wikipedia/commons/3/34/Microsoft_Office_Excel_%282019%E2%80%93present%29.svg" alt="Excel" onerror="this.style.display=\'none\';this.parentNode.innerHTML=\'<div class=\\\'logo-placeholder\\\' style=\\\'background:#217346\\\'>E</div>Excel\'\">',
    '<svg width="28" height="28" viewBox="0 0 24 24"><path d="M23 1.5q.41 0 .7.3.3.29.3.7v19q0 .41-.3.7-.29.3-.7.3H7q-.41 0-.7-.3-.3-.29-.3-.7V18H1q-.41 0-.7-.3-.3-.29-.3-.7V7q0-.41.3-.7.29-.3.7-.3h5V2.5q0-.41.3-.7.29-.3.7-.3zM6 13.28l1.48 1.36L11 11.18l.25.24 1.5 1.38 1.48-1.36L12.75 10l3.48-3.2L14.75 5.46 11 8.82 7.48 5.46 6 6.82l3.52 3.2z" fill="#217346"/></svg>'
)

html = html.replace(
    '<img src="https://upload.wikimedia.org/wikipedia/commons/0/0d/Microsoft_Office_PowerPoint_%282019%E2%80%93present%29.svg" alt="PPT" onerror="this.style.display=\'none\';this.parentNode.innerHTML=\'<div class=\\\'logo-placeholder\\\' style=\\\'background:#d24726\\\'>P</div>PPT\'\">',
    '<svg width="28" height="28" viewBox="0 0 24 24"><path d="M23 1.5q.41 0 .7.3.3.29.3.7v19q0 .41-.3.7-.29.3-.7.3H7q-.41 0-.7-.3-.3-.29-.3-.7V18H1q-.41 0-.7-.3-.3-.29-.3-.7V7q0-.41.3-.7.29-.3.7-.3h5V2.5q0-.41.3-.7.29-.3.7-.3zM6 13.28l1.48 1.36L11 11.18l.25.24 1.5 1.38 1.48-1.36L12.75 10l3.48-3.2L14.75 5.46 11 8.82 7.48 5.46 6 6.82l3.52 3.2z" fill="#d24726"/></svg>'
)

html = html.replace(
    '<img src="https://upload.wikimedia.org/wikipedia/commons/f/fd/Microsoft_Office_Word_%282019%E2%80%93present%29.svg" alt="Word" onerror="this.style.display=\'none\';this.parentNode.innerHTML=\'<div class=\\\'logo-placeholder\\\' style=\\\'background:#2b579a\\\'>W</div>Word\'\">',
    '<svg width="28" height="28" viewBox="0 0 24 24"><path d="M23 1.5q.41 0 .7.3.3.29.3.7v19q0 .41-.3.7-.29.3-.7.3H7q-.41 0-.7-.3-.3-.29-.3-.7V18H1q-.41 0-.7-.3-.3-.29-.3-.7V7q0-.41.3-.7.29-.3.7-.3h5V2.5q0-.41.3-.7.29-.3.7-.3zM6 13.28l1.48 1.36L11 11.18l.25.24 1.5 1.38 1.48-1.36L12.75 10l3.48-3.2L14.75 5.46 11 8.82 7.48 5.46 6 6.82l3.52 3.2z" fill="#2b579a"/></svg>'
)

html = html.replace(
    '<img src="https://upload.wikimedia.org/wikipedia/commons/4/4e/Docker_%28container_engine%29_logo.svg" alt="Docker" onerror="this.style.display=\'none\';this.parentNode.innerHTML=\'<div class=\\\'logo-placeholder\\\' style=\\\'background:#2496ed\\\'>Do</div>Docker\'\">',
    '<svg width="28" height="28" viewBox="0 0 24 24"><path d="M13.983 11.078h2.119a.186.186 0 00.186-.185V9.006a.186.186 0 00-.186-.186h-2.119a.185.185 0 00-.185.185v1.888c0 .102.083.185.185.185m-2.954-5.43h2.118a.186.186 0 00.186-.186V3.574a.186.186 0 00-.186-.185h-2.118a.185.185 0 00-.185.185v1.888c0 .102.082.185.185.186m-2.93 0h2.12a.186.186 0 00.184-.186V3.574a.185.185 0 00-.184-.185H8.1a.185.185 0 00-.185.185v1.888c0 .102.083.185.185.186m-2.964 0h2.119a.186.186 0 00.185-.186V3.574a.185.185 0 00-.185-.185H5.136a.186.186 0 00-.186.185v1.888c0 .102.084.185.186.186zm-2.93 5.43h2.12a.186.186 0 00.184-.185V9.006a.185.185 0 00-.184-.186h-2.12a.185.185 0 00-.184.185v1.888c0 .102.083.185.185.185m-2.964 0h2.119a.186.186 0 00.185-.185V9.006a.185.185 0 00-.184-.186h-2.12a.186.186 0 00-.185.186v1.887c0 .102.084.185.186.185m-2.92 0h2.12a.185.185 0 00.184-.185V9.006a.185.185 0 00-.184-.185h-2.12a.185.185 0 00-.184.185v1.888c0 .102.082.185.185.185M23.763 9.89c-.065-.051-.672-.51-1.954-.51-.338.001-.676.03-1.01.087-.248-1.7-1.653-2.53-1.716-2.566l-.344-.199-.226.327c-.284.438-.49.922-.612 1.43-.23.097-.912.365-2.357.615-.562.095-1.14.14-1.72.14-.084-.155-.168-.305-.254-.447-.652-1.075-1.586-1.828-2.72-2.18-.687-.22-1.38-.227-2.06-.02-.106-.597-.172-1.17-.172-1.71 0-4.48 4.58-8.9 11.16-8.9 6.58 0 11.16 4.42 11.16 8.9 0 3.74-2.37 6.6-4.8 8.3zm-7.64-1.3c-3.13.55-5.7 1.2-7.45 1.9-1.26 3.17-3.12 4.98-5.34 4.98-.92 0-1.75-.28-2.46-.83 2.1-.2 4.18-.93 6.2-2.24 2.02-1.3 3.5-2.8 4.4-4.42.45-.83.77-1.68.96-2.52 1.67-.2 3.47-.55 5.37-1.05 1.2 3.2 3.13 5.04 5.4 5.04.94 0 1.79-.3 2.51-.88-2.18.23-4.3.94-6.36 2.18-2.06 1.24-3.6 2.8-4.63 4.5z" fill="#2496ed"/></svg>'
)

# Replace Hermes, Claw, Fireworks placeholders with styled SVGs
HERMES_SVG = '<svg width="28" height="28" viewBox="0 0 24 24"><rect width="24" height="24" rx="6" fill="#4f46e5"/><text x="12" y="17" font-size="12" font-weight="700" text-anchor="middle" fill="white" font-family="Arial,sans-serif">H</text></svg>'
CLAW_SVG = '<svg width="28" height="28" viewBox="0 0 24 24"><rect width="24" height="24" rx="6" fill="#ea580c"/><text x="12" y="17" font-size="12" font-weight="700" text-anchor="middle" fill="white" font-family="Arial,sans-serif">C</text></svg>'
FIREWORKS_SVG = '<svg width="28" height="28" viewBox="0 0 24 24"><rect width="24" height="24" rx="6" fill="#ff4f00"/><text x="12" y="17" font-size="10" font-weight="700" text-anchor="middle" fill="white" font-family="Arial,sans-serif">F</text></svg>'

html = html.replace(
    '<div class="logo-placeholder" style="background:#4f46e5">H</div>',
    HERMES_SVG
)
html = html.replace(
    '<div class="logo-placeholder" style="background:#ea580c">C</div>',
    CLAW_SVG
)
html = html.replace(
    '<div class="logo-placeholder" style="background:#ff4f00">F</div>',
    FIREWORKS_SVG
)

with open('portfolio_v2_light.html', 'w', encoding='utf-8') as f:
    f.write(html)

remaining = html.count('logo-placeholder')
print(f'Done. Remaining logo-placeholder occurrences: {remaining}')
