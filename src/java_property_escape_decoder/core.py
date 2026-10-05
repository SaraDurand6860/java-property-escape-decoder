from __future__ import annotations


def _to_code_point(value: int) -> str:
    """Validate and convert a decoded u-escape value to its character.

    Java's |\\uXXXX| allows any value 0x0000-0xFFFF; values above 0xFFFF must be
    expressed as a surrogate pair. We mirror that exactly so callers do not
    silently get garbled output from over-long escapes.
    """
    if 0x0000 <= value <= 0xFFFF:
        return chr(value)
    raise ValueError(f"unicode escape out of range: \\u{value:04X}")


def decode(text: str) -> str:
    """Decode Java properties-file escape sequences in *text*.

    Recognised escapes:
      - \\t, \\n, \\r, \\f, \\\\  -> the obvious character
      - \\uXXXX        -> the BMP code point XXXX (exactly 4 hex digits)
      - any other \\c  -> the literal character c

    A trailing backslash is treated as an error, matching the behaviour of
    java.util.Properties when confronted with a dangling escape at the end
    of a logical line.
    """
    out: list[str] = []
    i = 0
    length = len(text)

    while i < length:
        char = text[i]
        if char != "\\":
            out.append(char)
            i += 1
            continue

        if i + 1 >= length:
            raise ValueError("dangling backslash at end of input")

        escaped = text[i + 1]
        if escaped == "u":
            j = i + 2
            if j + 4 > length:
                raise ValueError("truncated unicode escape")
            digits = text[j : j + 4]
            try:
                value = int(digits, 16)
            except ValueError as exc:
                raise ValueError(f"invalid unicode escape: \\u{digits}") from exc
            out.append(_to_code_point(value))
            i = j + 4
        elif escaped == "t":
            out.append("\t")
            i += 2
        elif escaped == "n":
            out.append("\n")
            i += 2
        elif escaped == "r":
            out.append("\r")
            i += 2
        elif escaped == "f":
            out.append("\f")
            i += 2
        else:
            out.append(escaped)
            i += 2

    return "".join(out)
