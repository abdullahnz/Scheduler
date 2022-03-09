#!/usr/bin/python3

from calendar import calendar
from ics import Calendar, Event
import datetime, arrow
import json, sys

# https://stackoverflow.com/questions/42950/how-to-get-the-last-day-of-the-month
def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)
    
def parse_hour(time):
    return map(int, time.split(':'))

def process_time(date, time, counter = 0):
    hour, minute, second = parse_hour(time)
    return arrow.get(datetime.datetime(year=date[0], day=date[1], month=date[2],
                                    hour=hour, minute=minute, second=second))

schedule = json.loads(open('data.json', 'rb').read())['aaData']

current_date = datetime.datetime.now()

year  = current_date.year
day   = current_date.day - datetime.datetime.today().weekday()
month = current_date.month

calendar = Calendar()
prev_day = 'SENIN'

n_weeks = int(sys.argv[1]) if len(sys.argv) > 1 else 1

for _ in range(n_weeks):
    for data in schedule:
        if prev_day != data[0]:
            prev_day = data[0]
            day += 1

        month_range = last_day_of_month(datetime.date(year, month, 1)).day
        
        if day > month_range:
            day = day % month_range
            month += 1

        if month > 12:
            month = 1
            year += 1

        event = Event()
        event.name  = f'{data[4]} ({data[5]})'
        event.description = f'''Ruang: {data[2]}\nKelas: {data[6]}\nCourse ID: {data[3]}'''
        event.begin = process_time((year, day, month), data[1])
        event.end   = process_time((year, day, month), data[7])

        calendar.events.add(event)

with open('schedule.ics', 'w') as scheduler:
    scheduler.writelines(calendar)