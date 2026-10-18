# bagr-status

An uptime monitor for BAGR that runs **outside our servers**: GitHub Actions
checks every service every 5 minutes (`.github/workflows/monitor.yml`, list in
`scripts/checks.txt`).

- **Live numbers:** [`STATUS.md` on the `data` branch](../../blob/data/STATUS.md) — up/down now and uptime % for 24 h, 7 and 30 days.
- **History:** `history/YYYY-MM.csv` on the `data` branch, one row per check per round.
- **Alerts:** two failed rounds in a row open an issue titled `DOWN: <check>`
  (assigned to the repo variable `ALERT_TO`, so GitHub emails that person);
  the issue closes itself when the check answers again.
- A failed check is retried once after 20 s before it counts.

Public on purpose: Actions minutes are free on public repos. It holds only
public hostnames; the API key it sends is the app's public anon key, kept as
the repo secret `SUPABASE_ANON_KEY` anyway.

Limits: GitHub may start a scheduled run several minutes late when it is busy,
and pauses schedules in a repo with no activity for 60 days (the `data`
commits count as activity).
