import datetime, time, functools


def get_col_widths(dataframe):
    # First we find the maximum length of the index column
    idx_max = max([len(str(s)) for s in dataframe.index.values] + [len(str(dataframe.index.name))])
    # Then, we concatenate this to the max of the lengths of column name and its values for each column, left to right
    return [idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]


def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string


def get_range(a, b, c, d):
    string = colnum_string(a) + str(b) + ':' + colnum_string(c) + str(d)
    return string


def sleeper(execution_time):
    now = datetime.datetime.now()
    start_date = (now + datetime.timedelta(days=1)).replace(hour=execution_time, minute=0)
    sleep_time = (start_date-now).seconds
    time.sleep(sleep_time)

def timer(sleep_time):
    def timer(func):
        @functools.wraps(func)
        def warpper(*args, **kwargs):
            sleeper(sleep_time, *args, **kwargs)
            func(*args, **kwargs)
        return warpper
    return timer


def lower_all_strings(col):
    if col.dtype == 'object':
        return col.str.lower()
    return col