import unittest
from argparse import ArgumentTypeError
from book_flight import valid_date, query_api, book_flight


class MyTestCase(unittest.TestCase):

    def test_data_validation(self):
        self.assertEqual(valid_date('2017-01-01'), '01/01/2017')
        self.assertEqual(valid_date('2017-12-01'), '01/12/2017')
        self.assertRaises(ArgumentTypeError, valid_date, '2017-13-01')
        self.assertEqual(valid_date('2017-12-31'), '31/12/2017')
        self.assertRaises(ArgumentTypeError, valid_date, '2017-12-32')

    def test_query_api(self):
        query_data = query_api('https://api.skypicker.com/flights?', {'flyFrom': 'BCN', 'to': 'DUB',
                                                                      'dateFrom': '01/12/2017'})
        self.assertEqual(query_data['_results'], 197)

    def test_naive_booking(self):
        result = book_flight('')

if __name__ == '__main__':
    unittest.main()
