"""This unit provides test cases for eTrade transaction
logs.
"""

from unittest import TestCase
# acct_no = get_acct_no(file_contents[0])

from etrade_reader import get_acct_no


class test_etrade(TestCase):
    """Unit test(s) for the reader.read(..) funcition.
    """

    def test_acct_no(self):
        """Verify extraction of account numbers from eTrade
        transaction logs.
        """
        CASES = [('2641', 'For Account:,####2641'),
                 ('', 'For Account:,###2841'),
                 ('', 'For Xccount:,####3641'),
                 ('', 'For  Account:,####2651'),
                 ('', 'For Account:,##*#264w'),
                 ('', 'For Account:,####f2642'),
                 ]
        for case in CASES:
            acct_no = get_acct_no(case[1])
            if case[0]:
                self.assertEqual(case[0], acct_no,
                                 'Wrong value for account number.')
                print(f'Read account number: "{acct_no}".')

            else:
                self.assertFalse(
                    acct_no, 'Unexpectedly read wrong account number.')
                print(
                    f'*** ERROR: {__name__}() =>\n  Failed to retrieve account number from line:\n  "{case[1]}".')

# End of File
