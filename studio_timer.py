#!/usr/bin/env python3
"""
Lightning AI Studio Timer (Educational / Free CPU Keepalive Utility)

Keeps any Lightning AI Studio alive for a requested duration using the official
`lightning_sdk` keepalive heartbeat without modifying `auto_sleep` settings
(keeping free CPU Studios on the free tier).
"""
import argparse
import signal
import sys
import time
from lightning_sdk import Machine, Status, Studio


_STOP_REQUESTED = False


def _handle_signal(signum, _frame):
    global _STOP_REQUESTED
    _STOP_REQUESTED = True
    print(f"\n[!] Received signal {signum}, shutting down timer cleanly...")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Keep a Lightning AI Studio running for a requested number of minutes."
    )
    parser.add_argument("--name", required=True, help="Studio name")
    parser.add_argument("--teamspace", required=True, help="Teamspace in OWNER/NAME format")
    parser.add_argument("--minutes", type=float, default=10.0, help="Duration in minutes to keep Studio alive (default: 10)")
    parser.add_argument("--machine", default="CPU", help="Machine type when starting (default: CPU)")
    parser.add_argument("--stop-on-exit", action="store_true", help="Stop the Studio when the timer expires")
    args = parser.parse_args()

    if args.minutes <= 0:
        print("[!] --minutes must be greater than 0.", file=sys.stderr)
        return 1

    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    machine = getattr(Machine, args.machine, args.machine)

    print(f"[*] Connecting to Studio '{args.name}' in '{args.teamspace}'...")
    studio = Studio(name=args.name, teamspace=args.teamspace)

    if studio.status != Status.Running:
        print(f"[*] Studio is {studio.status}. Starting on {args.machine}...")
        studio.start(machine=machine)
        print("[+] Studio started. Official SDK 30s keepalive heartbeat is active.")
    else:
        studio._setup()
        print("[+] Studio is already running. Official SDK 30s keepalive heartbeat is active.")

    total_seconds = int(args.minutes * 60)
    end_time = time.time() + total_seconds
    end_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time))
    print(f"[*] Timer active for {args.minutes:.1f} min (until {end_str}).")

    try:
        while not _STOP_REQUESTED and time.time() < end_time:
            remaining = int(end_time - time.time())
            if remaining <= 0:
                break
            time.sleep(min(30, remaining))
    finally:
        print("[*] Stopping SDK keepalive heartbeat...")
        try:
            studio._studio_api.stop_keeping_alive(
                teamspace_id=studio._teamspace.id,
                studio_id=studio._studio.id,
            )
        except Exception as exc:
            print(f"[!] Warning while stopping keepalive: {exc}", file=sys.stderr)

        if args.stop_on_exit:
            print("[*] Stopping Studio (--stop-on-exit)...")
            studio.stop()
            print("[+] Studio stopped.")

    print("[+] Timer completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
