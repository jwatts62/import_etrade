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

# error_context = ''


def process_EQ(tail):
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


def process_MF(tail):
    """Process the 'tail' of a record as an activity on a
    Mutual Fund position.
    """
    pass
    return {}


def process_unknown(tail):
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
    """Extract fields from a record."""

    desc_ndx = 8
    error_context = f'\nRaw record:\n  >{rec}\n'
    rec = rec.strip()

    platform = 'eTrade'
    account = ''
    Date = ''
    activity = 'Dividend'   # Dividend, Interest, Transfer
    invest_type = ''
    symbol = ''
    description = ''
    manager = ''
    quantity = ''
    price = ''
    cost = ''
    fee = ''
    foreign_tax = ''

    contents = {}
    m = gross_exp.match(rec)
    if m:
        error_context += (f'  Matched {len(m.groups())} captures:\n')
        for g in m.groups():
            error_context += (f'    Matched >{g}<\n')

        Date = m.group(1).strip()
        invest_type = m.group(3).strip()
        symbol = m.group(4).strip()

        if invest_type in position_processors:
            position_processors[invest_type](m.group(9))
            print(error_context)

        # if invest_type == 'EQ':
        #     # print('EQ')
        #     m = EQ_exp.match(rec)
        #     if m:
        #         error_context += (
        #             f'\n  EQ expression matched {len(m.groups())} captures:\n')
        #         for g in m.groups():
        #             error_context += (f'    Matched >{g}<\n')
        #         print(f'Decoding EQ:\n{error_context}')
        #     pass

        # elif invest_type == 'MF':
        #     # print('MF')
        #     m = MF_exp.match(rec)
        #     if m:
        #         error_context += (
        #             f'\n  MF expression matched {len(m.groups())} captures:\n')
        #         for g in m.groups():
        #             error_context += (f'    Matched >{g}<\n')
        #     pass

        # else:
        #     pass

        # description = m.group(9).strip()
        # manager = m.group(10).strip()
        # quantity = ''
        # price = ''
        # cost = ''
        # fee = ''
        # foreign_tax = ''

        # print(f'  group[{desc_ndx}] >{m.group(desc_ndx)}<')
        # description=m.group(desc_ndx)
        error_context += (f'\n>>>{description}<\n')
        # ndx=description.find('  ')
        # if ndx > 0:
        #     desc=description[:ndx].strip()
        # print(f'Desc: >{desc}<')
        # ndx = description.find('  ', ndx+2)
        # if ndx > 0:
        #     tail = description[ndx:].strip()
        #     error_context += (
        #         f'\n  line: >{rec}<\n'
        #         f'  desc: >{description}<\n'
        #         f'  tail: >{tail}<\n')

        #     # REINVEST?
        #     # ndx = tail.find('REINVEST PRICE $')
        #     # if ndx >= 0:
        #     #     print('***: REINVEST PRICE $')
        #     m = reinvest_exp.search(tail)
        #     if m:
        #         pass
        #         print(f'reinvest: {m.group(1)}')

        #     else:
        #         m = record_exp.match(tail)
        #         if m:
        #             pass
        #             print(f'rec {m.group(1)}; pay: {m.group(1)}')

        #         else:
        #             m = reinvest_exp.match(tail)
        #             if m:
        #                 pass
        #                 print(f'reinvest: {m.group(1)}')

        #             else:
        #                 if st_cg_exp.match(tail):
        #                     pass
        #                     print(
        #                         f'Short Term Capita; Gains.@@@@@@@@@@@@@@@@@@@@')

        #                 else:
        #                     if lt_cg_exp.match(tail):
        #                         pass
        #                         print(
        #                             f'Long Term Capita; Gains.@@@@@@@@@@@@@@@@@@@@')

        #                     elif tail == 'FIDELITY INVESTMENTS':
        #                         pass
        #                         print('Fidelity Investments.')

        # else:
        #     error_context += (
        #         '\n***************************\n'
        #         'unidentified transaction\n'
        #         # f'  line: >{rec}<\n'
        #         # f'  tail: >{tail}<\n'
        #         '***************************\n')
        #     print(error_context)

    else:
        print(f'Failed to match gross expression.')
        print(error_context)

    contents = {platform, account, Date, activity, invest_type, symbol,
                description, manager, quantity, price, cost, fee, foreign_tax}
    return contents


def read_file(fn) -> Tuple[str, List[str]]:
    """ Read a file into a list of lines.
    Returns a tuple containing the account number and a list
    of lines.
    """

    acct_no = ''
    lines_read = []

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

    #
    # 12/20/19,Dividend,MF,NSIDX,0.324,-4.29,0,0,NORTHERN SMALL CAP INDEX      NORTHERN FUNDS                REINVEST PRICE $ 13.23
    # 12/20/19, Dividend, MF, NSIDX, 3.028, -40.06, 0, 0, NORTHERN SMALL CAP INDEX      NORTHERN FUNDS                REINVEST PRICE $ 13.23
    #
    # date, transaction, instrument type, symbol, quantity, amount, price, commision, description
    #

        # gross_exp = re.compile(
        #     # '^([^,]),([^,]),([^,]),([^,]),([^,]),([^,]),([^,]),([^,]),(.*)$')
        #     '^([\\d/]{8}),(\w+),(EQ|MF),(\w+),((?:\+|\-)?\d+(?:.\d+)?),((?:\+|\-)?\d+(?:.\d+)?),((?:\+|\-)?\d+(?:.\d+)?),(.*)$', re.ASCII)
        # # detail_exp = re.compile(' +(\w(?: \w+))+')

        # # 'RECORD 02/28/19 PAY 02/28/19'
        # record_exp = re.compile(
        #     'RECORD (\d\d/\d\d/\d\d) PAY (\d\d/\d\d/\d\d)')

        # # 'REINVEST PRICE $  8.48'
        # reinvest_exp = re.compile(
        #     'REINVEST PRICE \$\s*(\d+\.\d+)')

        # # 'S/T CAPITAL GAIN              RECORD 12/27/19 PAY 12/30/19'
        # st_cg_exp = re.compile(
        #     'S/T CAPITAL GAIN\s+RECORD (\d\d/\d\d/\d\d) PAY (\d\d/\d\d/\d\d)')

        # # 'L/T CAPITAL GAIN              RECORD 12/27/19 PAY 12/30/19'
        # lt_cg_exp = re.compile(
        #     'L/T CAPITAL GAIN\s+RECORD (\d\d/\d\d/\d\d) PAY (\d\d/\d\d/\d\d)')

        trading_log = [()]
        # desc_ndx = 8
        ln = 0
        for line in lines[4:]:
            ln = ln + 1

            # print(f'  Line {ln}:\n    [{line[:-1]}]')
            rec = parse_record(line)
            if rec:
                trading_log.append(rec)

            else:
                print(f'\nERROR *** ERROR *** ERROR\n'
                      f'Parse failed on line {ln}:\n{line}\n'
                      f'ERROR *** ERROR *** ERROR\n')

            # line = line.strip()
            # ln = ln + 1
            # m = gross_exp.match(line)
            # if m:
            #     # print(f'\nMatched {len(m.groups())} captures:')
            #     # for g in m.groups():
            #     #     print(f'    Matched >{g}<')

            #     # print(f'  group[{desc_ndx}] >{m.group(desc_ndx)}<')
            #     description = m.group(desc_ndx)
            #     # print(f'\n>>>{description}<')
            #     ndx = description.find('  ')
            #     if ndx > 0:
            #         desc = description[:ndx].strip()
            #         # print(f'Desc: >{desc}<')
            #         ndx = description.find('  ', ndx+2)
            #         if ndx > 0:
            #             tail = description[ndx:].strip()
            #             print(
            #                 f'\n  line: >{line}<\n'
            #                 f'  desc: >{description}<\n'
            #                 f'  tail: >{tail}<')

            #             # REINVEST?
            #             # ndx = tail.find('REINVEST PRICE $')
            #             # if ndx >= 0:
            #             #     print('***: REINVEST PRICE $')
            #             m = reinvest_exp.search(tail)
            #             if m:
            #                 pass
            #                 print(f'reinvest: {m.group(1)}')

            #             else:
            #                 m = record_exp.match(tail)
            #                 if m:
            #                     pass
            #                     print(f'rec {m.group(1)}; pay: {m.group(1)}')

            #                 else:
            #                     m = reinvest_exp.match(tail)
            #                     if m:
            #                         pass
            #                         print(f'reinvest: {m.group(1)}')

            #                     else:
            #                         if st_cg_exp.match(tail):
            #                             pass
            #                             print(
            #                                 f'Short Term Capita; Gains.@@@@@@@@@@@@@@@@@@@@')

            #                         else:
            #                             if lt_cg_exp.match(tail):
            #                                 pass
            #                                 print(
            #                                     f'Long Term Capita; Gains.@@@@@@@@@@@@@@@@@@@@')

            #                             elif tail == 'FIDELITY INVESTMENTS':
            #                                 pass
            #                                 print('Fidelity Investments.')

            #                             else:
            #                                 print(
            #                                     '\n***************************')
            #                                 print('unidentified transaction')
            #                                 print(f'  line {ln}: >{line}<')
            #                                 print(f'  tail: >{tail}<')
            #                                 print('***************************')

            #             # m = detail_exp.search(tail)
            #             # # m = detail_exp.search(line)
            #             # if m:

            #             #     # ndx = description.find('  ', ndx+2)
            #             #     # if ndx > 0:
            #             #     trans = m.group(1).strip()
            #             #     print(f'trans: >{trans}<')

            # else:
            #     print('ERROR ### ERROR ### ERROR ### ERROR ### ERROR ### ERROR')
            #     print(f'Failed to parse line:\n>{line[:-1]}<')
            #     print('ERROR ### ERROR ### ERROR ### ERROR ### ERROR ### ERROR')
            #     return (acct_no, lines_read)

        return (acct_no, lines_read)


if __name__ == '__main__':
    srcFile = "./data/transactions.csv"
    contents = read_file(srcFile)
    print('\n\n\n', contents[:12])
