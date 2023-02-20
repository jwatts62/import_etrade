"""This module provides miscelaneous functions for
processing etrade logs.
Translate an eTrade transaction file to common format.

Input:
        For Account:,####2641

    TransactionDate,TransactionType,SecurityType,Symbol,Quantity,Amount,Price,Commission,Description

    12/31/19,Dividend,MF,JSPGX,5.834,-81.33,0,0,JANUS HENDERSON GLOBAL ALLOCATJANUS HENDERSON               REINVEST PRICE $ 13.94
    12/31/19,Dividend,MF,JSPGX,1.359,-18.95,0,0,JANUS HENDERSON GLOBAL ALLOCATJANUS HENDERSON               REINVEST PRICE $ 13.94
    12/31/19,Dividend,MF,BJBHX,0.655,-5.8,0,0,ABERDEEN GLOBAL HIGH INCOME A ABERDEEN                      REINVEST PRICE $  8.86
    12/31/19,Dividend,MF,JSPGX,0,18.95,0,0,JANUS HENDERSON GLOBAL ALLOCATJANUS HENDERSON               RECORD 12/27/19 PAY 12/30/19  DIVIDEND RATE      0.187279460
    12/31/19,Dividend,MF,BJBHX,0,5.8,0,0,ABERDEEN GLOBAL HIGH INCOME A ABERDEEN                      RECORD 12/27/19 PAY 12/31/19  DIVIDEND RATE      0.032020000
    12/31/19,Dividend,MF,JSPGX,0,81.33,0,0,JANUS HENDERSON GLOBAL ALLOCATJANUS HENDERSON               L/T CAPITAL GAIN              RECORD 12/27/19 PAY 12/30/19

Output:
    platform,account,date,activity,type,symbol,description,quantity,price,cost,fee,foreign tax
    eTrade,2641,12/31/19,Buy,JSPGX,JANUS HENDERSON GLOBAL ALLOCATJANUS HENDERSON,5.834,13.04,-81.33,,,

"""

import re
from typing import List, Tuple

from reader import read


def strip_header(lines: List[str]) -> Tuple[str, List[str]]:
    """Process lines to extract the account number and provide a 'clean' list of lines without the header.

    Returns a tuple containing the account number and the remaining lines of text.
    """
    result = ('', lines[4:])
    return result


def get_acct_no(line: str) -> str:
    """Process lines to extract the account number.

    Returns a string containing the account number and the remaining lines of text.
    """
    acct_no = ''
    acct_no_exp = re.compile('For Account:,####(\\d{4})$')
    m = acct_no_exp.search(line)
    if m:
        # print(f'Found match:\n  {m}')
        acct_no = m[1]
        # print(f'Account number: {acct_no}')

    else:
        print(
            f'\nERROR: {__name__}() =>\n'
            f'  Failed to extract account number from file header.\n  >{line}<')

    return acct_no


def translate_etrade(srcFile: str) -> bool:
    """Translate an eTrade file.

    Returns 0 if successful, or False otherwise.
    """

    # srcFile = "./data/transactions.csv"
    # contents = import_records(srcFile, Decoders.ETRADE)
    # print(f'\n\n\n{contents[0]}; {contents[1]}')
    # pprint(xactions, indent=2)
    # display_partial(contents)

    # Step 1: Read the source file.
    file_contents = read(srcFile)
    if file_contents:
        # Step 2: Read the account number.
        acct_no = get_acct_no(file_contents[0])
        if acct_no:
            print(f'Read account number: "{acct_no}".')
            return True

        else:
            print(
                f'*** ERROR: {__name__}() =>\n  Failed to retrieve account number from line:\n  "{file_contents[0]}"\n'
                f'  from file: "{srcFile}".')

    else:
        print(
            f'*** ERROR: {__name__}() =>\n'
            f'  Failed to read contents of file: "{srcFile}".')

    return False

# End of File
