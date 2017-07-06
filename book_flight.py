#!/usr/bin/python3
import requests
import json
import argparse

from datetime import datetime


class APIQueryException(Exception):
    pass


class FlightBookingException(Exception):
    pass


def book_ticket(booking_token):
    """
    Function for booking ticket in a specific flight

    :param booking_token: Unique id of flight in which the ticket will be booked
    :return: result of query_api function
    """
    passenger = dict(
        title='Mr',
        firstName='Franta',
        documentID='',
        birthday='2000-01-01',
        email='Novak@fitvut.cz',
        lastName='Novak')
    booking_data = dict(currency='EUR',
                        booking_token=booking_token,
                        passengers=passenger)
    return query_api('http://37.139.6.125:8080/booking', booking_data, False)


def book_flight(possible_flights):
    """
    Function for booking single flight

    :param possible_flights: dictionary of queried flights
    :return: booked ticket PNR code or exception when all flights are occupied
    """
    for flight in possible_flights['data']:
        ticket = book_ticket(flight['booking_token'])
        if ticket['status'] == 'confirmed':
            return ticket['pnr']
    raise FlightBookingException("ERROR: Unable to find free flight. Ticket was not booked."
                                 "Please try different date.")


def query_api(url, url_options, get_method=True):
    """
    Function for querying api with given params

    :param url: API url
    :param url_options: API options
    :param get_method: Boolean value which indicates whether it is a get or post api call
    :return: queried data in dictionary or raises exception in case of any problem
    """
    header = {"Content-type": "application/json"}
    try:
        if get_method:
            response = requests.get(url, url_options, headers=header)
        else:
            response = requests.post(url, json.dumps(url_options), headers=header)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as detail:
        raise APIQueryException("ERROR: Unable to access url '{0}' with given options '{1}'."
                                "With these details: '{2}'".format(url, url_options, detail))


def get_flights(args):
    """
    Function for finding relevant flights according to input arguments

    :param args: input arguments
    :return: dictionary of relevant flights
    """
    flight_params = dict(flyFrom=args.fly_from, to=args.to, dateFrom=args.date, dateTo=args.date,
                         typeFlight='oneway')
    if args.shortest:
        flight_params['sort'] = "duration"
    elif args.cheapest:
        flight_params['sort'] = 'price'
    elif args.return_days > 0:
        flight_params['typeFlight'] = 'round'
        flight_params['daysInDestinationTo'] = args.return_days
    return query_api('https://api.skypicker.com/flights?', flight_params)


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
        dest='return_days',
        default=0,
        help='Pick rounded flight according to given days in destination.'
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
    flights = get_flights(parse_args())
    print(book_flight(flights))
