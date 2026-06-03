<!-- Vendored into AERS from https://github.com/tondevrel/scientific-agent-skills on 2026-06-01. Upstream attribution + license preserved. -->

> **Vendored upstream skill (subset).** Curated snapshot of the empirically-relevant skills `dowhy` (causal inference) and `lifelines` (survival analysis) from [`tondevrel/scientific-agent-skills`](https://github.com/tondevrel/scientific-agent-skills) (license: MIT). Vendored 2026-06-01. `dowhy/SKILL.MD` was renamed to `SKILL.md` for exact-case portability. The broader upstream collection (astropy/biopython/jax/etc.) is out of scope and not vendored. The original upstream README follows verbatim.

---

# Scientific Agent Skills

A comprehensive collection of **72 Agent Skills** for scientific computing, research workflows, and data analysis. These skills automatically enhance AI coding assistants (like Cursor, Claude Code, and others) with deep domain knowledge across the entire scientific Python ecosystem.

## What Are Agent Skills?

**Agent Skills** are contextual knowledge modules that automatically load when an AI assistant detects relevant topics in your conversation. Instead of generic coding help, you get expert-level guidance tailored to specific scientific domains.

### How It Works

1. **You start coding** with scientific libraries (NumPy, PyTorch, scikit-learn, etc.)
2. **Skills auto-load** based on semantic matching of your code and questions
3. **AI gets expert knowledge** from detailed skill documentation
4. **You receive better assistance** with best practices, common patterns, and domain-specific solutions

### Example

When you describe your problem:
> "I need to process a large array of scientific data efficiently. How do I optimize NumPy operations for performance?"

Or when you ask:
> "What's the best way to handle missing values in pandas before training a machine learning model?"

The relevant skills (`numpy` or `pandas-performance`) automatically load, providing the AI with:
- 1,361 lines of expert documentation (for NumPy)
- Best practices for array operations
- Common pitfalls and solutions
- Performance optimization techniques
- Real-world patterns and examples

The AI then gives you expert-level guidance tailored to your specific problem, not generic coding help.

## What Problems Can This Solve?

### 🔬 Scientific Computing & Research

- **Numerical Computing**: NumPy, SciPy, SymPy, JAX for mathematical computations
- **Physics & Chemistry**: Quantum computing (Qiskit, PennyLane), molecular dynamics (MDAnalysis), quantum chemistry (PySCF)
- **Astronomy & Astrophysics**: Astropy, SunPy, Photutils for astronomical data analysis
- **Bioinformatics**: Biopython, scikit-bio, Scanpy for biological data processing

### 🤖 Machine Learning & AI

- **Deep Learning**: PyTorch, TensorFlow for neural networks
- **Classical ML**: scikit-learn, XGBoost, LightGBM for traditional algorithms
- **NLP**: Transformers, spaCy, NLTK for natural language processing
- **Graph Neural Networks**: PyTorch Geometric for graph-structured data

### 📊 Data Analysis & Visualization

- **Data Processing**: Pandas, Polars, XArray for tabular and multidimensional data
- **Visualization**: Matplotlib, Seaborn, Plotly for creating publication-quality plots
- **Statistical Analysis**: Statsmodels, PyMC, NumPyro for Bayesian inference

### 🗺️ Geospatial & Earth Science

- **Geospatial Analysis**: GeoPandas, Shapely, Rasterio for geographic data
- **Remote Sensing**: Rasterio for satellite imagery processing
- **Coordinate Systems**: PyProj for map projections

### ⚙️ Optimization & Simulation

- **Mathematical Optimization**: OR-Tools, Pyomo for linear/nonlinear programming
- **Bayesian Optimization**: Ax Platform for experiment design
- **Simulation**: SimPy for discrete event simulation
- **Parallel Computing**: Dask for distributed computing

### 🔬 Specialized Domains

- **Signal Processing**: MNE for neurophysiological data (EEG/MEG)
- **Medical Imaging**: PyDICOM for DICOM file processing
- **Time Series**: sktime, tsfresh for temporal data analysis
- **Causal Inference**: DoWhy for causal analysis beyond correlation

## What Systems Can You Build?

With these skills, you can build:

### Research & Analysis Systems

- **Scientific Data Pipelines**: Automated processing of experimental data
- **Statistical Analysis Tools**: Bayesian inference, hypothesis testing, causal analysis
- **Visualization Dashboards**: Interactive plots for research publications
- **Simulation Frameworks**: Physics simulations, molecular dynamics, quantum systems

### Machine Learning Systems

- **Research Prototypes**: Rapid prototyping of new ML architectures
- **Production ML Pipelines**: End-to-end training and deployment workflows
- **Explainable AI Tools**: Model interpretation and feature importance analysis
- **AutoML Systems**: Automated hyperparameter optimization with Ax

### Scientific Computing Platforms

- **Computational Chemistry Tools**: Quantum chemistry calculations, molecular modeling
- **Astronomical Data Processors**: Image analysis, catalog matching, light curve analysis
- **Bioinformatics Workflows**: Sequence analysis, protein structure prediction
- **Geospatial Analytics**: GIS analysis, remote sensing applications

### Domain-Specific Applications

- **Medical Imaging Analysis**: DICOM processing, image segmentation
- **Neuroscience Tools**: EEG/MEG signal processing and analysis
- **Materials Science**: Crystal structure analysis, property prediction
- **Climate Science**: Time series analysis, spatial data processing

## Installation

### For Cursor IDE

Cursor supports Agent Skills natively. Install this repository as a skill collection:

#### Method 1: Clone to Cursor Skills Directory

```bash
# Clone the repository
git clone https://github.com/your-username/scientific-agent-skills.git

# Copy to Cursor skills directory
cp -r scientific-agent-skills/skills/* ~/.cursor/skills/
```

#### Method 2: Symlink (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-username/scientific-agent-skills.git

# Create symlink (allows easy updates)
ln -s $(pwd)/scientific-agent-skills/skills ~/.cursor/skills/scientific-agent-skills
```

#### Method 3: Direct Reference

If Cursor supports direct repository references:

```bash
# In Cursor settings, add:
~/.cursor/skills/scientific-agent-skills
```

### For Other Agents

#### Claude Code

```bash
# Clone and copy
git clone https://github.com/your-username/scientific-agent-skills.git
cp -r scientific-agent-skills/skills/* ~/.claude/skills/
```

#### Manual Installation

Clone and copy to your agent's skill directory:

| Agent | Skill Directory |
|-------|-----------------|
| Cursor | `~/.cursor/skills/` |
| Claude Code | `~/.claude/skills/` |
| OpenCode | `~/.config/opencode/skill/` |
| OpenAI Codex | `~/.codex/skills/` |
| Pi | `~/.pi/agent/skills/` |

## Getting Started

### 1. Install the Skills

Follow the installation instructions above for your IDE.

### 2. Describe Your Problem

Simply describe what you're trying to accomplish. Skills will auto-load based on your problem description:

**Example 1:**
> "I'm working with NumPy arrays and need to compute statistical measures efficiently. What's the best approach?"

The `numpy` skill automatically loads, and the AI provides expert guidance on vectorization, broadcasting, and performance optimization.

**Example 2:**
> "I want to train a neural network with PyTorch for image classification. How should I structure the training loop?"

The `pytorch` skill loads, giving the AI access to best practices for device management, gradient handling, and model checkpointing.

**Example 3:**
> "I need to analyze time series data and extract features for machine learning."

The `sktime & tsfresh` skill loads, providing guidance on time series feature extraction and pipeline construction.

### 3. Ask Domain-Specific Questions

The AI will have expert knowledge for:

- **Best Practices**: "What's the best way to handle missing data in pandas?"
- **Performance**: "How do I optimize this NumPy operation?"
- **Architecture**: "What's the recommended way to structure a PyTorch training loop?"
- **Debugging**: "Why is my scikit-learn model overfitting?"
- **Advanced Topics**: "How do I implement Bayesian optimization with Ax?"

### 4. Verify Skills Are Loading

In Cursor, you can check if skills are active by:
- Observing more detailed, domain-specific responses
- Seeing references to best practices and patterns
- Getting warnings about common pitfalls

## Available Skills

### 🔢 Numerical Computing (7 skills)
- `numpy`, `numpy-low-level`, `scipy`, `sympy`, `numba`, `jax`, `jax-pde`

### 📊 Data Analysis & Visualization (7 skills)
- `pandas-performance`, `polars`, `matplotlib`, `matplotlib-pro`, `seaborn`, `plotly`, `xarray`

### 🤖 Machine Learning (11 skills)
- `scikit-learn`, `sklearn-advanced`, `sklearn-explainability`, `xgboost-lightgbm`
- `pytorch`, `pytorch-research`, `pytorch-deployment`, `pytorch-geometric`
- `tensorflow`, `transformers`, `statsmodels`, `lifelines`

### 🧬 Bioinformatics & Biology (8 skills)
- `biopython`, `scikit-bio`, `scanpy`, `pysam`, `mdanalysis`, `prody`, `openbabel`, `rdkit`

### ⚛️ Chemistry & Physics (7 skills)
- `chempy`, `pyscf`, `ase`, `qutip`, `sunpy`, `astropy`, `photutils`

### 🔬 Signal & Image Processing (5 skills)
- `scikit-image`, `scikit-video`, `mne`, `pydicom`, `opencv`

### 🌐 Geospatial (4 skills)
- `geopandas`, `shapely`, `pyproj`, `rasterio`

### ⚙️ Optimization & Modeling (6 skills)
- `ortools`, `pyomo`, `cobrapy`, `simpy`, `dask`, `dask-optimization`

### 💻 Quantum Computing (3 skills)
- `qiskit`, `qiskit-hardware`, `pennylane`

### 📈 Time Series & Causality (3 skills)
- `sktime & tsfresh`, `dowhy`, `pymc & numpyro`

### 🛠️ Specialized Tools (8 skills)
- `ax-platform`, `gmsh & meshio`, `networkx`, `fastapi-streamlit`
- `h5py`, `duckdb`, `tqdm`, `spacy & nltk`

**Total: 72 skills** covering the entire scientific Python ecosystem.

## Skill Quality

All 72 skills are fully documented with:

- ✅ **16 skills** with 1000+ lines of expert documentation
- ✅ **25 skills** with 300-1000 lines of comprehensive guides
- ✅ **31 skills** with 100-300 lines of essential patterns
- ✅ **0 empty skills** - 100% completion rate

Top documented skills:
- `qiskit` (2,088 lines) - Quantum computing
- `mdanalysis` (1,921 lines) - Molecular dynamics
- `sympy` (1,821 lines) - Symbolic mathematics
- `biopython` (1,520 lines) - Bioinformatics
- `numpy` (1,361 lines) - Numerical computing

## Structure

```
scientific-agent-skills/
├── skills/                  # Auto-loading contextual skills
│   ├── FORMAT.md            # Format documentation
│   └── skill-name/          # Each skill is a folder
│       ├── SKILL.md         # Main skill definition
│       └── references/      # Detailed reference docs (optional)
├── commands/                # Slash commands (/command-name)
│   ├── FORMAT.md            # Format documentation
│   └── *.md                 # Command files
├── .claude-plugin/          # Claude Code plugin configuration (optional)
├── MCP-FORMAT.md            # MCP server configuration (optional)
└── README.md                # This file
```

## Contributing

We welcome contributions! To add a new skill:

1. Create a folder in `skills/` with your skill name
2. Add `SKILL.md` with frontmatter (name, description) and content
3. Optionally add `references/` folder for detailed docs
4. See `skills/FORMAT.md` for detailed instructions

## Format Guides

Each folder contains a `FORMAT.md` explaining the expected file format:

- [`skills/FORMAT.md`](skills/FORMAT.md) - Contextual skills
- [`commands/FORMAT.md`](commands/FORMAT.md) - Slash commands
- [`MCP-FORMAT.md`](MCP-FORMAT.md) - MCP server configuration

## Examples

### Example 1: NumPy Optimization

**You describe:**
> "I have a large dataset and I'm using a Python loop to process each element. It's very slow. How can I speed this up with NumPy?"

**AI with NumPy skill responds:**
- Explains vectorization principles
- Shows how to convert loops to array operations
- Provides performance benchmarks
- Suggests: `result = data * 2` instead of loops (100x faster)
- Warns about common pitfalls (memory layout, dtype selection)

### Example 2: PyTorch Training Loop

**You describe:**
> "I'm building a deep learning model with PyTorch. My training seems unstable and I'm not sure if I'm handling gradients correctly. Can you help me structure a proper training loop?"

**AI with PyTorch skill provides:**
- Complete training loop with proper device management
- Explains why `optimizer.zero_grad()` is critical
- Shows gradient accumulation patterns
- Implements early stopping
- Best practices for model checkpointing
- Common mistakes and how to avoid them

### Example 3: Bayesian Analysis

**You describe:**
> "I have experimental data and want to quantify uncertainty in my parameter estimates. I've heard about Bayesian methods but don't know where to start with PyMC."

**AI with PyMC skill guides you through:**
- When to use Bayesian vs frequentist methods
- Model specification with proper priors
- MCMC sampling setup and diagnostics
- Posterior analysis and interpretation
- Convergence checking (Rhat, ESS)
- Posterior predictive checks

## License

MIT

## Acknowledgments

This collection represents expert knowledge from the entire scientific Python community, distilled into actionable skills for AI coding assistants.

---

**Ready to supercharge your scientific coding?** Install the skills and start building! 🚀
