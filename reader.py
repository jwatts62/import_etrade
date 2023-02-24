"""This module provides the means to read and return the
contents of a file as a sequence of strings.
"""
from typing import Dict, List, Tuple


def recordSymbol(symbol: str, name: str, xRef: Dict[str, str]):
    """Record a symbol and name.
    """

    if not symbol in xRef:
        xRef[symbol] = name.strip('*')
        print(f'Symbol: "{symbol}: {name}.')


def read(fn: str) -> List[str]:
    """ Read a file exported from eTrade into a list of lines.

    fn - filename;
    Returns a list of lines.
    """

    lines = []

    with open(fn, mode='r', encoding='utf8') as source_file:
        for line in source_file:
            line = line.strip()
            if line:
                lines.append(line)
        # print(f'Read {len(lines)} lines.')

    return lines


def write(acct_no: str, start_date: str, end_date: str, contents: List[List[str]]) -> bool:
    """Write an output file.
    """
    date = start_date.replace('/', '.')
    dst_file = f'output/{acct_no}-{date.replace("/", ".")}-{end_date.replace("/", ".")}.csv'
    print(f'  Writing output file: "{dst_file}".')
    with open(dst_file, mode='w', encoding='utf8') as outfile:
        outfile.write('\n'.join(str(line)for line in contents))


# End of File
