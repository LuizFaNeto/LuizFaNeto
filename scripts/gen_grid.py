#!/usr/bin/env python3
"""Gera assets/contributions-dark.svg a partir da GraphQL API do GitHub.

Uso: gh api graphql -f query='...' > contrib.json && python3 gen_grid.py contrib.json
Chamado pelo workflow .github/workflows/contributions.yml (cron diário).
"""
import json
import sys

colors = ['#161b22', '#0e4429', '#006d32', '#26a641', '#39d353']  # tema dark do GitHub
CELL, GAP, PAD = 11, 3, 8
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def main() -> None:
    d = json.load(open(sys.argv[1]))
    weeks = d['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
    w, h = len(weeks), 7
    W = PAD * 2 + w * (CELL + GAP) - GAP
    H = PAD * 2 + 20 + h * (CELL + GAP) - GAP + 14
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    svg.append(f'<rect width="{W}" height="{H}" fill="#0d1117" rx="6"/>')
    for wi, week in enumerate(weeks):
        m = int(week['contributionDays'][0]['date'][5:7])
        prev = int(weeks[wi - 1]['contributionDays'][0]['date'][5:7]) if wi else None
        if wi == 0 or (prev is not None and prev != m):
            x = PAD + wi * (CELL + GAP)
            svg.append(f'<text x="{x}" y="{PAD + 11}" fill="#8b949e" font-family="monospace" font-size="10">{months[m - 1]}</text>')
    for r, label in [(1, 'Mon'), (3, 'Wed'), (5, 'Fri')]:
        y = PAD + 20 + r * (CELL + GAP) + CELL - 2
        svg.append(f'<text x="{PAD - 2}" y="{y}" fill="#8b949e" font-family="monospace" font-size="9" text-anchor="end">{label}</text>')
    for wi, week in enumerate(weeks):
        for di, day in enumerate(week['contributionDays']):
            x = PAD + wi * (CELL + GAP)
            y = PAD + 20 + di * (CELL + GAP)
            c = day['contributionCount']
            svg.append(
                f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" '
                f'fill="{colors[min(c, 4)]}"><title>{day["date"]}: {c} contribuições</title></rect>'
            )
    svg.append('</svg>')
    with open('assets/contributions-dark.svg', 'w') as f:
        f.write('\n'.join(svg) + '\n')
    print(f'ok: {W}x{H}, {sum(len(x["contributionDays"]) for x in weeks)} dias')


if __name__ == '__main__':
    main()
