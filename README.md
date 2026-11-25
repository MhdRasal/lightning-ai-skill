# Lightning AI Skill & Studio Timer

> **For Educational Purposes Only.**  
> A lightweight, headless toolkit and AI Agent Skill (`SKILL.md`) for controlling **Lightning AI Studios** over CLI/SSH—without installing PyTorch locally—plus a generic **Studio Timer** using the official `lightning_sdk` keepalive heartbeat.

---

## ✨ Features

- **Zero Local Bloat:** Uses `lightning-sdk` only (~few MB, **no PyTorch or CUDA** required locally).
- **Generic Studio Timer (`studio_timer.py`):** Keeps any Lightning Studio alive for a requested number of minutes using `lightning_sdk`'s built-in 30-second keepalive heartbeat.
- **Free CPU Tier Safe:** Does **not** disable `auto_sleep` or alter `auto_sleep_time` (which would convert a free CPU Studio to paid). Uses `Machine.CPU` by default.
- **Agent-Ready (`SKILL.md`):** Drop into `~/.gemini/antigravity-cli/skills/` or `.claude/skills/` so AI coding agents can run real-time remote commands via SSH.

---

## 🚀 Quick Start

### 1. Install Lightweight Client (No PyTorch)
```bash
pip install -r requirements.txt
```

### 2. Log In Headlessly
```bash
lightning login --no-browser --no-keychain
```

### 3. Configure SSH Alias (One-Time)
```bash
lightning ssh configure --name my-studio --teamspace "<owner>/<teamspace>"
```
*(If the CLI cannot auto-upload your SSH key, copy `~/.ssh/lightning_ed25519.pub` and add it manually in Lightning AI **Settings ➔ SSH Keys**.)*

### 4. Start Studio With Timer
Keep any Studio online for e.g. 30 minutes without idle auto-sleep:
```bash
python3 studio_timer.py --name my-studio --teamspace "<owner>/<teamspace>" --minutes 30
```
Optional flags:
- `--machine CPU` (default; 4 vCPUs free tier)
- `--stop-on-exit` (automatically stops the Studio when the timer expires)

### 5. Run Commands in Real Time
While the timer is active, execute commands over standard SSH with sub-second latency:
```bash
ssh -o BatchMode=yes my-studio "nproc && free -h"
```

---

## ⚠️ Disclaimer
Intended strictly for **educational and personal development** use within Lightning AI's free Community tier quotas and Terms of Service. Always use `--stop-on-exit` or stop Studios when you are done.
