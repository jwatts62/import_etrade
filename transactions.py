"""
Define transaction records.
Transaction records contain:
     0: Date;
     1: activity - See ACTIVITIES below;
     2: invest_type - See INVESTMENT_TYPES below;
     3: symbol
     4: description
     5: manager
     6: quantity
     7: price
     8: value
     9: fee
    10: foreign_tax

"""

ACTIVITIES = ['Buy', 'Sell', 'Dividend',
              'Return of Capital', 'Interest', 'Transfer']

# EQ = Equity
# MF = Mutual Fund
INVESTMENT_TYPES = ['EQ', 'MF']

DIVIDEND_TYPES = ['Ordinary', 'Qualified']

CAPITAL_GAIN_TYPES = ['Short Term', 'Long Term']


#
