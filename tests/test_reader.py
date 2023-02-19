"""Unit test for functions in unit readers."""

from unittest import TestCase


class test_read(TestCase):
    """Unit test(s) for the reader.read(..) funcition.
    """

    def test_read_files(self):
        """Read all of the test files."""
        CASE_FILES = [
            ('original-TxnHistory.csv', 0),
            ('transactions.csv', 1),
            ('TxHistory.csv', 99)
        ]

        for case in CASE_FILES:
            print(f'Expect to read {case[1]} lines from file: "{case[0]}".')

# End of File
