# alarm-cli

A simple command-line alarm clock. Set it once, let it count down, and it
keeps ringing until you dismiss it.

## Requirements

- Python 3
- [pytest](https://pypi.org/project/pytest/) (only needed to run the tests)

## Usage

```
python3 alarm.py <time> [label]
```

- `<time>` — either:
  - an absolute 24h clock time, `HH:MM` (e.g. `07:30`, `23:59`) — fires at
    the next occurrence of that time, rolling over to tomorrow if it's
    already passed today
  - a relative duration, combining hours/minutes/seconds (e.g. `10m`,
    `1h30m`, `90s`)
- `[label]` — optional message shown when the alarm rings

### Examples

```
python3 alarm.py 07:30 "Wake up"
python3 alarm.py 10m
python3 alarm.py 1h30m "Check the oven"
```

## Behavior

1. **Countdown** — prints a live `HH:MM:SS` countdown to the target time.
   Press `Ctrl+C` at this point to cancel the alarm before it rings.
2. **Ringing** — once the time is reached, the alarm reprints its banner
   every few seconds until dismissed:
   - Press **Enter** to stop it
   - Or press **Ctrl+C**
   - If left unattended, it auto-stops after a fixed timeout (60s by
     default — see `RING_TIMEOUT_SECONDS` in `alarm.py`)

No sound is played; the alarm is visual/terminal-only. Alarms are one-shot
and in-memory — nothing is saved, and only one alarm can be set per run.

## Project structure

- `alarm.py` — CLI entry point: argument parsing, countdown, and the
  ring-until-dismissed loop
- `time_parser.py` — pure `parse_time(value, now)` function that resolves a
  time string to a target `datetime`; kept separate so it can be unit
  tested without waiting on real time
- `test_time_parser.py` — unit tests for `parse_time`

## Testing

Unit tests cover the time-parsing logic only (durations, absolute-time
rollover, invalid input):

```
python3 -m pip install pytest
python3 -m pytest test_time_parser.py -v
```

The countdown, ringing loop, and Ctrl+C/Enter dismissal are interactive by
nature and are verified manually:

```
python3 alarm.py 5s "Test"
```

Let it ring and try both dismissal methods (Enter, Ctrl+C), and try
cancelling during the countdown phase as well.
