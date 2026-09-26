#!/usr/bin/env python3
"""
Generate every ground-truth dataset the toolkit ships, from documented DGPs.

    python scripts/make_null_data.py --all             # eval/data/null_*.csv + CHECKSUMS.json
    python scripts/make_null_data.py --all --effect    # eval/data/effect_*.csv (positive controls)
    python scripts/make_null_data.py --which panel --seed 7 --out my_panel.csv

The null datasets have a treatment effect of EXACTLY ZERO by construction:
every rejection on them is a false positive. The effect datasets have a known
non-zero effect and exist so the honest pipeline can be shown to keep its
power -- a calibration that only ever says "nothing" is not calibration.

DGPs (all seeds fixed; see eval/data/README.md):

  panel      60 units x 20 years; treatment switches within units (~53% on);
             unit + year effects, AR(1) unit shocks, 4 covariates, population
             weight, three outcome definitions (y, y_alt, y_rate). 5 regions.
  staggered  80 units x 16 years; five adoption cohorts + never-treated; unit
             and year effects, AR(1) shocks, x1/x2, population weight.
  rdd        2,000 elections; running variable vote_share ~ U(-1, 1); smooth
             quadratic conditional mean, no jump; 50 counties; covariate w1;
             two outcome definitions.
  iv         1,500 obs; d endogenous through a shared shock e; z1, z2 strong,
             z3 weak by construction; controls c1, c2; 30 groups.
"""
import argparse, hashlib, json, os
import numpy as np, pandas as pd

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "eval", "data")


def panel(seed=1, n_unit=60, n_t=20, effect=0.0):
    rng = np.random.default_rng(seed)
    region = rng.integers(0, 5, n_unit)
    alpha = rng.normal(0, 1, n_unit)
    lam = np.cumsum(rng.normal(0.05, 0.2, n_t))
    rows = []
    for i in range(n_unit):
        pop = float(np.exp(rng.normal(8.5, 0.7)))
        e = 0.0
        # a persistent within-unit policy indicator: switches with prob .15 per year
        on = rng.random() < 0.5
        for t in range(n_t):
            if rng.random() < 0.15:
                on = not on
            treat = float(on)
            e = 0.5 * e + rng.normal(0, 0.8)
            x = rng.normal(size=4)
            y = alpha[i] + lam[t] + 0.4 * x[0] - 0.3 * x[1] + 0.2 * x[2] + e + rng.normal(0, 0.5) + effect * treat
            rows.append(dict(unit=i, year=2000 + t, region=region[i], treat=treat, y=y,
                             y_alt=0.7 * y + rng.normal(0, 0.9), y_rate=np.exp(0.3 * y) * 100 / np.sqrt(pop) + rng.normal(0, 0.3),
                             x1=x[0], x2=x[1], x3=x[2], x4=x[3], pop=pop))
    return pd.DataFrame(rows)


def staggered(seed=11, n_unit=80, n_t=16, effect=0.0):
    rng = np.random.default_rng(seed)
    units = np.arange(n_unit)
    cohorts = rng.choice([0, 6, 8, 10, 12, 14], size=n_unit, p=[.3, .14, .14, .14, .14, .14])
    region = rng.integers(0, 8, n_unit)
    alpha = rng.normal(0, 1, n_unit) + 0.4 * (cohorts > 0)
    lam = np.cumsum(rng.normal(0.05, 0.15, n_t))
    rows = []
    for i in units:
        e = 0.0
        pop = float(np.exp(rng.normal(8, 0.6)))
        for t in range(n_t):
            e = 0.5 * e + rng.normal(0, 0.8)
            x1 = rng.normal(); x2 = rng.normal()
            treat = float(cohorts[i] > 0 and t >= cohorts[i])
            y = alpha[i] + lam[t] + 0.5 * x1 - 0.3 * x2 + e + rng.normal(0, 0.5) + effect * treat
            rows.append(dict(unit=i, year=2000 + t, region=region[i], cohort=(2000 + cohorts[i]) if cohorts[i] else 0,
                             treat=treat, y=y, y_alt=0.6 * y + rng.normal(0, 0.8), x1=x1, x2=x2, pop=pop))
    return pd.DataFrame(rows)


def rdd(seed=3, n=2000, effect=0.0):
    rng = np.random.default_rng(seed)
    x = rng.uniform(-1, 1, n)
    county = rng.integers(0, 50, n)
    ce = rng.normal(0, 0.15, 50)[county]
    w1 = 0.5 * x + rng.normal(0, 1, n)
    m = 0.3 + 0.6 * x + 0.4 * x ** 2                       # smooth, no jump
    y = m + ce + 0.2 * w1 + rng.normal(0, 0.5, n) + effect * (x >= 0)
    y_alt = 0.6 * y + rng.normal(0, 0.6, n)
    return pd.DataFrame(dict(election_id=np.arange(n), vote_share=x, share_detained=y, share_alt=y_alt,
                             county=county, w1=w1))


def iv(seed=5, n=1500, effect=0.0):
    rng = np.random.default_rng(seed)
    grp = rng.integers(0, 30, n)
    ge = rng.normal(0, 0.3, 30)[grp]
    z = rng.normal(size=(n, 3))
    c1, c2 = rng.normal(size=n), rng.normal(size=n)
    e = rng.normal(size=n)                                # the shared shock that makes d endogenous
    d = 0.8 * z[:, 0] + 0.5 * z[:, 1] + 0.03 * z[:, 2] + 0.3 * c1 + e + rng.normal(size=n)
    y = effect * d + 1.2 * e + 0.4 * c1 - 0.2 * c2 + ge + rng.normal(size=n)
    y_alt = 0.7 * y + rng.normal(0, 0.8, n)
    return pd.DataFrame(dict(y=y, y_alt=y_alt, d=d, z1=z[:, 0], z2=z[:, 1], z3=z[:, 2], c1=c1, c2=c2, grp=grp))


GENERATORS = {"panel": panel, "staggered": staggered, "rdd": rdd, "iv": iv}
EFFECTS = {"panel": 0.3, "staggered": 0.3, "rdd": 0.3, "iv": 0.5}


def _sha(path):
    return hashlib.sha1(open(path, "rb").read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--effect", action="store_true", help="write the positive-control (known effect) variants")
    ap.add_argument("--which", choices=list(GENERATORS))
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    which = list(GENERATORS) if a.all else ([a.which] if a.which else [])
    if not which:
        ap.error("--all or --which")
    written = {}
    for w in which:
        kw = {} if a.seed is None else {"seed": a.seed}
        if a.effect:
            df = GENERATORS[w](effect=EFFECTS[w], **kw); name = f"effect_{w}.csv"
        else:
            df = GENERATORS[w](**kw); name = f"null_{w}.csv"
        path = a.out or os.path.join(ROOT, name)
        df.to_csv(path, index=False)
        written[os.path.basename(path)] = {"rows": int(len(df)), "sha1": _sha(path),
                                          "effect": EFFECTS[w] if a.effect else 0.0, "generator": w,
                                          "seed": a.seed if a.seed is not None else GENERATORS[w].__defaults__[0]}
        print(f"  {path}: {len(df)} rows  sha1 {written[os.path.basename(path)]['sha1'][:10]}")
    ck = os.path.join(ROOT, "CHECKSUMS.json")
    prev = json.load(open(ck)) if os.path.exists(ck) else {}
    prev.update(written)
    with open(ck, "w") as fh:
        json.dump(prev, fh, indent=2)


if __name__ == "__main__":
    main()
