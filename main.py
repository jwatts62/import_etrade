#!/bin/python3

"""
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
# import re
from sys import exit

from pprint import pprint


# from import_etrade import read
# from decoders import Decoders
# from reader import read
from etrade_reader import translate_etrade_file


def import_records(src, dec):
    """Invoke the appropriate decoder to read and import records.
    """
    file_contents = read_file(srcFile, dec)
    return file_contents


if __name__ == '__main__':
    """Translate an eTrade file.

    Returns 0 if successful, or False otherwise.
    """

    ROOT_FOLDER = './data/'
    # srcFile = f'{ROOT_FOLDER}transactions.csv'
    # srcFile = f'{ROOT_FOLDER}2641-Q4-2022.csv'
    srcFile = f'{ROOT_FOLDER}2641-Q3-2022.csv'
    xRef = dict()
    if translate_etrade_file(srcFile, xRef):
        pprint(xRef)
        print('Success')

    else:
        print('Failure')
        exit(255)

    exit(0)
