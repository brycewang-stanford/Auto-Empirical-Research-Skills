"""Shared numeric-check protocol for AER-Skills example demos.

Every demo is also a regression test: it pins an estimate to a *known* target —
a Monte Carlo truth, a coverage rate, or a published number — and fails if the
estimate drifts outside a stated tolerance. This helper makes that contract
uniform and machine-checkable. Each call

  * asserts the check (so the demo exits non-zero on a wrong answer), and
  * prints one parseable line:

        NUMERIC-CHECK | <name> | got=<value> | <spec> | PASS|FAIL

`scripts/run_example_smoke.py` parses those lines and fails a demo that emits no
checks (so the assertions cannot silently rot into a no-op that still exits 0)
or that emits a FAIL. The economics analogue of an L1-tolerance replication
gate: "runs" is not enough; the answer must be numerically correct.

Demos import this from the examples/ root:

    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
    from _aer_numeric_check import numeric_check

Usage:

    numeric_check("Oster beta*(delta=1)", beta_star, target=0.0, tol=0.03)
    numeric_check("honest-DiD coverage at M=1", cov, lo=0.94)
    numeric_check("naive rejection rate", rate, lo=0.10, hi=1.0)
"""

from __future__ import annotations

PROTOCOL_PREFIX = "NUMERIC-CHECK"
_EPS = 1e-12


def numeric_check(
    name: str,
    got: float,
    *,
    target: float | None = None,
    tol: float | None = None,
    lo: float | None = None,
    hi: float | None = None,
) -> float:
    """Assert ``got`` matches a target within ``tol`` (or lies in [lo, hi]) and
    emit the standardized protocol line. Raises AssertionError on failure."""
    got = float(got)
    if target is not None:
        if tol is None:
            raise ValueError("numeric_check: 'target' requires 'tol'")
        ok = abs(got - target) <= tol + _EPS
        spec = f"target={target:g} tol={tol:g}"
    else:
        if lo is None and hi is None:
            raise ValueError("numeric_check: pass either target+tol or lo/hi")
        ok = True
        parts: list[str] = []
        if lo is not None:
            ok = ok and got >= lo - _EPS
            parts.append(f">={lo:g}")
        if hi is not None:
            ok = ok and got <= hi + _EPS
            parts.append(f"<={hi:g}")
        spec = " ".join(parts)
    status = "PASS" if ok else "FAIL"
    print(f"{PROTOCOL_PREFIX} | {name} | got={got:.4f} | {spec} | {status}", flush=True)
    if not ok:
        raise AssertionError(f"numeric check failed: {name}: got {got:.4f}, expected {spec}")
    return got
