from datetime import datetime


def load_datestring(datestring, prefix=''):
    """Based on a prefix return a dict with the date_key and time_key"""
    first_date = datetime.fromisoformat('2014-01-01')
    date_ = datetime.strptime(datestring, '%m/%d/%Y %H:%M')

    date_id = date_ - first_date

    time_ = 1000 + date_.hour * 60 + date_.minute
    date_and_time = {
        prefix + 'date': date_id.days,
        prefix + 'time': time_
    }

    return date_and_time
