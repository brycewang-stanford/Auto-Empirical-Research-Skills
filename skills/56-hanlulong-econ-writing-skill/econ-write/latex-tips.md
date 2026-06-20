# LaTeX Tips for Economics Papers

Practical LaTeX guidance for writing, formatting, and submitting economics papers.

## Document Structure

```latex
\documentclass[12pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{setspace}\doublespacing  % many journals require double or 1.5 spacing -- check target journal
\usepackage{amsmath,amssymb}
\usepackage{graphicx,float}
\usepackage{booktabs,threeparttable}
\usepackage{natbib}
\usepackage[hidelinks]{hyperref}
\usepackage{cleveref}
\usepackage{appendix}
```

## Essential Packages

| Package | Purpose |
|---------|---------|
| `amsmath` | Aligned equations, multi-line math |
| `booktabs` | Professional table rules |
| `threeparttable` | Table notes below tables |
| `natbib` | Author-year citations (economics standard) |
| `siunitx` / `dcolumn` | Decimal-aligned columns |
| `subcaption` | Subfigures (a), (b), etc. |
| `tikz` | Diagrams, game trees, timelines |
| `cleveref` | Smart cross-references |

## Table Formatting

**Use booktabs, never `\hline`.** Use `\toprule`, `\midrule`, `\bottomrule` and avoid vertical lines entirely.

**Regression tables** -- wrap in `threeparttable` for notes:

```latex
\begin{table}[t]
\begin{threeparttable}
\caption{Effect of X on Y}\label{tab:main}
\begin{tabular}{lcc}
\toprule
 & (1) & (2) \\
\midrule
Treatment & 0.45*** & 0.38** \\
 & (0.12) & (0.15) \\
Controls & No & Yes \\
Observations & 5,000 & 5,000 \\
\bottomrule
\end{tabular}
\begin{tablenotes}\small
\item \textit{Notes:} Standard errors in parentheses. *** p<0.01.
\end{tablenotes}
\end{threeparttable}
\end{table}
```

**Decimal alignment** with `siunitx`: use `S[table-format=1.3]` as the column type. For multi-panel tables, use `\midrule` to separate panels and label each with `\multicolumn`.

## Figure Formatting

- **Always use PDF** vector graphics, not PNG/JPG. Exception: photographs or maps.
- **Exporting from Stata:** `graph export fig.pdf, replace`. From R: `ggsave("fig.pdf", width=6, height=4)`. From Python: `plt.savefig("fig.pdf", bbox_inches="tight")`.
- **Subfigures** with `subcaption`:

```latex
\begin{figure}[t]
\begin{subfigure}{0.48\textwidth}
  \includegraphics[width=\linewidth]{fig_a.pdf}
  \caption{Pre-period}\label{fig:pre}
\end{subfigure}\hfill
\begin{subfigure}{0.48\textwidth}
  \includegraphics[width=\linewidth]{fig_b.pdf}
  \caption{Post-period}\label{fig:post}
\end{subfigure}
\caption{Event study results}\label{fig:event}
\end{figure}
```

- Keep all figures the same width (e.g., `width=0.9\textwidth` or a fixed `width=5in`) for visual consistency.

## Bibliography Management

**Use `natbib` with `\bibliographystyle{aer}` or `chicago`.** This gives author-year format: `\citet{FF1993}` produces "Fama and French (1993)" and `\citep{FF1993}` produces "(Fama and French, 1993)".

`biblatex` with `style=authoryear` is an alternative but less common in economics submissions. Check the target journal before choosing.

**Working papers:** include `note = {NBER Working Paper No.\ 12345}` in the bib entry. Update to the published version before submission.

## Math Formatting

- Use `equation` for single-line, `align` for multi-line. Avoid `eqnarray`.
- **Number only referenced equations:** use `\begin{equation*}` or `\nonumber` for unnumbered, and number only those you cite with `\eqref`.
- **Notation convention:** Latin letters for observables/variables ($Y$, $X$, $D$), Greek for parameters ($\beta$, $\gamma$, $\varepsilon$). Define notation on first use.

```latex
\begin{align}
Y_{it} &= \alpha + \beta D_{it} + \mathbf{X}_{it}'\gamma + \varepsilon_{it} \label{eq:main}
\end{align}
```

## Cross-Referencing

Label every table, figure, and equation. Use `\cref` from `cleveref` to auto-format:

```latex
\cref{tab:main}   % -> Table 1
\cref{fig:event}  % -> Figure 2
\cref{eq:main}    % -> eq. (1)
```

This avoids inconsistencies like "table 1" vs "Table 1" throughout the paper.

## Journal Submission Tips

| Journal | Key requirements |
|---------|-----------------|
| AER | 11pt or 12pt, 1.5 spacing, 1-inch margins; ~40-45 pp incl. everything; single-blind (names on page 1) |
| QJE | Similar to AER; online appendix as separate PDF |
| Econometrica | Own `ecta` document class; strict formatting |
| REStud | `restud` class available; figures at end |
| JPE | Chicago style bibliography; standard article class |

**Anonymous submissions:** remove author names and self-citations that reveal identity. Use `\thanks{}` sparingly. Add `\date{}` to suppress the date.

**Word counts:** run `texcount paper.tex` from the command line. Top-5 journals state length in pages, not words: AER ~40-45 pp (avg 35-36 typeset pp); Econometrica and REStud cap at 45 pp (12pt, 1.5 spacing); QJE and JPE set no hard limit. As a rough proxy a 40-page double-spaced manuscript is ~10,000 words -- but check each journal's current page-based guidelines.

**Online appendix:** create a separate file (`appendix.pdf`) with its own title page. Cross-reference from the main text: "see Online Appendix Table A1."

## Beamer Presentations

```latex
\documentclass{beamer}
\usetheme{metropolis}  % clean, modern
\setbeamertemplate{navigation symbols}{}  % remove nav clutter
```

- One idea per slide. Use `\pause` sparingly.
- Label backup slides after `\appendix` with a "Backup Slides" frame.
- Use `\hyperlink{backup1}{\beamerbutton{Detail}}` to link to backup slides from the main presentation.

## Common Pitfalls

- **Floats landing far from text:** use `[t]` or `[!htbp]`, or `\usepackage{float}` with `[H]` as a last resort. Placing all tables/figures at the end avoids this for submissions.
- **Overfull boxes:** check the log for warnings. Use `\resizebox{\textwidth}{!}{...}` for wide tables, or reduce font with `\small` inside the tabular.
- **Tables too wide:** restructure the table (fewer columns, abbreviate headers) rather than shrinking to illegible sizes. Split into panels if needed.
- **Missing references:** run BibTeX/Biber, then LaTeX twice. Use `latexmk -pdf` to automate the build chain.
