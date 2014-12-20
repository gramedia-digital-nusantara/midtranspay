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
    '''
    if amount not in [None, '']:
        # only IDR supported -- so split off the fractional portion
        amt_str = amount.split('.')[0]
        return int(amt_str)
    else:
        return 0