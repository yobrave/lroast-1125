"""Roast entry: gate check on entry.txt, then publish to the runner's output path."""
import json
import os
from pathlib import Path

GATE_MAX = 200
ORIGIN = Path(__file__).absolute().parent / "entry.txt"
STAMP = {"round": "11251342-lro5", "bounty": "long-roast"}


def emit() -> str:
    data = ORIGIN.read_bytes()
    line = data.decode("utf-8").strip()
    gate = 0 < len(line) <= GATE_MAX
    if gate:
        dest = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "entry.txt").write_bytes(line.encode("utf-8"))
    gate_report = {"gate": "pass" if gate else "fail", "n": len(line), "cap": GATE_MAX}
    return json.dumps(gate_report)


def start():
    body = emit()
    print(body, STAMP["round"])
    return '"gate": "pass"' in body


if __name__ == "__main__":
    ok = start()
    raise SystemExit(0 if ok else 1)
