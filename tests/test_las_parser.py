'''Test LASParser Module'''
import unittest


class TestLASParser(unittest.TestCase):
    '''Test LasParser Class'''

    # preparing to test
    def setUp(self) -> None:
        ''' Setting up for the test '''
        #LASParser()

    def test_get_section_exception(self) -> None:
        '''Test Ascii Block Section Permutations'''
        self.assertEqual(LASParser.get_section("B"), "B")

    def test_parse_section_line_exception(self) -> None:
        '''Test Ascii Block Section Permutations'''
        self.assertEqual(LASParser.parse_section_line('~Test_Section[1]'),
            'TEST_SECTION')
        self.assertEqual(LASParser.parse_section_line('~'),
            '')
        self.assertEqual(LASParser.parse_section_line(''),
            None)

    def test_parse_las_comment(self) -> None:
        '''Test Ascii Block Section Permutations'''
        self.assertEqual(next(LASParser().parse_las(['#test'])),
            ('COMMENT', '#test'))

    def test_parse_las_blank(self) -> None:
        '''Test Ascii Block Section Permutations'''
        self.assertEqual(next(LASParser().parse_las([' ']), None),
            None)

    def test_parse_parameter_line_general(self) -> None:
        '''Test General Paramater Permutations'''
        self.assertEqual(LASParser.parse_parameter_line(
            "DATE .       13/12/1986  : LOG DATE  {DD/MM/YYYY}"),
            ('DATE', '', '13/12/1986', 'LOG DATE  {DD/MM/YYYY}', ''))
        self.assertEqual(LASParser.parse_parameter_line(
            "RUN_DATE.     22/09/1998  : Run 1 date  {DD/MM/YYYY}     | Run[1]"),
            ('RUN_DATE', '', '22/09/1998', 'Run 1 date  {DD/MM/YYYY}', 'Run[1]'))
        self.assertEqual(LASParser.parse_parameter_line(
            " UTM  .                                        : UTM LOCATION"),
            ('UTM', '', '', 'UTM LOCATION', ''))

    def test_parse_las_well_block_null(self) -> None:
        '''Test Well Block Section Key Parameters'''
        parser = LASParser()
        parser.current_section = 'WELL'
        parser.line_type = 'PARAMETER'
        self.assertEqual(
            next(parser.parse_las(['NULL.  -999.25000: null'])),
            ('WELL', ('NULL', '', '-999.25000', 'null', ''))
        )
        self.assertEqual(parser.NULL, '-999.25000')

    def test_parse_las_curve_block(self) -> None:
        '''Test Curve Block Section Curve Parameters'''
        parser = LASParser()
        parser.current_section = 'CURVE'
        parser.line_type = 'PARAMETER'
        self.assertEqual(
           next(parser.parse_las(["RHOB.G/C3                 :   Bulk Density"])),
            ('CURVE', ('RHOB', 'G/C3', '', 'Bulk Density', '')))
        self.assertEqual(parser.curves, ['RHOB'])

    def test_get_section_ascii_section_returned(self) -> None:
        '''Test Ascii Block Section Permutations'''
        self.assertEqual(LASParser.get_section("A"), "ASCII")

    def test_parse_parameter_line_curves(self) -> None:
        '''Test Curve Block Section Permutations'''
        self.assertEqual(LASParser.parse_parameter_line(
            "RHOB.G/C3                 :   Bulk Density"),
            ('RHOB', 'G/C3', '', 'Bulk Density', ''))

    def test_parse_parameter_line_ascii_section_returned(self) -> None:
        '''Test Ascii Block Section Permutations'''
        pass

    # ending the test
    def tearDown(self) -> None:
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
