<!-- preamble: parameter database check -->
After the update check, verify the parameter database is available and check staleness:

```bash
PARAMS_DIR="$HOME/econstack-data/parameters"
if [ -d "$PARAMS_DIR" ]; then
  PARAM_COUNT=$(find "$PARAMS_DIR" -name "*.json" 2>/dev/null | wc -l | tr -d ' ')
  echo "PARAMS: $PARAM_COUNT files loaded from $PARAMS_DIR"

  # Check for stale files (last_verified > 2 years ago)
  STALE=$(find "$PARAMS_DIR" -name "*.json" -mtime +730 2>/dev/null | wc -l | tr -d ' ')
  if [ "$STALE" -gt 0 ]; then
    echo "PARAMS_WARNING: $STALE file(s) not updated in 2+ years. Run: cd ~/econstack-data && git pull"
  fi
else
  echo "PARAMS: not found. Using built-in defaults. For full parameter support: git clone https://github.com/charlescoverdale/econstack-data.git ~/econstack-data"
fi
```

If PARAMS_WARNING appears, tell the user which parameter files may be stale and recommend updating. Continue with the skill normally using whatever parameters are available.