from datetime import date, time


def normalize_str_to_time(
    time_point: time | str,
) -> time:
    if isinstance(time_point, str):
        str_hour, str_minute, *_ = time_point.split(":")
        return time(
            hour=int(str_hour),
            minute=int(str_minute),
        )
    return time_point


def normalize_str_to_date(
    date_point: date | str,
) -> date:
    if isinstance(date_point, str):
        str_year, str_month, str_day = date_point.split("-")
        return date(
            year=int(str_year),
            month=int(str_month),
            day=int(str_day),
        )
    return date_point
