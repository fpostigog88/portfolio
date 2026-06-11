# Language switch fix

Implemented fully offline.

Behavior:
- First visit to `/` from a Spanish-language browser redirects to `/es/`.
- English/non-Spanish browsers stay on `/`.
- Language buttons set `localStorage.preferredLanguage` and a `preferredLanguage` cookie.
- Once a visitor clicks EN or ES, the homepage redirect respects that choice and does not force Spanish-browser users back to `/es/`.
- `/es/` never redirects English-browser users away; users can switch manually using buttons.
