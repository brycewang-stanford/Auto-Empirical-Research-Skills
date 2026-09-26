# p-hacking-skills

A specification-search audit and p-hacking benchmark for econometric
designs. It can perform a search — on known-zero data, a realistic search
manufactures p < .05 in a median of about a second
([the measured tables](capability.md)) — and it always shows what the
search was worth — see
[Responsible use](https://github.com/brycewang-stanford/p-hacking-skills/blob/main/RESPONSIBLE_USE.md).

!!! warning "Intended use"
    This tool is for academic research on and teaching about p-hacking, and
    for evaluating whether AI research agents p-hack. It is **not** meant to
    be used in real paper writing or research projects. Every search it runs
    leaves a complete ledger and a null-calibrated honest p-value; if you
    want to p-hack a real analysis, it will tell on you, by design.

- **How fast can an agent p-hack** — the capability, measured: seconds to
  significance and false-positive rate per search procedure, per design.
- **Concepts** — the ledger contract, the honest p-value, search procedures,
  pathology flags.
- **Tutorial** — from a dataset to a card, a search, a report and a
  third-party verification, in Python or your own language.
- **Ledger schema** and **Language map** — the two contracts other tools can
  target.
- **Verification and benchmark versions** — how a run becomes evidence.

```bash
pip install phack            # or: pip install -e . from a clone
phack init data.dta --design did --treatment policy --outcome lnwage
phack size data_card.json
phack search data.dta data_card.json --direction + --null-draws 200 --n-jobs 6 --summary
phack race data.dta data_card.json --direction + --budget 60 --null-scheme cluster_permute --summary
phack verify phack_out/
```
