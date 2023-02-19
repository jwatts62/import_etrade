

# from main import parse_record
from import_etrade import parse_record

# TransactionDate,TransactionType,SecurityType,Symbol,Quantity,Amount,Price,Commission,Description
transactions = [
    # ('12/31/21,Dividend,MF,BJBHX,0.854,-7.5,0,0,ABERDEEN GLOBAL HIGH INCOME A ABERDEEN                      REINVEST PRICE $  8.78',
    #  # Date activity invest_type symbol description manager quantity price value fee foreign_tax
    #  ('12/31/21', 'Buy', 'MF', 'BJBHX', 'ABERDEEN GLOBAL HIGH INCOME A', 'ABERDEEN', 0.854, 8.78, 7.5, 0.0, 0.0)),
    # ('12/31/21,Dividend,MF,BJBHX,0.715,-6.28,0,0,ABERDEEN GLOBAL HIGH INCOME A ABERDEEN                      REINVEST PRICE $  8.78',
    #  ('12/31/21', 'Buy', 'MF', 'BJBHX', 'ABERDEEN GLOBAL HIGH INCOME A', 'ABERDEEN', 0.715, 8.78, 6.28, 0.0, 0.0)),
    # ('12/31/21,Dividend,MF,BJBHX,0,7.5,0,0,ABERDEEN GLOBAL HIGH INCOME A ABERDEEN                      RECORD 12/29/21 PAY 12/31/21  DIVIDEND RATE      0.03782000',
    #  ('12/31/21', 'Dividend', 'MF', 'BJBHX', 'ABERDEEN GLOBAL HIGH INCOME A', 'ABERDEEN', 0.0, 0.0, 7.5, 0.0, 0.0)),
    # ('12/31/21,Dividend,MF,BJBHX,0,6.28,0,0,ABERDEEN GLOBAL HIGH INCOME A ABERDEEN                      RECORD 12/29/21 PAY 12/31/21  DIVIDEND RATE      0.03165000',
    #  ('12/31/21', 'Dividend', 'MF', 'BJBHX', 'ABERDEEN GLOBAL HIGH INCOME A', 'ABERDEEN', 0.0, 0.0, 6.28, 0.0, 0.0)),
    # ('12/31/21,Dividend,EQ,CSWC,0,145.5,0,0,CAPITAL SOUTHWEST CORP        CASH DIV  ON     150 SHS      REC 12/15/21 PAY 12/31/21     NON-QUALIFIED DIVIDEND',
    #  ('12/31/21', 'Dividend', 'EQ', 'CSWC', 'CAPITAL SOUTHWEST CORP', '', 0.0, 0.0, 145.5, 0.0, 0.0)),
    # '12/27/21,Interest,EQ,#2145605,0,0.05,0,0,EXTENDED INSURANCE SWEEP      DEPOSIT ACCOUNT               INTEREST',
    ('12/13/21,Dividend,EQ,MMM,0,35.78,0,0,3M COMPANY                    CASH DIV  ON                  24.17703 SHS                  REC 11/19/21 PAY 12/12/21',
     ('12/13/21', 'Dividend', 'EQ', 'MMM', '3M COMPANY', '', 0.0, 0.0, 35.78, 0.0, 0.0)),
    # '12/07/21,Fee,EQ,BIDU,0,-0.18,0,0,***BAIDU INC                  ADS 1 ADS REPRESENTING        8 SHARES                      ADR CUSTODY FEE',
    # '12/06/21,Sold,EQ,MMM,-0.17703,31.43,177.52,0,3M COMPANY',
    # '12/06/21,Sold,EQ,MMM,-24,4262.85,177.62,0,3M COMPANY',
    # '12/06/21,Sold,EQ,BIDU,-9,1269.62,141.07,0,***BAIDU INC                  ADS 1 ADS REPRESENTING        8 SHARES',
    # '12/06/21,Transfer,UNKNOWN,,0,2000,0,0,ACH DEPOSIT                   REFID:41257580906;',
    # '11/30/21,Dividend,MF,BJBHX,0.834,-7.27,0,0,ABERDEEN GLOBAL HIGH INCOME A ABERDEEN                      REINVEST PRICE $  8.72',
    # '11/30/21,Dividend,MF,BJBHX,0,7.27,0,0,ABERDEEN GLOBAL HIGH INCOME A ABERDEEN                      RECORD 11/26/21 PAY 11/30/21  DIVIDEND RATE      0.03681000',
    # '11/26/21,Interest,EQ,#2145605,0,0.01,0,0,EXTENDED INSURANCE SWEEP      DEPOSIT ACCOUNT               INTEREST',
    # '11/19/21,Dividend,EQ,MPLX,0,187.86,0,0,MPLX LP                       COM UNIT REPSTG LTD PARTNER   INT                           DIST      ON',
    # '11/19/21,Dividend,EQ,ET,0,39.36,0,0,ENERGY TRANSFER LP            COMMON UNITS REPRESENTING     LIMITED PARTNER INTERESTS     DIST      ON',
    # ('11/15/21,Dividend,EQ,ORCC,0,34.82,0,0,OWL ROCK CAPITAL CORPORATION  COMMON STOCK $0.01 PAR VALUE  PER SHARE                     CASH DIV  ON',
    #  ('11/15/21', 'Dividend', 'EQ', 'ORCC', 'OWL ROCK CAPITAL CORPORATION', 'COMMON STOCK', 0.0, 0.0, 35.78, 0.0, 0.0)),
    ('11/15/21,Dividend,EQ,OKE,0,87.14,0,0,ONEOK INC                     CASH DIV  ON                  93.19563 SHS                  REC 11/01/21 PAY 11/15/21',
     ('11/15/21', 'Dividend', 'EQ', 'OKE', '3M COMPANY', '', 0.0, 0.0, 35.78, 0.0, 0.0)),
    ('11/15/21,Dividend,EQ,ABBV,0,46,0,0,ABBVIE INC                    CASH DIV  ON                  35.38508 SHS                  REC 10/15/21 PAY 11/15/21',
     ('11/15/21', 'Dividend', 'EQ', 'ABBV', '3M COMPANY', '', 0.0, 0.0, 35.78, 0.0, 0.0)),
    # '11/12/21,Dividend,EQ,MMP,0,108.15,0,0,MAGELLAN MIDSTREAM PARTNERS LPUNIT REPSTG LTD PARTNER       DIST      ON                  104.24052 SHS',
    # '11/03/21,Bought,EQ,MO,75,-3331.25,44.4166,0,ALTRIA GROUP INC',
    # '11/01/21,Transfer,UNKNOWN,,0,3000,0,0,ACH DEPOSIT                   REFID:38282355906;',
    # '10/29/21,Dividend,MF,BJBHX,0.846,-7.49,0,0,ABERDEEN GLOBAL HIGH INCOME A ABERDEEN                      REINVEST PRICE $  8.85',
    # '10/29/21,Dividend,MF,BJBHX,0,7.49,0,0,ABERDEEN GLOBAL HIGH INCOME A ABERDEEN                      RECORD 10/27/21 PAY 10/29/21  DIVIDEND RATE      0.03806000',
    # '10/26/21,Interest,EQ,#2145605,0,0.01,0,0,EXTENDED INSURANCE SWEEP      DEPOSIT ACCOUNT               INTEREST',
    # '10/18/21,Bought,EQ,ASTR,250,-2292.5,9.17,0,ASTRA SPACE INC               CLASS A COMMON STOCK',
    # '10/14/21,Bought,EQ,BTI,100,-3589.7,35.897,0,***BRITISH AMERICAN TOBACCO   PLC SPONSORED ADR',
    # '10/14/21,Transfer,UNKNOWN,,0,5000,0,0,ACH DEPOSIT                   REFID:36907487906;',
    # '10/07/21,Bought,EQ,CSWC,150,-3917.25,26.115,0,CAPITAL SOUTHWEST CORP',
    # '10/07/21,Sold,EQ,AA,-105,4965.78,47.2935,0,ALCOA CORPORATION             COMMON STOCK',
    ('10/05/21,Dividend,EQ,QSR,0,-5.6,0,0,***RESTAURANT  Foreign Stk W/HINTERNATIONAL INC COM         CASH DIV  ON                  70.49701 SHS',
     ('10/05/21', 'Dividend', 'EQ', 'QSR', '3M COMPANY', '', 0.0, 0.0, 35.78, 0.0, 0.0)),
    ('10/05/21,Dividend,EQ,QSR,0,37.36,0,0,***RESTAURANT BRANDS          INTERNATIONAL INC COM         CASH DIV  ON                  70.49701 SHS',
     ('10/05/21', 'Dividend', 'EQ', 'QSR', '3M COMPANY', '', 0.0, 0.0, 35.78, 0.0, 0.0)),
    # '10/01/21,Dividend,EQ,HQH,3.02626,-79.53,0,0,TEKLA HEALTHCARE INVS         SH BEN INT                    REIN @  26.2800               REC 08/26/21 PAY 09/30/21',
    ('10/01/21,Dividend,EQ,HQH,0,79.53,0,0,TEKLA HEALTHCARE INVS         SH BEN INT                    CASH DIV  ON                  152.94349 SHS',
     ('10/01/21', 'Dividend', 'EQ', 'HQH', '3M COMPANY', '', 0.0, 0.0, 35.78, 0.0, 0.0)),
    # '09/30/21,Dividend,MF,BJBHX,0.819,-7.32,0,0,ABERDEEN GLOBAL HIGH INCOME A ABERDEEN                      REINVEST PRICE $  8.94',
    # '09/30/21,Dividend,MF,BJBHX,0,7.32,0,0,ABERDEEN GLOBAL HIGH INCOME A ABERDEEN                      RECORD 09/28/21 PAY 09/30/21  DIVIDEND RATE      0.03738000'
]


def doit():
    print('\n<*** doit ***>')
    is_passing = True
    for case in transactions:
        print(f'\n\n#########\n{case[0]}')
        res = parse_record(case[0])
        if res:
            print(f'\nInput:\n  >{case[0]}<\n'
                  '     date        action   type     symbol       description               qty price value fee tax\n'
                  f'  Parsed/Expected contents:\n  {res}\n  {case[1]}')
            # failed = not set(res).isdisjoint(set(case[1]))
            matches = (res == case[1])
            is_passing = is_passing and matches
            # passed = not len(set(res).difference(case[1]))
            # print(f'Passed: {case[1] == res}.')
            if matches:
                print(f'PASSed')
                # break

            else:
                print(f'FAILed')
                # break

        else:
            print(f'Failed at line:\n >{case[0]}<')
            # break

    print(f'\n\nAll cases passed: {is_passing}\nAll done.')
# if __name__ == '__main__':
#     srcFile = "./data/transactions.csv"
