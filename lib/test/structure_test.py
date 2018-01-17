from structure import *
import datetime, unittest

class RepresentationTest(unittest.TestCase):
    def test_enum_to_int(self):
        self.assertEqual(Representation.NUMERIC, 0)
        self.assertEqual(Representation.ROMAN, 1)
        self.assertEqual(Representation.SMALL_ROMAN, 2)
        self.assertEqual(Representation.UPPERCASE, 3)
        self.assertEqual(Representation.LOWERCASE, 4)

    def test_numeric_representation(self):
        self.assertEqual(num_to_representation(3, Representation.NUMERIC), 3)

    def test_roman_representation(self):
        self.assertEqual(num_to_representation(3, Representation.ROMAN), 'III')

    def test_small_roman_representation(self):
        self.assertEqual(num_to_representation(3, Representation.SMALL_ROMAN), 'iii')

    def test_uppercase_representation(self):
        self.assertEqual(num_to_representation(3, Representation.UPPERCASE), 'C')

    def test_lowercase_representation(self):
        self.assertEqual(num_to_representation(3, Representation.LOWERCASE), 'c')

    def test_num_to_roman(self):
        values = [1, -1, 5, 9, 18, 23]
        expected = ['I', '-I', 'V', 'IX', 'XVIII', 'XXIII']
        for i in range(len(values)):        
            self.assertEqual(num_to_roman(values[i]), expected[i])

class StructureTest(unittest.TestCase):
    def setUp(self):
        self.date_2011 = datetime.datetime(year=2011, month=1, day=1)
        self.date_2012 = datetime.datetime(year=2012, month=1, day=1)
        self.diff_2012 = [Diff(DiffType.ADD, position=4, add='u'),
                          Diff(DiffType.REMOVE, position=4, remove=1)]
        self.sample_structure = Structure(1, Representation.NUMERIC, 'Title',
                                          dates=[self.date_2011, self.date_2012],
                                          texts={self.date_2011: 'Hello',
                                                 self.date_2012: 'Hellu'},
                                          diffs={self.date_2011: [],
                                                 self.date_2012: self.diff_2012})
    
    def test_short_str(self):
        self.assertEqual(self.sample_structure.short_str(), 'Title 1')

    def test_has_children(self):
        self.assertEqual(self.sample_structure.has_children(), False)

    def test_get_text_at(self):
        text_at_2011 = self.sample_structure.get_text_at(datetime.datetime(year=2011, month=2, day=1))
        text_at_2018 = self.sample_structure.get_text_at(datetime.datetime(year=2018, month=2, day=1))
        self.assertEqual(text_at_2011.texts[self.date_2011], 'Hello')
        self.assertEqual(text_at_2018.texts[self.date_2012], 'Hellu')                         
                
if __name__ == '__main__':
    unittest.main()
