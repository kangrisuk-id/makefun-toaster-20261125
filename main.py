"""The Funniest Toaster Error Message.

Writes one line -- the funniest error message a kitchen toaster
could show its owner -- to /output/entry.txt.

No network, no randomness, fully deterministic. The line is
71 characters, inside the 120-character limit.
"""

import os

ENTRY = "Error: This toaster has unionized. Toasting resumes after negotiations."

# The gate requires 1 to 120 characters of UTF-8 text, not only
# white space. Fail loudly here rather than shipping an invalid entry.
assert 1 <= len(ENTRY) <= 120, "entry must be 1-120 characters"
assert ENTRY.strip(), "entry must not be only white space"


def _write(path):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
        _write(os.path.join(out_dir, "entry.txt"))
        return
    except OSError:
        pass
    for fallback in ("./output", "."):
        try:
            os.makedirs(fallback, exist_ok=True)
            _write(os.path.join(fallback, "entry.txt"))
            return
        except OSError:
            continue


if __name__ == "__main__":
    main()
