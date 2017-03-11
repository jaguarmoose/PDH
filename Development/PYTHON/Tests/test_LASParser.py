"""Test LASParser Module"""

import unittest

class TestLASParser(unittest.TestCase):
    """Test LasParser Class"""

    # preparing to test
    def setUp(self):
        """ Setting up for the test """
        pass

    def test_getSection_AsciiSectionReturned(self):
        """Test Ascii Block Section Permutations"""
        self.assertEqual(LASParser.getSection("A"), "ascii")

    # ending the test
    def tearDown(self):
        """Cleaning up after the test"""
        pass


if __name__ == '__main__':
    import sys
    from os import path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from Lib.LASParser import LASParser, LASParseError
    unittest.main()
else:
    from ..Lib.LASParser import LASParser,LASParseError
