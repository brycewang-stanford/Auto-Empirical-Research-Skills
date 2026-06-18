# LaTeX Survey Template

Use this template as the starting point for `survey.tex`. Adapt the title, sections,
and table columns based on the specific topic and papers found.

```latex
\documentclass[12pt]{article}

% Packages
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage[margin=1in]{geometry}
\usepackage[colorlinks=true,citecolor=blue,linkcolor=blue,urlcolor=blue]{hyperref}
\usepackage{booktabs}
\usepackage{natbib}
\usepackage{setspace}
\usepackage{array}

% Bibliography style
\bibliographystyle{plainnat}

% Document metadata
\title{[TOPIC]: A Survey of Recent Contributions in [JOURNALS] ([YEAR])}
\author{Generated Survey\\{\small Auto-generated literature review}}
\date{[MONTH YEAR]}

\begin{document}

\maketitle

\begin{abstract}
% 150-200 words. Cover:
% 1. What the survey covers (topic, journals, year)
% 2. Main thematic groups found
% 3. Key findings across papers
% 4. Note on selection methodology and varying relevance
\end{abstract}

\doublespacing

%% ============================================================
\section{Introduction}
\label{sec:intro}
%% ============================================================

% Paragraph 1: Why this topic matters in economics
% Paragraph 2: Position relative to existing surveys/foundational works
% Paragraph 3: Scope of this survey (journals, year, search method)
% Paragraph 4: Selection methodology — be transparent about keyword search,
%   note papers with varying degrees of relevance to the core topic
% Paragraph 5: Preview of thematic groups and paper distribution

%% ============================================================
\section{Summary of Surveyed Papers}
\label{sec:summary}
%% ============================================================

\begin{table}[htbp]
\centering
\caption{Papers Surveyed}
\label{tab:summary}
\begin{tabular}{>{\raggedright\arraybackslash}p{3.5cm} l >{\raggedright\arraybackslash}p{4.5cm} l >{\raggedright\arraybackslash}p{3cm}}
\toprule
Authors & Journal & Title & Type & Key Aspect \\
\midrule
% Fill in one row per paper
% Type: Theory / Empirical / Econometric / Methodological
\bottomrule
\end{tabular}
\end{table}

%% ============================================================
\section{[Thematic Group 1]}
\label{sec:theme1}
%% ============================================================

% For each paper in this group:
% - 2+ paragraphs of substantive discussion
% - What the paper does, how it does it, what it finds
% - How it connects to other papers in the survey
% - At least 1 sentence on limitations or open questions

%% ============================================================
\section{[Thematic Group 2]}
\label{sec:theme2}
%% ============================================================

%% ============================================================
\section{[Thematic Group 3]}
\label{sec:theme3}
%% ============================================================

%% ============================================================
\section{Methodological Advances}
\label{sec:methods}
%% ============================================================

% Cross-cutting comparison of methods used across papers:
% - What identification strategies are used?
% - What data sources?
% - What tradeoffs (tractability vs generality, structural vs reduced-form)?
% - What platforms/datasets are novel?

%% ============================================================
\section{Conclusion}
\label{sec:conclusion}
%% ============================================================

% 1. Synthesize the main themes
% 2. Identify gaps — what's missing from the literature?
% 3. Future directions — what questions do these papers raise?
% 4. Optional: data availability note for open-access PDFs

\bibliography{references}

\end{document}
```

## Citation Style Guide

- `\citet{key}` — when the author is the grammatical subject:
  "Zenou and Zhou (2026) develop a model..."
- `\citep{key}` — parenthetical:
  "...multiplex network games (Zenou and Zhou, 2026)"
- `\citep[see, e.g.,][]{key}` — with prefix:
  "...foundational treatments (see, e.g., Jackson, 2008)"
- `\citep{key1,key2}` — multiple citations:
  "(Sadler, 2026; Leung and Moon, 2026)"

## BibTeX Citation Key Convention

`{firstauthorlastname}{year}{keyword}`

Examples:
- `zenou2026multiplex`
- `sadler2026swap`
- `bailey2026integration`
