#!/bin/python3

"""_summary_
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
from typing import List, Tuple
import re

from pprint import pprint

# error_context = ''

xactions = {}


def process_EQ(tail, accum):
    """Process the 'tail' of a record as an activity on an
    Equity position.
    """
    pass
    error_context = ''
    m = EQ_exp.match(tail)
    if m:
        error_context += (
            f'\n  EQ expression matched {len(m.groups())} captures:\n')
        for g in m.groups():
            error_context += (f'    Matched >{g}<\n')
        print(f'Decoding EQ:\n{error_context}')

    return {}


def process_MF(tail, accum):
    """Process the 'tail' of a record as an activity on a
    Mutual Fund position.
    """
    pass
    return {}


def process_unknown(tail, accum):
    """Process the 'tail' of a record as an activity on an
    unknown position.
    """
    pass
    return {}


# from gzip import _OpenTextMode
# ([\\d/]{8}),(\w+),(EQ|MF),(\w+),((?:\+|\-)?\d+(?:.\d+)?)
# 10/01/19,Dividend,MF,WMFAX,0,5.96,0,0,WELLS FARGO MUNICIPAL BOND A  WELLS FARGO FUNDS             RECORD 09/30/19 PAY 09/30/19
gross_exp = re.compile(
    # 10/01/19,Dividend,MF,WMAF
    '^([\d/]{8}),'                                  # 1 - Date.
    # 2 - Activity: Bought, Dividend, Transfer.
    '(\w+),'
    # 3 - investment type: Equity or Mutual Fund.
    '(EQ|MF|UNKNOWN),'
    '([ A-Z]+),'                                     # 4 - Investment symbol.
    '((?:\+|\-)?\d+(?:\.\d+)?),'                    # 5 - 0.
    '((?:\+|\-)?\d+(?:\.\d+)?),'                    # 6 - Amount: 5.96.
    '((?:\+|\-)?\d+(?:\.\d+)?),'                    # 7 - 0.
    '((?:\+|\-)?\d+(?:\.\d+)?),'                    # 8 - 0.
    # # 9 - Investment description  e.g. 'WELLS FARGO MUNICIPAL BOND A'.
    # '([A-Z? ]{30})'
    # # 10 - Investment manager e.g. 'WELLS FARGO FUNDS'.
    # # '([A-Z]+(?: [A-Z]+)?)(?: *)'
    '(.*)$',                                         # 9 - Transaction details
    re.ASCII)

MF_exp = re.compile(
    # 1 - Investment description  e.g. 'WELLS FARGO MUNICIPAL BOND A'.
    '([A-Z? ]{30})'
    # 2 - Investment manager e.g. 'WELLS FARGO FUNDS'.
    '([A-Z]+(?: [A-Z]+)?)(?: *)'
    '(.*)',                                         # 3 -
    re.ASCII)

EQ_exp = re.compile(
    # 9 - Investment description  e.g. 'WELLS FARGO MUNICIPAL BOND A'.
    '([A-Z? ]{30})'
    # 10 - Investment manager e.g. 'WELLS FARGO FUNDS'.
    # '([A-Z](?: [A-Z]+))(?: *)'
    '(.*)',                                         # 11 -
    re.ASCII)

# 12/31/21,Dividend,EQ,CSWC,5.81305,-145.5,0,0,CAPITAL SOUTHWEST CORP        REIN @  25.0299               REC 12/15/21 PAY 12/31/21


# 'RECORD 02/28/19 PAY 02/28/19'
record_exp = re.compile(
    'RECORD (\d\d/\d\d/\d\d) PAY (\d\d/\d\d/\d\d)')

# 'REINVEST PRICE $  8.48'
reinvest_exp = re.compile(
    'REINVEST PRICE \$\s*(\d+\.\d+)')

# 'S/T CAPITAL GAIN              RECORD 12/27/19 PAY 12/30/19'
st_cg_exp = re.compile(
    'S/T CAPITAL GAIN\s+RECORD (\d\d/\d\d/\d\d) PAY (\d\d/\d\d/\d\d)')

# 'L/T CAPITAL GAIN              RECORD 12/27/19 PAY 12/30/19'
lt_cg_exp = re.compile(
    'L/T CAPITAL GAIN\s+RECORD (\d\d/\d\d/\d\d) PAY (\d\d/\d\d/\d\d)')

position_processors = {'EQ': process_EQ,
                       'MF': process_MF,
                       'UNKNOWN': process_unknown
                       }


def parse_record(rec) -> Tuple:
    """Extract fields from a record.
    Returns a tuple:
        (Date, activity, invest_type, symbol, description,
         manager, quantity, value, Commission, foreign_tax)
    """

    error_context = f'\nRaw record:\n  >{rec}\n'
    rec = rec.strip()

    # platform = 'eTrade'
    # account = ''
    Date = ''
    activity = ''   # Dividend, Interest, Transfer
    invest_type = ''
    symbol = ''
    description = ''
    manager = ''
    quantity = ''
    value = ''
    price = ''
    Commission = ''
    foreign_tax = ''

    contents = ()
    m = gross_exp.match(rec)
    if m:
        error_context += (f'  Matched {len(m.groups())} captures:\n')
        for g in m.groups():
            error_context += (f'    Matched >{g}<\n')

        Date = m.group(1).strip()
        activity = m.group(2).strip()
        invest_type = m.group(3).strip()
        symbol = m.group(4).strip()
        quantity = m.group(5).strip()
        value = m.group(6).strip()
        Commission = m.group(7).strip()

        if not invest_type in xactions:
            xactions[invest_type] = {}

        if not activity in xactions[invest_type]:
            xactions[invest_type][activity] = []

        xactions[invest_type][activity].append(m.group(9))
        if activity in xactions[invest_type]:
            position_processors[invest_type](
                m.group(9), xactions[invest_type][activity])

        error_context += (f'\n>>>{description}<\n')

    else:
        print(f'Failed to match gross expression.')
        print(error_context)
        return contents

    contents = (Date, activity, invest_type, symbol, description,
                manager, quantity, value, Commission, foreign_tax)
    # print(f'contents:\n  {contents}')
    return contents


def read_file(fn) -> Tuple[str, List[str]]:
    """ Read a file into a list of lines.
    Returns a tuple containing the account number and a list
    of lines:  (acct_no, trading_log)
    """

    acct_no = ''
    trading_log = []

    with open(fn, mode='r', encoding='utf8') as input:
        lines = input.readlines()
        print(f'Read {len(lines)} lines.')
        gross_exp = re.compile('####(\\d{4})$')
        m = gross_exp.search(lines[0])
        if m:
            print(f'Matches:\n  {m}')
            acct_no = m[1]
            print(f'Account number: {acct_no}')

        else:
            print(
                f'\nERROR\nFailed to extract account number from file header.\n  >{lines[0]}<')
            return (acct_no, lines_read)

        header = lines[:4]
        print(f'Header:\n{header}')

        # trading_log = [()]
        ln = 0
        for line in lines[4:]:
            ln = ln + 1

            # print(f'  Line {ln}:\n    [{line[:-1]}]')
            rec = parse_record(line)
            if rec:
                trading_log.append(rec)
                # print(f'New record:\n  {rec}\nLog:')
                # pprint(trading_log, indent=2)
                # print(f'\nFrom line:\n  {line.strip()}\n  New record: {rec}')

            else:
                print(f'\nERROR *** ERROR *** ERROR\n'
                      f'Parse failed on line {ln}:\n{line.strip()}'
                      f'ERROR *** ERROR *** ERROR\n')

        return (acct_no, trading_log)


def display_partial(data):
    """Display fragments of data."""
    print(f'data:\n{data}')
    print(f'Keys:')
    for datum in data:
        print(f'  {datum}')
    print(f'type(data): {type(data)}')
    print(f'\nPartial contents:')
    for nv_type in data:
        print(f'type(nv_type): {type(nv_type)}')
        print(f'{data.index(nv_type)}: {nv_type}')
        # print(f'{data[nv_type]}')


if __name__ == '__main__':
    srcFile = "./data/transactions.csv"
    contents = read_file(srcFile)
    print(f'\n\n\n{contents[0]}; {contents[1]}')
    # pprint(xactions, indent=2)
    display_partial(contents)
