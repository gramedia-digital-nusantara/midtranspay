from datetime import datetime


VERITRANS_DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

def parse_veritrans_datetime(vt_datetime):
    '''
    Given an input string, returns a datetime representation.
    Assumes the veritrans documented datetime format of Y-m-d H:M:S.
    If no datetime provided, returns None.
    '''
    return (datetime.strptime(vt_datetime, VERITRANS_DATE_TIME_FORMAT)
            if vt_datetime
            else None)

def parse_veritrans_amount(amount):
    '''
    Given an input string, returns it as an integer.  Veritrans returns
    an extra .00 appended to the end of every string, we strip that off
    because IDR is the only supported currency.

    If None or an empty string is provided, 0 is returned.
    '''
    if amount not in [None, '']:
        # only IDR supported -- so split off the fractional portion
        amt_str = amount.split('.')[0]
        return int(amt_str)
    else:
        return 0
