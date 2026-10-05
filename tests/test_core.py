import unittest

from java_property_escape_decoder import decode


class DecodeTests(unittest.TestCase):
    def test_plain_text_passes_through(self):
        self.assertEqual(decode("hello world"), "hello world")

    def test_tab_escape(self):
        self.assertEqual(decode("col1\\tcol2"), "col1\tcol2")

    def test_newline_escape(self):
        self.assertEqual(decode("line1\\nline2"), "line1\nline2")

    def test_return_escape(self):
        self.assertEqual(decode("a\\rb"), "a\rb")

    def test_formfeed_escape(self):
        self.assertEqual(decode("a\\fb"), "a\fb")

    def test_backslash_escape(self):
        self.assertEqual(decode("a\\\\b"), "a\\b")

    def test_passthrough_escape_keeps_character(self):
        # Java allows \X for any X not otherwise defined; it becomes X.
        self.assertEqual(decode("a\\:b"), "a:b")

    def test_unicode_escape_lowercase(self):
        self.assertEqual(decode("\\u00e9"), "\u00e9")

    def test_unicode_escape_uppercase(self):
        self.assertEqual(decode("\\u00E9"), "\u00e9")

    def test_unicode_escape_mixed_case(self):
        self.assertEqual(decode("\\u0aB4"), "\u0ab4")

    def test_unicode_escape_space(self):
        self.assertEqual(decode("\\u0020"), " ")

    def test_mixed_escapes(self):
        self.assertEqual(decode("\\t\\u0041\\n"), "\tA\n")

    def test_empty_string(self):
        self.assertEqual(decode(""), "")

    def test_dangling_backslash_raises(self):
        with self.assertRaises(ValueError):
            decode("\\")

    def test_truncated_unicode_escape_raises(self):
        with self.assertRaises(ValueError):
            decode("\\u00")

    def test_invalid_hex_digits_raises(self):
        with self.assertRaises(ValueError):
            decode("\\u00zz")

    def test_unicode_escape_followed_by_plain_text(self):
        self.assertEqual(decode("\\u0041bc"), "Abc")

    def test_backslash_followed_by_escape_sequence_keeps_escape(self):
        self.assertEqual(decode("\\\\\\n"), "\\\n")


if __name__ == "__main__":
    unittest.main()
