from datetime import datetime, timedelta
from collections import OrderedDict


def get_weekdays(start_date, end_date):
    if end_date > start_date:
        diff_days = (end_date - start_date).days
        current_day = start_date - timedelta(days=1)
        while current_day.date() < end_date.date():
            current_day = (
                current_day + timedelta(days=1)
                if current_day.weekday() != 4
                else current_day + timedelta(days=3)
            )

            yield current_day.date().strftime("%Y-%m-%d")

def get_monthlist():
    dates = ["1997-01-01", "2022-01-01"]
    start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
    data = list(OrderedDict(((start + timedelta(_)).strftime(r"1-%m-%y"), None) for _ in range((end - start).days)).keys())

    return data

def generate_dates(sentence):
    import re
    import calendar
    from datetime import datetime
    days = []
    regex = r"(\w{3}\s*-\s*\d*\d)"
    r = re.findall(regex, sentence)
    s = ",".join(r)
    dates = s.replace(" ", "").split(",")
    months = {
        month.lower(): index for index, month in enumerate(calendar.month_abbr) if month
    }

    for date in dates:
        month, day = date.split("-")
        month_index = months[month.lower()]
        year = sentence.split(" ")[0]
        day = datetime(int(year), month_index, int(day))
        days.append(day)
    return days