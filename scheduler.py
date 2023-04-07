#!/usr/bin/python3
  
from icalendar import Calendar, Event
import datetime, argparse
import json 

class Scheduler:
    DAYS = {
        'SENIN'  : 0,   'SELASA' : 1,
        'RABU'   : 2,   'KAMIS'  : 3,
        'JUMAT'  : 4,   'SABTU'  : 5,
    }

    def __init__(self, filename = None):
        current_date = datetime.datetime.now()
        
        self.filename = "data.json" if filename == None else filename
        self.year  = current_date.year
        self.day   = current_date.day - datetime.datetime.today().weekday()
        self.month = current_date.month
        self.prev  = "SENIN"

    def parse_time(self, time):
        hour, minute, second = map(int, time.split(':'))
        return datetime.datetime(year=self.year, day=self.day, month=self.month,
                                    hour=hour, minute=minute, second=second)
        
    def last_day_of_month(self, date):
        if date.month == 12:
            return date.replace(day=31)
        return date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)

    def check_date(self, course_day):
        range_day_of_month = self.last_day_of_month(datetime.date(self.year, self.month, 1)).day
        
        if self.prev != course_day:
            self.day += self.DAYS.get(course_day) - \
                        self.DAYS.get(self.prev)

        if self.day > range_day_of_month:
            self.day = self.day % range_day_of_month
            self.month += 1

        if self.month > 12:
            self.month = 1
            self.year += 1

        return course_day
    
    def parse(self, verbose, outfile):
        schedule = open(self.filename, 'rb').read()
        schedule = json.loads(schedule)['aaData']

        calendar = Calendar()
       
        for course_day, start, room, course_id, course, lecturer_id, grade, end, stat in schedule:
            self.prev = self.check_date(course_day)

            summary = f'{course} ({lecturer_id})'
            description    = f'Ruang: {room} | Kelas: {grade} | Course ID: {course_id}'
            weekly_freq = {'freq': 'weekly'}
            
            event = Event()
            event.add('summary', summary)
            event.add('description', description)
            event.add('dtstart', self.parse_time(start))
            event.add('dtend', self.parse_time(end))
            event.add('rrule', weekly_freq)
            
            if verbose:
                print(f'Adding event {course} in {course_day} at {start} - {end} ({self.day}-{self.month}-{self.year})')
            
            calendar.add_component(event)

        with open(outfile, 'wb') as scheduler:
            scheduler.write(calendar.to_ical())

if __name__ == "__main__":
    scheduler = Scheduler(filename = 'data.json')
    scheduler.parse(outfile = 'schedule.ics', verbose = True)
    