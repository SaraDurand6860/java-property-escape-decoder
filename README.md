# Java Property Escape Decoder

Decodes the escape sequences Java `.properties` files use — `\t`, `\n`, `\r`, `\f`, `\uXXXX`, `\\`, and the pass-through `\X` form — into the characters they stand for. Standard library only, nothing to install.

```python
from java_property_escape_decoder import decode

print(decode("line\\t\\u00e9"))   # line<TAB>é
```

## Why

Writing a `.properties` file by hand or generating one programmatically is easy; reading one back and turning `\u00e9` into `é` without pulling in the JVM is the part people keep reinventing badly. This library exists to do that one job, deterministically, with no dependencies.

The trade-off: this is a pure decoder. It does not split `.properties` files into key/value pairs, it does not honour the continuation line (`\` at end of line), and it does not handle the key/value separator rules. Feed it the contents of a logical line and it gives you back the decoded string.

## Edge cases

- A trailing backslash with nothing after it is an error, not a literal backslash. Java's own reader treats this as malformed input.
- `\uXXXX` must be exactly four hex digits. Java allows the full BMP range; values above `0xFFFF` must be written as a surrogate pair of two `\uXXXX` escapes — a single `\u` followed by more than four digits is rejected, matching Java's strict four-digit rule.
- `\X` for an `X` that is not one of the defined escapes decodes to the literal `X`. That is Java's behaviour for the pass-through form and this library preserves it.

## Exports

`decode(text: str) -> str` — the only public function.

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

