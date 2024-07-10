import datetime as dt
import operator as op


def normalize_str_to_time(
    time_point: dt.time | str,
) -> dt.time:
    if isinstance(time_point, str):
        str_hour, str_minute, *_ = time_point.split(":")
        return dt.time(
            hour=int(str_hour),
            minute=int(str_minute),
        )
    return time_point


def normalize_str_to_date(
    date_point: dt.date | str,
) -> dt.date:
    if isinstance(date_point, str):
        str_year, str_month, str_day = date_point.split("-")
        return dt.date(
            year=int(str_year),
            month=int(str_month),
            day=int(str_day),
        )
    return date_point


def timedelta_seconds_to_time(timedelta: dt.timedelta) -> dt.time:
    return dt.time(
        hour=op.floordiv(timedelta.seconds, 60 * 60),
        minute=op.mod(op.floordiv(timedelta.seconds, 60), 60),
    )
