'''Test LASParser Module'''
import unittest

class TestLASParser(unittest.TestCase):
    '''Test LasParser Class'''

    # preparing to test
    def setUp(self):
        ''' Setting up for the test '''
        #LASParser()

    def test_getSection_Exception(self):
        '''Test Ascii Block Section Permutations'''
        self.assertEqual(LASParser.getSection("B"), "B")

    def test_parseSectionLine_Exception(self):
        '''Test Ascii Block Section Permutations'''
        self.assertEqual(LASParser.parseSectionLine('~Test_Section[1]'),
            'TEST_SECTION')
        self.assertEqual(LASParser.parseSectionLine('~'),
            '')
        self.assertEqual(LASParser.parseSectionLine(''),
            None)

    def test_parseLAS_Comment(self):
        '''Test Ascii Block Section Permutations'''
        self.assertEqual(next(LASParser().parseLAS(['#test'])),
            ('COMMENT', '#test'))

    def test_parseLAS_Blank(self):
        '''Test Ascii Block Section Permutations'''
        self.assertEqual(next(LASParser().parseLAS([' ']), None),
            None)

    def test_parseParameterLine_General(self):
        '''Test General Paramater Permutations'''
        self.assertEqual(LASParser.parseParameterLine(
            "DATE .       13/12/1986  : LOG DATE  {DD/MM/YYYY}"),
            ('DATE', '', '13/12/1986', 'LOG DATE  {DD/MM/YYYY}', ''))
        self.assertEqual(LASParser.parseParameterLine(
            "RUN_DATE.     22/09/1998  : Run 1 date  {DD/MM/YYYY}     | Run[1]"),
            ('RUN_DATE', '', '22/09/1998', 'Run 1 date  {DD/MM/YYYY}', 'Run[1]'))
        self.assertEqual(LASParser.parseParameterLine(
            " UTM  .                                        : UTM LOCATION"),
            ('UTM', '', '', 'UTM LOCATION', ''))

    def test_parseLAS_WellBlock_Null(self):
        '''Test Well Block Section Key Parameters'''
        parser = LASParser()
        parser.current_section = 'WELL'
        parser.line_type = 'PARAMETER'
        self.assertEqual(
            next(parser.parseLAS(['NULL.  -999.25000: null'])),
            ('WELL', ('NULL', '', '-999.25000', 'null', ''))
        )
        self.assertEqual(parser.NULL, '-999.25000')

    def test_parseLAS_CurveBlock(self):
        '''Test Curve Block Section Curve Parameters'''
        parser = LASParser()
        parser.current_section = 'CURVE'
        parser.line_type = 'PARAMETER'
        self.assertEqual(
           next(parser.parseLAS(["RHOB.G/C3                 :   Bulk Density"])),
            ('CURVE', ('RHOB', 'G/C3', '', 'Bulk Density', '')))
        self.assertEqual(parser.curves, ['RHOB'])

    def test_getSection_AsciiSectionReturned(self):
        '''Test Ascii Block Section Permutations'''
        self.assertEqual(LASParser.getSection("A"), "ASCII")

    def test_parseParameterLine_Curves(self):
        '''Test Curve Block Section Permutations'''
        self.assertEqual(LASParser.parseParameterLine(
            "RHOB.G/C3                 :   Bulk Density"),
            ('RHOB', 'G/C3', '', 'Bulk Density', ''))

    def test_parseParameterLine_AsciiSectionReturned(self):
        '''Test Ascii Block Section Permutations'''
        pass

    # ending the test
    def tearDown(self):
        '''Cleaning up after the test'''
        pass


# pylint: disable=too-many-instance-attributes
if __name__ == '__main__':
    import sys
    import os
    sys.path.append(
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.path.pardir, "src")
        )
    )
    from pdh.library.las_parser import LASParser, LASParseError
    unittest.main()
    pass
else:
    from pdh.library.las_parser import LASParser, LASParseError
