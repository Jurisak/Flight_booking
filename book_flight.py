import requests
import json
import argparse
from datetime import datetime


def book_flight(booking_token):
    passenger = dict(
        title='Mr',
        firstName='Franta',
        documentID='',
        birthday='2000-01-01',
        email='frantik@fitvut.cz',
        lastName='Frantik')
    data = dict(currency='EUR',
                booking_token=booking_token,
                passengers=passenger)
    response = query_api('http://37.139.6.125:8080/booking', data, 'POST')
    print(response)
    return response


class APIQueryException(Exception):
    pass


def query_api(url, url_options, method='GET'):
    header = {"Content-type": "application/json"}
    try:
        response = requests.get(url, params=url_options)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as detail:
        raise APIQueryException("ERROR: Unable to access url '{0}' with given options '{1}'."
                                "With these details: '{2}'".format(url, url_options, detail))


def valid_date(s):
    """
    Function for date format validation

    :param s -- input date time
    :return date in api format or raises an exception
    """
    try:
        return datetime.strptime(s, "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Booking flights using skypicker API'
    )
    parser.add_argument(
        '--date',
        required=True,
        type=valid_date,
        help='Flight date in YYYY-MM-DD format.'
    )
    parser.add_argument(
        '--from',
        dest='fly_from',
        required=True,
        help='Flight from place.'
    )
    parser.add_argument(
        '--to',
        required=True,
        help='Flight to destination.'
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--one-way',
        action='store_true',
        default=True,
        help='Random one way flight.'
    )
    group.add_argument(
        '--return',
        type=int,
        default=0,
        help='Random one way flight.'
    )
    group.add_argument(
        '--cheapest',
        action='store_true',
        help='Pick cheapest one way flight.'
    )
    group.add_argument(
        '--shortest',
        action='store_true',
        help='Pick shortest one way flight.'
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    query_data = query_api('https://api.skypicker.com/flights?', {'flyFrom': 'LHR', 'to': 'DXB',
                                                                  'dateFrom': args.date})

    # book_flight(query_data['data'][1]['booking_token'])
    print(args)
