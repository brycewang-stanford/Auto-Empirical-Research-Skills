# LaTeX Support Reference

## Detection Strategy

Analyze .tex files for complexity using these metrics:

### Math Environments Count
- Inline: `$...$`
- Display: `\[...\]`, `$$...$$`
- Equation: `\begin{equation}...\end{equation}`
- Align: `\begin{align}...\end{align}`
- Theorem environments: `\begin{theorem}`, `\begin{lemma}`, `\begin{proposition}`

### Custom Commands Count
- `\newcommand{...}{...}`
- `\def\...{...}`
- `\newenvironment{...}{...}{...}`

### Cross-References Count
- Citations: `\cite{...}`, `\citet{...}`, `\citep{...}`
- References: `\ref{...}`, `\eqref{...}`
- Labels: `\label{...}`

## Complexity Classification

| Complexity | Math Envs | Custom Cmds | Cross-Refs |
|------------|-----------|-------------|------------|
| Simple     | < 20      | < 3         | < 30       |
| Moderate   | 20-50     | 3-10        | 30-100     |
| Complex    | > 50      | > 10        | > 100      |

## Safe Editing Zones

### CAN SAFELY EDIT:
- Plain text paragraphs (outside math mode)
- Section titles (but preserve \section{} command)
- Figure captions (but preserve \caption{} command)
- Abstract and introduction text
- Comments (% lines)

### CANNOT EDIT (preserve exactly):
- Content within $...$ or \[...\]
- Content within math environments
- Citation commands (\cite, \citet, \citep)
- Reference commands (\ref, \eqref, \label)
- Custom command definitions
- Preamble (everything before \begin{document})

## Warning Template

For Moderate complexity:
```
⚠️ LaTeX Moderate Complexity

Your file contains:
- [N] math environments
- [M] custom commands
- [K] cross-references

Recommendation:
- Review changes in math-heavy sections carefully
- Compile after each stage: pdflatex [file].tex
- Check theorem numbering and references
```

For Complex complexity:
```
⚠️ LaTeX High Complexity

Your file contains:
- [N] math environments
- [M] custom commands
- [K] cross-references

Strong recommendations:
- Create backup: cp [file].tex [file]-backup.tex
- Compile after EVERY stage to catch issues early
- Review ALL math sections carefully
- Consider processing in smaller sections
```

## Compilation Recommendation

After each stage, recommend user runs:
```bash
pdflatex [file].tex
# Check output for errors
# If errors, run again (for references):
pdflatex [file].tex
```
