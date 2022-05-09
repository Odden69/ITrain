"""
In this module, format methods in Python's built in HTMLCalendar class is
overridden to contain the planned sessions.

This module is copied in its whole from
https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html
with only a few modifications to fit the ITrain app
"""
# from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Session


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, sessions):
        sessions_per_day = sessions.filter(date__day=day)
        d = ''
        for session in sessions_per_day:
            d += f'<li> {session.get_html_url} </li>'

        if day != 0:
            return f'<td><span class="date">{day}</span><ul> {d} </ul></td>'
        return '<td class="mark"></td>'

    def formatweek(self, theweek, sessions):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, sessions)
        return f'<tr> {week} </tr>'

    def formatmonth(self, withyear=True):
        sessions = Session.objects.filter(date__year=self.year,
                                          date__month=self.month)
        month_name = self.formatmonthname(self.year, self.month,
                                          withyear=withyear)
        cal = '<table border="0" cellpadding="0" cellspacing="0" \
               class="calendar">\n'
        cal += f'{month_name}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, sessions)}\n'
        return cal
