from logic import *
import datetime, unittest

class LogicTest(unittest.TestCase):
    def test_num_to_roman(self):
        values = [1, -1, 5, 9, 18, 23]
        expected = ['I', '-I', 'V', 'IX', 'XVIII', 'XXIII']
        for i in range(len(values)):        
            self.assertEqual(num_to_roman(values[i]), expected[i])

    def test_shorttime_to_datetime(self):
        self.assertEqual(shorttime_to_datetime('20180101'),
                         datetime.datetime(year=2018, month=1, day=1))

    def test_datetime_to_shorttime(self):
        self.assertEqual(datetime_to_shorttime(
            datetime.datetime(year=1990, month=2, day=2)), '19900202')

if __name__ == '__main__':
    unittest.main()
