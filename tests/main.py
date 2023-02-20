"""Main/Root module for all unit tests.
"""

import unittest
import sys

from tests.test_reader import test_read
from tests.test_etrade import test_etrade


def main():

    # unittest.main(verbosity=2)
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    unittest.TextTestRunner(verbosity=3).run(suite)


if __name__ == '__main__':
    main()

# End of File
