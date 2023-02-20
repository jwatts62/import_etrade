"""Unit test for functions in unit readers."""

from unittest import TestCase

from reader import read


class test_read(TestCase):
    """Unit test(s) for the reader.read(..) funcition.
    """

    def test_read_files(self):
        """Read all of the test files."""
        CASE_FILES = [
            ('original-TxnHistory.csv', 146),
            ('transactions.csv', 159),
            ('TxnHistory.csv', 146),
            ('no such file', 0)
        ]

        DATA_ROOT = 'data/'
        for case in CASE_FILES:
            print(f'Expect to read {case[1]} lines from file: "{case[0]}".')
            lines = read(f'{DATA_ROOT + case[0]}')
            self.assertEqual(
                len(lines), case[1], 'Read unexpected number of lines from file "{case[0]}".')

# End of File
