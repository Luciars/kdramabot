import calendar
from datetime import datetime

def humanize_date(time: datetime) -> str:
    current_time = datetime.now()

    if time.minute < 10:
        min = "0" + str(time.minute)
    else:
        min = str(time.minute)

    if time.year > current_time.year:
        return "next year on %s %s" % (calendar.month_name[time.month], time.day)
    if time.date() == current_time.date() and current_time.time() < time.time():
        if time.hour < 18:
            return "today at %s:%s" % (time.hour, min)
        else:
            return "tonight at %s:%s" % (time.hour, min)

    return "%s %s at %s:%s" % (calendar.month_name[time.month], time.day, time.hour, min)
