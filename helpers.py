from datetime import datetime, date
from dateutil import relativedelta
import random
from flask import redirect, session
from functools import wraps

today = datetime.today().date()

def main():
    print("Here")

def randomize4Digits():
    return random.randint(1000,9999)

def today_date():
    return today.strftime("%Y-%m-%d")

def count_months(start):
    startD = date.fromisoformat(start)
    r = relativedelta.relativedelta(today, startD)
    print(r.months + (r.years * 12))
    return r.months + (r.years * 12)

def negative_days(start):
    startD = date.fromisoformat(start)
    r = relativedelta.relativedelta(startD, today)
    return r.days

def negative_months(start):
    startD = date.fromisoformat(start)
    r = relativedelta.relativedelta(startD, today)
    return r.months

def past_sick_date(list):
    final = []

    for i in list:
        if negative_days(i['NextSickDate']) < 0 or negative_months(i['NextSickDate']) < 0:
            final.append(i)

    return final

def past_vacation_date(list):
    final = []

    for i in list:
        if negative_days(i['NextVacationDate']) < 0 or negative_months(i['NextVacationDate']) < 0:
            final.append(i)

    return final

def add_a_month(dat):
    theDate = date.fromisoformat(dat)
    month = relativedelta.relativedelta(months=1)
    print(theDate + month)
    return theDate + month


def add_six_months(dat):
    datas = date.fromisoformat(dat)
    months = relativedelta.relativedelta(months=6, day=31)
    six = datas + months
    print(six)
    return six

def add_n_months(dat, num):
    datas = date.fromisoformat(dat)
    months = relativedelta.relativedelta(months=num)
    return datas + months

def find_the_last_day(dat):
    datas = date.fromisoformat(dat)
    months = relativedelta.relativedelta(day=31)
    return datas + months

def next_month_last_day(dat):
    datas = date.fromisoformat(dat)
    months = relativedelta.relativedelta(months=1, day=31)
    print(datas + months)
    return datas + months

def findTime(dat, hours):
    months = count_months(dat)
    print(months)

    if months >= 6 and months <= 18:
        hours += 3
    elif months >= 19 and months <=42:
        hours += 6
    elif months > 42:
        hours += 9

    if hours >= 240:
        return 240
    else:
        return hours

def vacation_time(months):
    total = 0
    for i in range(6, months):
        if i >= 6 and i <= 18:
            total += 3
        elif i >= 19 and i <= 42:
            total += 6
        elif 42 < i:
            total += 9

        print(f"{i} -> {total}")
    if total > 240:
        total = 240
    return total

if __name__ == "__main__":
    main()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/")
        return f(*args, **kwargs)

    return decorated_function
