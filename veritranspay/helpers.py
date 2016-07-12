from datetime import datetime


VERITRANS_DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def parse_veritrans_datetime(vt_datetime):
    """ Takes a string representing a date and time, in the format returned by Veritrans, and returns a python datetime instance.

    :param `six.string_types|None` vt_datetime: String in format yyyy-mm-dd hh:mm:ss.
    :rtype: datetime
    """
    return (datetime.strptime(vt_datetime, VERITRANS_DATE_TIME_FORMAT) if vt_datetime else None)


def parse_veritrans_amount(amount):
    """ Parsers a given Veritrans 'currency amount' string (returned by the API) into an integer.

    Veritrans returns an extra .00 appended to the end of every string, we strip that off
    because IDR is the only supported currency.

    .. note::

        Veritrans does not use the standard Indonesian format for representing numbers with a fractional
        portion (comma as the fractional separator, period as the thousands separator).  Instead it uses the US-style
        (period as the fractional separator, comma as the thousands separator).

    :param `six.string_types|None` amount:
        A string representing a numeric amount, with fractional currency amounts separated by '.' (NOT ',').
    :rtype: int
    """
    if amount not in [None, '']:
        # only IDR supported -- so split off the fractional portion
        amt_str = amount.split('.')[0]
        return int(amt_str)
    else:
        return 0
