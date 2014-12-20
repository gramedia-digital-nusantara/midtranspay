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