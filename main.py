"""One Word for the Boss entry generator.

Writes exactly one word describing the boss to
``$MAKEFUN_OUTPUT_DIR/entry.txt`` (default ``/output``).

The word is "Hoverer": the boss who is always physically looming over
your shoulder while you work -- hovering by your desk, hovering in the
doorway, hovering over the document you are still typing. It is a real
word a person would actually use about the one they report to ("the
Hoverer is circling again"), it lands on its own with no caption, it
catches a habit every office worker has met, it is not the first word
anyone reaches for (that would be "micromanager"), and it travels --
a Hoverer works in a kitchen, a warehouse or an office alike.

Self-check gates (the entry is refused, not written, if any fail):
  * UTF-8 encodable
  * 1-30 characters long
  * exactly one word: no spaces, no newlines, no punctuation
  * not only whitespace
  * no control characters
The file is written with no trailing newline, so its bytes are exactly
the word and nothing else. After writing, the file is read back and
the bytes are compared with the word: a mismatch fails the run, so a
silent write error can never ship a wrong entry.
"""

import os
import sys

WORD = "Hoverer"

MAX_LENGTH = 30


def validate(word):
    """Return a list of gate failures; empty means the word passes."""
    failures = []
    try:
        word.encode("utf-8")
    except UnicodeEncodeError:
        failures.append("word is not UTF-8 encodable")
    if not 1 <= len(word) <= MAX_LENGTH:
        failures.append(
            "word must be 1-%d characters, got %d" % (MAX_LENGTH, len(word))
        )
    if word != word.strip() or not word.strip():
        failures.append("word must not be only whitespace or padded")
    if any(ch.isspace() for ch in word):
        failures.append("word must be a single word with no whitespace")
    if any(not ch.isalpha() for ch in word):
        failures.append("word must contain letters only")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in word):
        failures.append("word contains control characters")
    return failures


def main():
    failures = validate(WORD)
    if failures:
        for failure in failures:
            print("gate failed: %s" % failure, file=sys.stderr)
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    entry_path = os.path.join(output_dir, "entry.txt")
    with open(entry_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(WORD)
    with open(entry_path, "rb") as handle:
        on_disk = handle.read()
    if on_disk != WORD.encode("utf-8"):
        print("gate failed: file on disk does not match the word", file=sys.stderr)
        return 1
    print("wrote %d characters to %s" % (len(WORD), entry_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
