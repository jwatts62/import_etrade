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

# from gzip import _OpenTextMode
import re
from typing import List, Tuple


gross_exp = re.compile(
    # '^([^,]),([^,]),([^,]),([^,]),([^,]),([^,]),([^,]),([^,]),(.*)$')
    '^([\\d/]{8}),(\w+),(EQ|MF),(\w+),((?:\+|\-)?\d+(?:.\d+)?),((?:\+|\-)?\d+(?:.\d+)?),((?:\+|\-)?\d+(?:.\d+)?),(.*)$', re.ASCII)
# detail_exp = re.compile(' +(\w(?: \w+))+')

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


def parse_record(rec):
    """Extract fields from a record."""
    desc_ndx = 8
    rec = rec.strip()
    contents = {}
    m = gross_exp.match(rec)
    if m:
        # print(f'\nMatched {len(m.groups())} captures:')
        # for g in m.groups():
        #     print(f'    Matched >{g}<')

        # print(f'  group[{desc_ndx}] >{m.group(desc_ndx)}<')
        description = m.group(desc_ndx)
        # print(f'\n>>>{description}<')
        ndx = description.find('  ')
        if ndx > 0:
            desc = description[:ndx].strip()
            # print(f'Desc: >{desc}<')
            ndx = description.find('  ', ndx+2)
            if ndx > 0:
                tail = description[ndx:].strip()
                print(
                    f'\n  line: >{rec}<\n'
                    f'  desc: >{description}<\n'
                    f'  tail: >{tail}<')

                # REINVEST?
                # ndx = tail.find('REINVEST PRICE $')
                # if ndx >= 0:
                #     print('***: REINVEST PRICE $')
                m = reinvest_exp.search(tail)
                if m:
                    pass
                    print(f'reinvest: {m.group(1)}')

                else:
                    m = record_exp.match(tail)
                    if m:
                        pass
                        print(f'rec {m.group(1)}; pay: {m.group(1)}')

                    else:
                        m = reinvest_exp.match(tail)
                        if m:
                            pass
                            print(f'reinvest: {m.group(1)}')

                        else:
                            if st_cg_exp.match(tail):
                                pass
                                print(
                                    f'Short Term Capita; Gains.@@@@@@@@@@@@@@@@@@@@')

                            else:
                                if lt_cg_exp.match(tail):
                                    pass
                                    print(
                                        f'Long Term Capita; Gains.@@@@@@@@@@@@@@@@@@@@')

                                elif tail == 'FIDELITY INVESTMENTS':
                                    pass
                                    print('Fidelity Investments.')

                                else:
                                    print(
                                        '\n***************************')
                                    print('unidentified transaction')
                                    print(f'  line: >{rec}<')
                                    print(f'  tail: >{tail}<')
                                    print('***************************')


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
                print(f'\nERROR *** ERROR *** ERROR')
                print(f'Parse failed on line {ln}:\n{line}')
                print(f'ERROR *** ERROR *** ERROR\n')

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
    srcFile = "./data/TxnHistory.csv"
    contents = read_file(srcFile)
    print('\n\n\n', contents[:12])
