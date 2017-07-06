#!/usr/bin/python3
import unittest

from argparse import ArgumentTypeError

from book_flight import valid_date, query_api, book_flight, book_ticket
from book_flight import APIQueryException, get_flights


class ArgparseObject:
    cheapest = False
    date = '13/10/2017'
    fly_from = 'BCN'
    one_way = True
    return_days = 0
    shortest = False
    to = 'DUB'


class MyTestCase(unittest.TestCase):
    PNR_CODE_SIZE = 7
    SHORTEST_FLIGHT_ID = '322685545'
    CHEAPEST_FLIGHT_ID = '322687923|322692335'

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

    def test_shortest_flight(self):
        args = ArgparseObject()
        args.shortest = True
        flights = get_flights(args)
        pnr = book_flight(flights)
        self.assertEqual(len(pnr), self.PNR_CODE_SIZE)
        self.assertEqual(flights['data'][0]['id'], self.SHORTEST_FLIGHT_ID)

    def test_cheapest_flight(self):
        args = ArgparseObject()
        args.cheapest = True
        flights = get_flights(args)
        pnr = book_flight(flights)
        self.assertEqual(len(pnr), self.PNR_CODE_SIZE)
        self.assertEqual(flights['data'][0]['id'], self.CHEAPEST_FLIGHT_ID)

    def test_return_flight(self):
        args = ArgparseObject()
        args.return_days = 5
        flights = get_flights(args)
        pnr = book_flight(flights)
        self.assertEqual(len(pnr), self.PNR_CODE_SIZE)
        self.assertEqual(flights['data'][0]['id'], self.CHEAPEST_FLIGHT_ID)

if __name__ == '__main__':
    unittest.main()
