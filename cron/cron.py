
"""Gevent based crontab implementation"""
# Reference https://stackoverflow.com/a/2946908/5341800
# © Hackeron
from datetime import datetime, timedelta
import gevent

# Some utility classes / functions first
def conv_to_set(obj):
    """Converts to set allowing single integer to be provided"""

    if isinstance(obj, (int, )):
        return set([obj])  # Single item
    if not isinstance(obj, set):
        obj = set(obj)
    return obj

class AllMatch(set):
    """Universal set - match everything"""
    def __contains__(self, item): 
        return True

allMatch = AllMatch()

class Event(object):
    """The Actual Event Class"""

    def __init__(self, action, minute=allMatch, hour=allMatch, 
                       day=allMatch, month=allMatch, daysofweek=allMatch, 
                       args=(), kwargs={}):
        self.mins = conv_to_set(minute)
        self.hours = conv_to_set(hour)
        self.days = conv_to_set(day)
        self.months = conv_to_set(month)
        self.daysofweek = conv_to_set(daysofweek)
        self.action = action
        self.args = args
        self.kwargs = kwargs

    def matchtime(self, t1):
        """Return True if this event should trigger at the specified datetime"""
        return ((t1.minute     in self.mins) and
                (t1.hour       in self.hours) and
                (t1.day        in self.days) and
                (t1.month      in self.months) and
                (t1.weekday()  in self.daysofweek))

    def check(self, t):
        """Check and run action if needed"""

        if self.matchtime(t):
            self.action(*self.args, **self.kwargs)

class CronTab(object):
    """The crontab implementation"""

    def __init__(self, *events):
        self.events = events

    def _check(self):
        """Check all events in separate greenlets"""

        t1 = datetime(*datetime.now().timetuple()[:5])
        for event in self.events:
            gevent.spawn(event.check, t1)

        t1 += timedelta(minutes=1)
        s1 = (t1 - datetime.now()).seconds + 1
        print("Checking again in %s seconds" % s1)
        job = gevent.spawn_later(s1, self._check)

    def run(self):
        """Run the cron forever"""

        self._check()
        while True:
            gevent.sleep(60)

import os 
def email_task():
    """Just an example that sends a bell and asd to all terminals"""
    # os.system('date; echo nice;')
    os.system('date; python3 /code/deans_api/manage.py runcrons  >> /var/log/cron.log')  

cron = CronTab(
  Event(email_task, [0 ,
1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10 ,11 ,12 ,13 ,14 ,15 ,16 ,17 ,18 ,19 ,20 ,21 ,22 ,23 ,24 ,25 ,26 ,27 ,28 ,29 ,30 ,31 ,32 ,33 ,34 ,35 ,36 ,37 ,38 ,39 ,40 ,41 ,42 ,43 ,44 ,45 ,46 ,47 ,48 ,49 ,50 ,51 ,52 ,53 ,54 ,55 ,56 ,57 ,58 ,59 ,
  ] ),
)
cron.run()