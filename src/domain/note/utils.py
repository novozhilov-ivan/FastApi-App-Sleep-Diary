import datetime as dt
import operator as op


def timedelta_seconds_to_time(timedelta: dt.timedelta) -> dt.time:
    return dt.time(
        hour=op.floordiv(timedelta.seconds, 60 * 60),
        minute=op.mod(op.floordiv(timedelta.seconds, 60), 60),
    )
