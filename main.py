#!/usr/bin/env python3
"""Write the single judged artifact for Loading Screen Gold.

The grader runs this at the repository root with python3.13 and reads only
/output/entry.txt.  The text is embedded here: nothing is read from the
network, git history, or any file outside this repository.

v2 improvement over the first write: the output directory is swept of stale
temp files so it holds only the required artifact, and a strict post-condition
checks the written bytes, the 0644 mode, the absence of a trailing newline and
the final directory listing before the program reports success.
"""

import os
import tempfile

OUTPUT_DIR = "/output"
ARTIFACT = os.path.join(OUTPUT_DIR, "entry.txt")

# One line, no trailing newline. 115 characters, well inside the 200 cap.
ENTRY = (
    "Loading tip: when the agent says done and the build says nope, "
    "trust the build. It has no incentive to comfort you."
)


def validate(text: str) -> bytes:
    """Apply the house gate's preconditions and return the exact bytes."""
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    if not (1 <= len(text) <= 200):
        raise ValueError(f"entry length {len(text)} is outside 1..200")
    if not text.strip():
        raise ValueError("entry is only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text.encode("utf-8")  # strict UTF-8 validation


def sweep_output_dir() -> None:
    """Leave /output holding nothing but the required artifact."""
    for name in os.listdir(OUTPUT_DIR):
        path = os.path.join(OUTPUT_DIR, name)
        if name != "entry.txt" and os.path.isfile(path) and not os.path.islink(path):
            os.unlink(path)


def write_atomically(payload: bytes) -> None:
    """Write payload into /output/entry.txt with a 0644 atomic replace."""
    fd, tmp = tempfile.mkstemp(prefix=".entry-", suffix=".tmp", dir=OUTPUT_DIR)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        # mkstemp creates 0600; the grader refuses that. Fix it BEFORE replace.
        os.chmod(tmp, 0o644)
        os.replace(tmp, ARTIFACT)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def verify(payload: bytes) -> None:
    """Hard post-conditions: byte-exact, 0644, one line, sole artifact."""
    if os.stat(ARTIFACT).st_mode & 0o777 != 0o644:
        raise RuntimeError("final artifact mode is not 0644")
    with open(ARTIFACT, "rb") as handle:
        written = handle.read()
    if written != payload:
        raise RuntimeError("final artifact bytes differ from the intended entry")
    if written.endswith((b"\n", b"\r")):
        raise RuntimeError("final artifact has a trailing newline")
    if os.listdir(OUTPUT_DIR) != ["entry.txt"]:
        raise RuntimeError("/output holds something other than entry.txt")
    print(
        f"entry.txt: {len(written)} bytes, {len(written.decode('utf-8'))} chars, "
        f"mode 0644, single line, /output clean"
    )


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    payload = validate(ENTRY)
    sweep_output_dir()
    write_atomically(payload)
    verify(payload)


if __name__ == "__main__":
    main()
