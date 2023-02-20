"""This module provides the means to read and return the
contents of a file as a sequence of strings.
"""
from typing import List, Tuple


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
    dst_file = f'output/{acct_no}-{start_date}-{end_date}.csv'
    print(f'  Writing output file: "{dst_file}".')
    with open(dst_file, mode='w', encoding='utf8') as outfile:
        outfile.write('\n'.join(str(line)for line in contents))


# End of File
