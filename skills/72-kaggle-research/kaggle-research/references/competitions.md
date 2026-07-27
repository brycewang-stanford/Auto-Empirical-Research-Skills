# Competitions

Competition list, files, leaderboard, and submission-history reads are useful
for reproducible context:

```bash
python scripts/kaggle_research.py run -- competitions list -s "topic" -v
python scripts/kaggle_research.py run -- competitions files -c competition-ref -v
```

Joining a competition, accepting rules, or submitting predictions can create
legal, quota, or public-account effects. Verify the competition rules and ask
for explicit authorization before those actions. Preview submissions with
`--dry-run --allow-write`; execute only after the user confirms the exact
competition, file, and message.

Never fabricate a submission result. Preserve the returned submission ID,
status, score visibility, timestamp, and redacted audit artifact.
