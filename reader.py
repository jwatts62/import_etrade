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
        lines = source_file.readlines()
        # print(f'Read {len(lines)} lines.')

    return lines

# End of File
