from src.domain.sleep_diary.values.points import Points


def convert_points_to_json(
    points: Points,
    timespec: str = "minutes",
) -> dict[str, str]:
    return {
        "bedtime_date": points.bedtime_date.isoformat(),
        "went_to_bed": points.went_to_bed.isoformat(timespec),
        "fell_asleep": points.fell_asleep.isoformat(timespec),
        "woke_up": points.woke_up.isoformat(timespec),
        "got_up": points.got_up.isoformat(timespec),
        "no_sleep": points.no_sleep.isoformat(timespec),
    }
