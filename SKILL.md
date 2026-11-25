---
name: lightning-ai-skill
description: Control Lightning AI Studios headlessly via CLI/SSH and keep a free 4-vCPU Studio alive for a requested timer duration using the official lightning_sdk keepalive heartbeat.
---

# Lightning AI Studio & Timer Skill

Use this skill when an AI agent needs a **real-time remote 4-vCPU Linux environment** on Lightning AI without touching the web UI, and needs the Studio to stay online for a specific duration without auto-sleeping.

## Prerequisites
1. Install lightweight control client (zero PyTorch/CUDA bloat):
   ```bash
   pip install -r requirements.txt
   ```
2. Authenticate:
   ```bash
   lightning login --no-browser --no-keychain
   ```
3. Configure SSH alias (one-time per Studio):
   ```bash
   lightning ssh configure --name <studio-name> --teamspace "<owner>/<teamspace>"
   ```

## Keeping a Free CPU Studio Alive for a Requested Duration
Do **not** modify `auto_sleep` or `auto_sleep_time` (doing so converts a free CPU Studio to paid). Instead, run `studio_timer.py` in the background for the requested duration:

```bash
python3 studio_timer.py --name <studio-name> --teamspace "<owner>/<teamspace>" --minutes 30
```

While `studio_timer.py` runs, `lightning_sdk` automatically sends Lightning's official 30-second keepalive heartbeat (`cloud_space_service_keep_alive_cloud_space_instance`), keeping the free `CPU` Studio online without restarts.

## Running Commands Over SSH
Once the Studio is running:
```bash
ssh -o BatchMode=yes <studio-name> "nproc && free -h"
```
