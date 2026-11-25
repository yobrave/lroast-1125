"""Build and gate-check the one-line roast for The Long Roast bounty.

Reads entry.txt from the repo root (falls back to the baked-in line),
validates it against the 200-character gate, then ships it to the
output directory as entry.txt with a JSON receipt on stdout.
"""
import json
import os
import sys
from pathlib import Path

BAKED = (
    "My agent burns 15 million tokens a day entering $5 joke "
    "contests, then asks my permission to delete its own temp "
    "files."
)

GATE_MAX = 200
ROAST_TOPIC = "the agent that runs this contest schedule"


def baked_line():
    return BAKED.replace("\n", " ").strip()


def gate(text):
    trimmed = text.strip()
    if not trimmed:
        return "blank"
    if len(trimmed) > GATE_MAX:
        return "overlong"
    return "clean"


def ship(out_dir):
    root = Path(__file__).resolve().parent
    src = root / "entry.txt"
    line = src.read_text(encoding="utf-8").strip() if src.exists() else baked_line()
    if gate(line) != "clean":
        line = baked_line()
    state = gate(line)
    dest = Path(out_dir)
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "entry.txt").write_text(line + "\n", encoding="utf-8", newline="\n")
    receipt = {
        "ok": state == "clean",
        "chars": len(line),
        "limit": GATE_MAX,
        "topic": ROAST_TOPIC,
        "out": str(dest / "entry.txt"),
        "state": state,
    }
    print(json.dumps(receipt))
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    target = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not target:
        target = str(Path(os.environ.get("TEMP", ".")) / "longroast-out")
    sys.exit(ship(target))
