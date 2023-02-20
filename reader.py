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

    try:
        with open(fn, mode='r', encoding='utf8') as source_file:
            # lines = source_file.readlines()
            for line in source_file:
                lines.append(line.strip())
        # print(f'Read {len(lines)} lines.')
    except FileNotFoundError:
        lines = []
        print(
            f'*** ERROR: {__name__}("{fn}") => File not found for file named "{fn}".')

    return lines

# End of File
