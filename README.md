# devdash

**Beautiful developer dashboard for your terminal. Open a new tab and actually *feel* productive.**

```bash
pip install devdash
devdash --github your_username
```

[![CI](https://github.com/bhupendra05/devdash/actions/workflows/ci.yml/badge.svg)](https://github.com/bhupendra05/devdash/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

```
╭─────────────────────────╮  ╭──────────────────────────╮  ╭──────────────────────────╮
│           Time          │  │         Weather          │  │          GitHub          │
│                         │  │                          │  │                          │
│  🌅  Good morning!      │  │  ☀️  Sunny               │  │  🐙 @bhupendra05         │
│                         │  │  🌡️  28°C (feels 32°C)   │  │  Builder & AI tinkerer  │
│  🕐  09:14:32           │  │  💧 Humidity: 71%        │  │                          │
│  📅  Thursday, May 28   │  │  📍 Mumbai, India        │  │  📦 42 repos             │
│                         │  │                          │  │  👥 120 followers        │
╰─────────────────────────╯  ╰──────────────────────────╯  ╰──────────────────────────╯
╭─────────────────────────────────────────╮  ╭────────────────────────────────────────╮
│                 System                  │  │           Quote of the Day             │
│                                         │  │                                        │
│  CPU    ████████░░░░░░░░░░░░  39%       │  │  First, solve the problem.             │
│  RAM    ████████████░░░░░░░░  61%  8/13 │  │  Then, write the code.                 │
│  Disk   █████████████░░░░░░░  65% 320GB │  │                                        │
│  💻 macOS                               │  │    — John Johnson                      │
╰─────────────────────────────────────────╯  ╰────────────────────────────────────────╯
```

---

## Install

```bash
pip install devdash

# With better system stats (optional)
pip install devdash[system]
```

## Usage

```bash
# Basic (clock + system + quote)
devdash

# With weather (auto-detects your location)
devdash --github bhupendra05

# Specify city for weather
devdash --github bhupendra05 --location Mumbai

# Print once and exit (for screenshots!)
devdash --github bhupendra05 --once

# Custom refresh interval (seconds)
devdash --refresh 5

# Set permanently via environment variables
export DEVDASH_GITHUB=bhupendra05
export DEVDASH_LOCATION=Mumbai
devdash
```

## What's shown

| Widget | Description |
|--------|-------------|
| 🕐 **Time** | Live clock, date, and time-of-day greeting |
| ☀️ **Weather** | Current conditions via [wttr.in](https://wttr.in) — no API key needed |
| 🐙 **GitHub** | Your public repo count, followers, bio |
| 💻 **System** | CPU, RAM, disk usage with visual bars |
| 💬 **Quote** | A different developer quote every day |

## Tips

```bash
# Add to your shell profile for a dashboard on every new terminal tab
echo 'devdash --github bhupendra05 --once' >> ~/.zshrc

# Or as an alias
alias dash='devdash --github bhupendra05'
```

## License

MIT © [Bhupendra Tale](https://github.com/bhupendra05)
