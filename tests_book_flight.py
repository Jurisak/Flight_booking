#!/usr/bin/python3
import unittest
from argparse import ArgumentTypeError
from book_flight import valid_date, query_api, book_flight, book_ticket
from book_flight import APIQueryException


class MyTestCase(unittest.TestCase):
    PNR_CODE_SIZE = 7

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
        result = book_ticket('')
        self.assertEqual('confirmed', result['status'])
        self.assertRaises(APIQueryException, book_ticket, 'UNKNOWN')

    def test_one_way_flight(self):
        query_data = query_api('https://api.skypicker.com/flights?', {'flyFrom': 'BCN', 'to': 'DUB',
                                                                      'dateFrom': '01/12/2017'})
        pnr = book_flight(query_data)
        self.assertEqual(len(pnr), self.PNR_CODE_SIZE)


if __name__ == '__main__':
    unittest.main()
