from datetime import datetime


VERITRANS_DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def parse_veritrans_datetime(vt_datetime):
    '''
    Takes a string representing a date and time, in the format
    returned by Veritrans, and returns a python datetime instance.

    :param vt_datetime: String in format yyyy-mm-dd hh:mm:ss.
    :type vt_datetime: :py:class:`str`
    :rtype: :py:class:`datetime`
    '''
    return (datetime.strptime(vt_datetime, VERITRANS_DATE_TIME_FORMAT)
            if vt_datetime
            else None)


def parse_veritrans_amount(amount):
    '''
    Given an input string, returns it as an integer.  Veritrans returns
    an extra .00 appended to the end of every string, we strip that off
    because IDR is the only supported currency.

    :param amount: A string representing a numeric amount, with fractional
        currency amounts separated by '.' (NOT ,).
    :type amount: :py:class:`str`
    :rtype: :py:class:`int`
    '''
    if amount not in [None, '']:
        # only IDR supported -- so split off the fractional portion
        amt_str = amount.split('.')[0]
        return int(amt_str)
    else:
        return 0
