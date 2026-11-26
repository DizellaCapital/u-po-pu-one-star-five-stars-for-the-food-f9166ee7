"""One Star, Five Stars for the Food — make.fun entry.

Writes one alien tourist's one-star review of Earth, at most 200
characters, to entry.txt. Stdlib only.
"""

import os
import sys

REVIEW = (
    "I gave Earth one star: the sun quits every evening, "
    "the rain has no schedule, and you sleep away a third "
    "of your lives \u2014 but the rendang in Padang almost "
    "made me miss my flight home."
)
MAX_CHARS = 200


def abort(message):
    print("error: " + message, file=sys.stderr)
    raise SystemExit(1)


def checked_sentence(text):
    if not isinstance(text, str):
        abort("review is not text")
    if not text.strip():
        abort("review is empty")
    if len(text) > MAX_CHARS:
        abort(
            "review is %d characters, over the 200 limit" % len(text)
        )
    if "\n" in text or "\r" in text:
        abort("review must be a single line")
    if text.count(".") != 1 or not text.endswith("."):
        abort("review must be exactly one sentence ending in a period")
    return text


def target_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(out_dir, "entry.txt")


def main():
    line = checked_sentence(REVIEW)
    path = target_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    with open(path, "r", encoding="utf-8", newline="") as handle:
        back = handle.read()
    if back != line:
        abort("read-back mismatch: file does not hold the review")
    if len(back.encode("utf-8")) != len(line.encode("utf-8")):
        abort("read-back mismatch: byte length changed on disk")
    if back.endswith("\n") or back.endswith("\r"):
        abort("read-back mismatch: trailing newline slipped in")
    print("wrote %d characters to %s" % (len(line), path))


if __name__ == "__main__":
    main()
