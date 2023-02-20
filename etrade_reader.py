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


def strip_header(lines: List[str]) -> List[str]:
    """Process lines to extract the account number and provide a 'clean' list of lines without the header.

    Returns a tuple containing the account number and the remaining lines of text.
    """
    result = lines[4:]
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

    print(f'Processing source file: "{srcFile}".')
    # Step 1: Read the source file.
    file_contents = read(srcFile)
    if file_contents:
        print(f'  Read {len(file_contents)} lines from file.')
        # Step 2: Read the account number.
        acct_no = get_acct_no(file_contents[0])
        if acct_no:
            print(f'  Read account number: "{acct_no}".')
            filtered_contents = strip_header(file_contents)
            print(f'  Filtered {len(filtered_contents)} entries.')
            print(f'{"  Line 0:":>12} {filtered_contents[0]}')
            print(f'  Line [-1]: {filtered_contents[-1]}')

            sorted_contents = filtered_contents
            sorted_contents.sort()
            print(f'  Sortered {len(sorted_contents)} entries.')
            print(f'{"  Line 0:":>12} {sorted_contents[0]}')
            print(f'  Line [-1]: {sorted_contents[-1]}')

            # Step 3: Tokenize contents.
            tokenized_contents = []
            for line in sorted_contents:
                # print(f'\n  Before split: {len(tokenized_contents)}.')
                tokens = line.split(',')
                # print(f'  {tokens = }')
                tokenized_contents.append(tokens)
                # print(f'  After split: {len(tokenized_contents)}.')

            # Step 3b Sort on date.
            print(
                f'\n  first/last tokens:\n  {"  Line 0:":>12} {tokenized_contents[0]}')
            print(f'  Line [-1]: {tokenized_contents[-1]}')

            # Step 3c: Get start and end dates.
            start_date = tokenized_contents[0][0]
            end_date = tokenized_contents[-1][0]
            print(f'\n  Span: {start_date} => {end_date}')

            start_date = start_date.replace('/', '_')
            end_date = end_date.replace('/', '_')
            print(f'\n  Span: {start_date} => {end_date}')


            # Step 3c: Sort on activity.
            tokenized_contents.sort(key=lambda row: row[1])
            print(
                f'\n  first/last tokens:\n  {"  Line 0:":>12} {tokenized_contents[0]}')
            print(f'  Line [-1]: {tokenized_contents[-1]}')

            # Step 4: Save new file:
            dst_file = f'output/{acct_no}-{start_date}-{end_date}.csv'
            print(f'  Writing output file: "{dst_file}".')
            with open(dst_file, mode='w', encoding='utf8') as outfile:
                outfile.write('\n'.join(str(line) for line in tokenized_contents))

            # Step 4: Write new file.
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
