import datetime as dt
from zoneinfo import ZoneInfo


CPH_TIMEZONE = ZoneInfo("Europe/Copenhagen")


def ensure_local_copenhagen_datetime(value) -> dt.datetime:
    if isinstance(value, dt.datetime):
        local_dt = value
    else:
        local_dt = dt.datetime.fromisoformat(str(value))

    if local_dt.tzinfo is not None:
        return local_dt.astimezone(CPH_TIMEZONE)

    return local_dt.replace(tzinfo=CPH_TIMEZONE)


def get_aula_utc_offset(local_dt) -> str:
    localized = ensure_local_copenhagen_datetime(local_dt)
    offset = localized.strftime("%z")
    return f"{offset[:3]}:{offset[3:]}"


def format_aula_datetime(local_dt, include_timezone=True) -> str:
    localized = ensure_local_copenhagen_datetime(local_dt)
    formatted = localized.strftime("%Y-%m-%dT%H:%M:%S")
    if not include_timezone:
        return formatted

    return f"{formatted}{get_aula_utc_offset(localized)}"
