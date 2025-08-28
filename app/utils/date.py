import datetime

def str_to_datetime(**kwargs):
    result = ()
    for value in kwargs.values():
        if value:
            if "T" in value:
                value = value.replace("T", " ")

            if isinstance(value, datetime.datetime):
                result += (value,)
            else:
                result += (datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S"),)
        else:
            result += (None,)
    return result if len(result) > 1 else result[0]


def str_to_date(**kwargs):
    result = ()
    for value in kwargs.values():
        if value:
            if isinstance(value, datetime.datetime):
                result += (value,)
            else:
                result += (datetime.datetime.strptime(value, "%Y-%m-%d").date(),)
        else:
            result += (None,)
    return result if len(result) > 1 else result[0]


def str_to_time(**kwargs):
    result = ()
    for value in kwargs.values():
        if value:
            if isinstance(value, datetime.datetime):
                result += (value,)
            else:
                result += (datetime.datetime.strptime(value, "%H:%M").time(),)
        else:
            result += (None,)
    return result if len(result) > 1 else result[0]