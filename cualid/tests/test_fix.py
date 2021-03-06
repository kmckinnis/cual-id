import unittest
import io

from cualid.fix import fix_ids, format_output, parse_ids


class TestFormatOutput(unittest.TestCase):
    def test_simple(self):
        formatted = format_output([('abc', 'abc', 'k')], 'k')
        self.assertEqual(list(formatted),
                         ["abc\tabc\tk"])

    def test_excluded(self):
        formatted = format_output([
                ('ab1', 'a1c', 'a'),
                ('ab2', 'a2c', 'b'),
                ('ab3', 'a3c', 'k'),
                ('ab4', 'a4c', 'a'),
                ('ab5', 'a5c', 'b')
            ], 'ba')
        self.assertEqual(list(formatted), [
                "ab1\ta1c\ta",
                "ab2\ta2c\tb",
                "ab4\ta4c\ta",
                "ab5\ta5c\tb",
        ])


class TestFixIDs(unittest.TestCase):
    def setUp(self):
        correct1.seek(0)
        correct2.seek(0)
        identical.seek(0)
        bad.seek(0)

    def test_fix_ids_no_errors(self):
        tested = False
        for a, b, err in fix_ids(correct1, identical):
            tested = True
            self.assertEqual(a, b)
            self.assertEqual(err, 'V')

        self.assertTrue(tested)

    def test_fix_ids_unfixable(self):
        tested = False
        for a, b, err in fix_ids(correct1, bad):
            tested = True
            self.assertEqual(b, '')
            self.assertEqual(err, 'N')

        self.assertTrue(tested)

    def test_fix_ids_fix_all(self):
        tested = False
        for a, b, err in fix_ids(correct2, fixable):
            tested = True
            self.assertEqual(a[1:], b)
            self.assertEqual(err, 'F')

        self.assertTrue(tested)

    def test_parse_ids(self):
        exp = ['23bb9', 'c0cab', '87696', '7869b', 'd50cc']
        self.assertEqual(parse_ids(identical, 0), exp)
        self.assertEqual(parse_ids(correct1, 0), exp)

correct1 = io.StringIO("23bb9\tc0b5d3ae-d2d4-4aa5-bd51-76c93e223bb9\n"
                       "c0cab\t0b95a10f-0610-434f-9734-4d2ac02c0cab\n"
                       "87696\tef09be86-dfee-4ce1-84d4-e60b5df87696\n"
                       "7869b\tc13f1644-cab9-4474-b674-1442efc7869b\n"
                       "d50cc\tb60e7c07-bbf9-468c-a8f0-98639f2d50cc\n")

correct2 = io.StringIO("843ce05576\t9563938c-72db-4cf4-aa1c-b8843ce05576\n"
                       "2c9dbf17fa\tfdb1cca7-0a94-4725-95de-5d2c9dbf17fa\n"
                       "8f783cd158\t296bb722-bdc1-40c9-b154-178f783cd158\n"
                       "c1afedcf74\t1ab8e24e-3661-4a54-a2fc-c4c1afedcf74\n"
                       "f4b56fff8e\t6c36f950-5462-489a-9292-8ff4b56fff8e\n"
                       "0280dbdd77\t5f357627-14ad-4611-9706-040280dbdd77\n")

identical = io.StringIO("23bb9\n"
                        "c0cab\n"
                        "87696\n"
                        "7869b\n"
                        "d50cc\n")

bad = io.StringIO("xxxxx\n"
                  "xxxxx\n"
                  "xxxxx\n"
                  "xxxxx\n"
                  "xxxxx\n")

fixable = io.StringIO("t843ce05576\n"
                      "t2c9dbf17fa\n"
                      "t8f783cd158\n"
                      "tc1afedcf74\n"
                      "tf4b56fff8e\n"
                      "t0280dbdd77\n")

if __name__ == "__main__":
    unittest.main()
