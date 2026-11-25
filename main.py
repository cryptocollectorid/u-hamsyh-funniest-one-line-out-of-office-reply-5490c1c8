"""Funniest One-Line Out-of-Office Reply — make.fun entry.

Writes a single out-of-office auto-reply line to /output/entry.txt.
The sealed gate requires UTF-8 text of 1 to 160 characters, not only
whitespace, on a single line.
"""

import sys
from pathlib import Path

ENTRY = (
    "I'm away from my desk, and my inbox is being handled by a man "
    "named Dave who does not work here."
)

MIN_CHARS = 1
MAX_CHARS = 160
OUTPUT_PATH = Path("/output/entry.txt")


def validate_entry(line: str) -> str:
    """Check the entry against the competition gate; fail loudly."""
    if not line or not line.strip():
        raise ValueError("entry must not be blank")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    bad = [c for c in line if ord(c) < 0x20 or ord(c) == 0x7F]
    if bad:
        raise ValueError(
            "entry must not contain control characters: "
            + ", ".join(f"U+{ord(c):04X}" for c in bad)
        )
    if not MIN_CHARS <= len(line) <= MAX_CHARS:
        raise ValueError(
            f"entry must be {MIN_CHARS}-{MAX_CHARS} characters, "
            f"got {len(line)}"
        )
    return line


def write_entry(line: str, out_path: Path) -> Path:
    """Validate the entry, write it, then read it back to verify."""
    validate_entry(line)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(line, encoding="utf-8")
    if out_path.read_text(encoding="utf-8") != line:
        raise ValueError("round-trip check failed: file differs from entry")
    return out_path


def main() -> None:
    path = write_entry(ENTRY, OUTPUT_PATH)
    print(f"Wrote {len(ENTRY)} characters to {path}")


if __name__ == "__main__":
    main()
