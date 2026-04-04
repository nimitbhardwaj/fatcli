# fatcli

A CLI tool for Fatsecret API - track your nutrition, meals, and fitness goals from the command line.

## Features

- **Authentication** - OAuth flow with Fatsecret API
- **Profile** - View your profile, weight, BMI, and goals
- **Meals** - View, search, add, and delete food entries
- **Agent-friendly** - Designed for LLM agent integration

## Installation

```bash
pip install fatcli
```

Or from source:

```bash
git clone https://github.com/nimitbhardwaj/fatcli.git
cd fatcli
uv pip install -e .
```

## Setup

1. Get your Fatsecret API credentials from [platform.fatsecret.com](https://platform.fatsecret.com/api/)

2. Create a `.env` file or export variables:

```bash
export FATSECRET_CONSUMER_KEY=your_consumer_key
export FATSECRET_CONSUMER_SECRET=your_consumer_secret
export FATSECRET_CONFIG_DIR=~/.config/fatsecret  # optional
```

3. Authenticate:

```bash
fatcli init --url-only
# Visit the URL, get PIN, then:
fatcli init --pin 123456
```

Or interactive mode:

```bash
fatcli init
```

## Usage

### View Profile

```bash
fatcli profile
```

Output:
```
Profile
  Height:        173 cm
  Current Weight: 84.0 kg (as of 2026-04-03)
  Goal Weight:    74.0 kg
  Difference:     +10.0 kg
  BMI:            28.1
  Status:         Overweight
```

### Log Weight

```bash
fatcli profile --weight 83.5 --goal 74
```

### View Meals

```bash
# Today's meals
fatcli meals get --date 2026-04-04

# With macro summary
fatcli meals get --date 2026-04-04 --summary
```

### Search Foods

```bash
fatcli meals search chicken
```

### Get Food Details

```bash
fatcli meals info 1641
```

### Add Food Entry

```bash
fatcli meals add 1641 --serving 50321 --units 1 --meal lunch
```

### Delete Food Entry

```bash
# First get the entry ID from meals get
fatcli meals delete 23112601131
```

## Help

```bash
fatcli                    # Show main help
fatcli -h                 # Same as --help
fatcli meals              # Show meals subcommands
fatcli meals get --help   # Help for specific command
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `FATSECRET_CONSUMER_KEY` | Yes | - | API consumer key |
| `FATSECRET_CONSUMER_SECRET` | Yes | - | API consumer secret |
| `FATSECRET_CONFIG_DIR` | No | `~/.config/fatsecret` | Config directory |

## Agent Integration

This CLI is designed for LLM agent use:

```bash
# Get authorization URL
fatcli init --url-only

# Complete with PIN (from human)
fatcli init --pin 123456

# View meals for analysis
fatcli meals get --date 2026-04-04 --summary

# Check profile
fatcli profile
```

## License

MIT
