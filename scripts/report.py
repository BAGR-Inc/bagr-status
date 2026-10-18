#!/usr/bin/env python3
"""Append this round to history/YYYY-MM.csv and rewrite STATUS.md (uptime %)."""
import csv, datetime as dt, glob, os, sys
rows = [l.strip().split('|') for l in sys.stdin if l.strip()]
now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
os.makedirs('history', exist_ok=True)
path = f'history/{now:%Y-%m}.csv'
new = not os.path.exists(path)
with open(path, 'a', newline='') as f:
    w = csv.writer(f)
    if new: w.writerow(['utc', 'check', 'state', 'http', 'seconds'])
    for name, state, code, secs in rows: w.writerow([now.isoformat(), name, state, code, secs])
# uptime over the last 24 h, 7 d and 30 d, from every CSV
hist = []
for p in sorted(glob.glob('history/*.csv')):
    with open(p) as f:
        for r in csv.DictReader(f):
            hist.append((dt.datetime.fromisoformat(r['utc']), r['check'], r['state']))
def pct(name, days):
    since = now - dt.timedelta(days=days)
    xs = [s for t, n, s in hist if n == name and t >= since]
    return '—' if not xs else f"{100 * sum(s == 'up' for s in xs) / len(xs):.3f}%"
names = [r[0] for r in rows]
state = {r[0]: r for r in rows}
lines = ['# BAGR status', '', f'Last check: {now:%Y-%m-%d %H:%M} UTC (every 5 minutes, from GitHub, outside our servers).', '',
         '| Check | Now | Last 24 h | Last 7 days | Last 30 days |', '|---|---|---|---|---|']
for n in names:
    s = state[n]
    now_s = 'up' if s[1] == 'up' else f'**DOWN** (HTTP {s[2]})'
    lines.append(f'| {n} | {now_s} | {pct(n, 1)} | {pct(n, 7)} | {pct(n, 30)} |')
lines += ['', 'Five nines (99.999%) allows 5 minutes down per year; 99.9% allows 8.8 hours.',
          'A check runs every 5 minutes, so one failed round counts as about 5 minutes down.']
open('STATUS.md', 'w').write('\n'.join(lines) + '\n')
