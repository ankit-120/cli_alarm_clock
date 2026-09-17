#!/usr/bin/env python3
import argparse
import sys
import threading
import time
from datetime import datetime

from time_parser import parse_time

RING_INTERVAL_SECONDS = 3
RING_TIMEOUT_SECONDS = 60


def countdown(target: datetime) -> None:
    while True:
        remaining = (target - datetime.now()).total_seconds()
        if remaining <= 0:
            break
        hours, rem = divmod(int(remaining), 3600)
        minutes, seconds = divmod(rem, 60)
        print(f"\rTime remaining: {hours:02d}:{minutes:02d}:{seconds:02d}", end="", flush=True)
        time.sleep(min(1, remaining))
    print()


def listen_for_enter(dismiss_event: threading.Event) -> None:
    input()
    dismiss_event.set()


def ring(message: str, interval: float, timeout: float) -> str:
    banner = "=" * max(len(message) + 4, 20)
    dismiss_event = threading.Event()
    threading.Thread(target=listen_for_enter, args=(dismiss_event,), daemon=True).start()

    start = time.monotonic()
    while not dismiss_event.is_set():
        if time.monotonic() - start >= timeout:
            return "timeout"
        print(f"\n{banner}\n  {message}\n{banner}\n(Press Enter to stop)")
        dismiss_event.wait(interval)

    return "dismissed"


def main() -> None:
    parser = argparse.ArgumentParser(description="A simple CLI alarm clock.")
    parser.add_argument("time", help="Alarm time as HH:MM (24h) or a duration like 10m, 1h30m, 90s")
    parser.add_argument("label", nargs="?", default=None, help="Optional label for the alarm")
    args = parser.parse_args()

    try:
        target = parse_time(args.time, datetime.now())
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Alarm set for {target.strftime('%Y-%m-%d %H:%M:%S')}. Press Ctrl+C to cancel.")

    message = f"ALARM: {args.label}" if args.label else "ALARM! Time's up!"
    phase = "waiting"
    try:
        countdown(target)
        phase = "ringing"
        result = ring(message, RING_INTERVAL_SECONDS, RING_TIMEOUT_SECONDS)
    except KeyboardInterrupt:
        print("\nAlarm cancelled." if phase == "waiting" else "\nAlarm stopped.")
        sys.exit(0)

    if result == "timeout":
        print(f"\n{message}\n(Auto-stopped after {RING_TIMEOUT_SECONDS}s with no response.)")
    else:
        print("\nAlarm stopped.")


if __name__ == "__main__":
    main()
