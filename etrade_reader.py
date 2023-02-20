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
        print(f'Found match:\n  {m}')
        acct_no = m[1]
        print(f'Account number: {acct_no}')

    else:
        print(
            f'\nERROR\nFailed to extract account number from file header.\n  >{line}<')

    return acct_no

# End of File
