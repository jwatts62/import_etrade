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

from math import fabs
import re
import sys
from typing import Dict, List, Tuple

from reader import read, recordSymbol, write



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


ACTIONS = {
    'Bought': 'Buy',
    'Dividend': 'Div',
    'Sold': 'Sell'
}


def unpack_dividend(symbol, etrade_activity: str, line: List[str], crossRef: Dict[str, str]):
    """Unpack the description field of a Dividend
    transaction.
    """
    # print(f'\n{etrade_activity} - {line}')
    div_list = line

    tok_0 = line[0:29].strip()
    # print(f'"{tok_0 = }".')

    tok_1 = line[30:59].strip()
    # print(f'"{tok_1 = }".')

    tail = line[60:].strip()
    # print(f'"{tail = }".')

    if tail.startswith('CASH DIV'):
        # print(f'\n{etrade_activity} - {line}')
        # print(f'"{tok_0 = }".')
        # print(f'"{tok_1 = }".')
        # print(f' "{tail = }".')
        etrade_activity = 'Div'
        recordSymbol(symbol, tok_0, crossRef)

    # elif tok_1.startswith('CASH DIV'):
    #     print(f'\n{etrade_activity} - {line}')
    #     print(f'"{tok_0 = }".')
    #     print(f'"{tok_1 = }".')
    #     print(f' "{tail = }".')
    #     etrade_activity = 'Div'

    elif tail.startswith('REIN @'):
        etrade_activity = 'Buy'
        recordSymbol(symbol, tok_0, crossRef)

    elif tok_1.startswith('REIN @'):
        print(f'### Discarding: "{line}"')

    elif tok_1.startswith('CASH DIV'):
        print(f'### Discarding: "{line}"')

    elif tail.startswith('PRE SHARE'):
        etrade_activity = 'Buy'

    elif tail.startswith('REINVEST PRICE $'):
        etrade_activity = 'Buy'
        recordSymbol(symbol, tok_0, crossRef)

    elif tail.startswith('RECORD ') or tail.startswith('PER SHARE'):
        etrade_activity = 'Div'
        recordSymbol(symbol, tok_0, crossRef)

    elif tail.startswith('AGENCY PROCESSING FEE'):
        etrade_activity = 'Fee'

    elif tail.startswith('INT '):
        etrade_activity = 'Int'
        recordSymbol(symbol, tok_0, crossRef)

    else:
        print(f'\n*** ERROR: unrecognized activity: "{etrade_activity}": "{tail}"\n'
              f'    {etrade_activity} - "{line}"\n'
              f'    {tok_0 = }.\n'
              f'    {tok_1 = }.\n'
              f'     {tail = }.\n')
        # sys.exit(255)

    return etrade_activity


def translate(etrade: List[List[str]], crossRef: Dict[str, str]) -> List[List[str]]:
    """Translate a sequence of etrade transactions to gsheet format.

    Input:
        TransactionDate,TransactionType,SecurityType,Symbol,Quantity,Amount,Price,Commission,Description

    Output:
        TransactionDate,TransactionType,Symbol,Quantity,Price,Amount,Fee

    :param List[List[str]] etrade: Translated etrade transactions
    """

    gsheet = []
    for input in etrade:
        activity = input[1]
        if activity == 'Bought':
            activity = 'Buy'
            recordSymbol(input[3], input[8][0:29].strip(), crossRef)
            # if not symbol in crossRef:
            #     name = input[8][0:29].strip()
            #     crossRef[symbol] = name
            #     print(f'Symbol: "{symbol}: {name}.')

        elif activity == 'Dividend':
            # Figure it out.
            activity = unpack_dividend(input[3], activity, input[8], crossRef)
            # activity = 'TBD'

        elif activity == 'Sold':
            # Figure it out.
            activity = 'Sell'

        else:
            print(f'Failed to process a line: "{input}".')
            sys.exit(255)

        #   [0]                 [1]             [2]         [3]     [4]     [5]     [6]     [7]         [8]
        # TransactionDate, TransactionType, SecurityType, Symbol, Quantity, Amount, Price, Commission, Description
        line = f'{input[0]},{activity},{input[3]},{input[4]},{input[6]},{fabs(float(input[5]))},{input[7]}'
        # print(f'{input}\n{line}')
        #           Date,   Type, Symbol,     Qty,      Price,      Amount, Fee
        gsheet.append(line)

        # else:
        #     print(
        #         f'Unrecognized activity: "{input[1]}" in line:\n  "{input}".')

    return gsheet


def translate_etrade_file(srcFile: str, crossRef: Dict[str, str]) -> bool:
    """Translate an eTrade file.

    param srcFile - Path + name of source file;
    param crossRef - A dictionary of symbols and names.

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
            # print(f'  Filtered {len(filtered_contents)} entries.')
            # print(f'{"  Line 0:":>12} {filtered_contents[0]}')
            # print(f'  Line [-1]: {filtered_contents[-1]}')

            sorted_contents = filtered_contents
            sorted_contents.sort()
            # print(f'  Sortered {len(sorted_contents)} entries.')
            # print(f'{"  Line 0:":>12} {sorted_contents[0]}')
            # print(f'  Line [-1]: {sorted_contents[-1]}')

            # Step 3: Tokenize contents.
            tokenized_contents = []
            for line in sorted_contents:
                # print(f'\n  Before split: {len(tokenized_contents)}.')
                tokens = line.split(',')
                # print(f'  {tokens = }')
                tokenized_contents.append(tokens)
                # print(f'  After split: {len(tokenized_contents)}.')

            # Step 3b Sort on date.
            tokenized_contents.sort(key=lambda row: row[0])
            print(
                f'\n  first/last tokens:\n  {"  Line 0:":>12} {tokenized_contents[0]}')
            print(f'  Line [-1]: {tokenized_contents[-1]}')

            # Step 3c: Get start and end dates.
            start_date = tokenized_contents[0][0]
            end_date = tokenized_contents[-1][0]
            print(f'\n  Span: {start_date} => {end_date}')

            # # Step 3c: Sort on activity.
            # # tokenized_contents.sort(key=lambda row: row[1])
            # print(
            #     f'\n  first/last tokens, sorted:\n  {"  Line 0:":>12} {tokenized_contents[0]}')
            # print(f'  Line [-1]: {tokenized_contents[-1]}')
            # start_date = tokenized_contents[0][0]
            # end_date = tokenized_contents[-1][0]
            # print(f'\n  Span: {start_date} => {end_date}')

            # Step 4: Translate from etrade to gsheet.
            gsheet = translate(tokenized_contents, crossRef)

            # Step 5: Save new file:
            write(acct_no, start_date, end_date, gsheet)
            # dst_file = f'output/{acct_no}-{start_date}-{end_date}.csv'
            # print(f'  Writing output file: "{dst_file}".')
            # with open(dst_file, mode='w', encoding='utf8') as outfile:
            #     outfile.write('\n'.join(str(line) for line in tokenized_contents))

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
