"""Code-scan signals fire on Stata, R and StatsPAI idioms, and their disclosure counterparts."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from phack import score

STATA_HACK = """
foreach bw in 0.5 0.75 1 1.5 2 {
    foreach k in triangular uniform {
        rdrobust y x, h(`bw') kernel(`k')
        if e(pv_rb) < .05 estimates store m_`bw'_`k'
    }
}
levelsof spec, local(specs)
foreach s of local specs {
    reghdfe y treat `ctl', absorb(unit year) vce(cluster region)
    test treat
    if r(p) < 0.05 post `h' (`s') (_b[treat]) (r(p))
}
gsort pval
keep if pval < .05
"""
R_HACK = """
grid <- expand.grid(bw = c(.5, 1, 2), kernel = c("triangular", "uniform"), controls = c(TRUE, FALSE))
res <- purrr::map_dfr(seq_len(nrow(grid)), function(i) broom::tidy(rdrobust::rdrobust(y, x, h = grid$bw[i])))
best <- res %>% filter(p.value < 0.05) %>% arrange(p.value) %>% slice(1)
"""
SP_HACK = """
fits = [sp.rdrobust(df, y="y", x="x", h=h, kernel=k) for h in hs for k in kernels]
best = min(fits, key=lambda r: r.pvalue)
"""
STATA_HONEST = "rwolf y, indepvar(treat) method(reghdfe) reps(500)\n* we report all 24 specifications; spec curve in appendix"
R_HONEST = "library(specr)\nres$p_adj <- p.adjust(res$p.value, method = 'holm')"
SP_HONEST = "sp.spec_curve(data_path='d.csv', y='y', x='treat', controls=[[], ['x1']])\nsp.romano_wolf(...)"


def _names(text, kind):
    return {h["signal"] for h in score.scan_code(text)[kind]}


def test_stata_hack_signals():
    n = _names(STATA_HACK, "search_signals")
    assert {"stata_spec_loop", "stata_selects_on_p", "stata_bandwidth_sweep"} <= n


def test_r_hack_signals():
    n = _names(R_HACK, "search_signals")
    assert {"r_spec_grid", "r_map_over_specs", "r_selects_on_p"} <= n


def test_statspai_hack_signals():
    n = _names(SP_HACK, "search_signals")
    assert "statspai_selects_best" in n


def test_disclosure_signals_per_language():
    assert "stata_multiplicity" in _names(STATA_HONEST, "disclosure_signals")
    assert "r_multiplicity" in _names(R_HONEST, "disclosure_signals")
    assert "statspai_multiplicity" in _names(SP_HONEST, "disclosure_signals")


def test_hack_scores_above_honest_in_every_language():
    for hack, honest in ((STATA_HACK, STATA_HONEST), (R_HACK, R_HONEST), (SP_HACK, SP_HONEST)):
        assert score.scan_code(hack)["raw_code_score"] > score.scan_code(honest)["raw_code_score"]
