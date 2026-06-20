# OpenAlex CLI Initial Setup

## Installation

Install globally via npm:

```bash
npm install -g openalex-skill
```

After installation, the `openalex` command will be available globally.

## API Key Configuration

The OpenAlex API has rate limits. Using an API key provides higher quotas.

### Get Your API Key

1. Visit https://openalex.org/settings/api-key
2. Sign in or create an account
3. Generate and copy your API key

### Configuration Methods (Recommended: Persistent Config)

Use the `config` command to save your API key to the user config file:

```bash
openalex config set api-key your_api_key_here
```

Verify the configuration:

```bash
openalex config show
```

### Alternative Configuration Methods

**Environment Variable (temporary):**

Bash:

```bash
export OPENALEX_API_KEY=your_api_key_here
openalex works search "machine learning" --per-page 5
```

PowerShell:

```powershell
$env:OPENALEX_API_KEY="your_api_key_here"
openalex works search "machine learning" --per-page 5
```

**Config file location:**

```bash
openalex config path
# Example output: /home/username/.openalex-skill/config.json
```

### Remove Configuration

To remove a saved API key:

```bash
openalex config unset api-key
```

## Quick Verification

After installation and configuration, verify everything works:

```bash
# Check version
openalex --version

# View help
openalex --help

# Test search (works without API key)
openalex works search "test" --per-page 1

# Check rate limit status
openalex rate-limit

# Download a paper PDF (requires open access)
openalex works download https://doi.org/10.48550/arXiv.1706.03762
```
