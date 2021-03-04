import icalendar
import uuid
from datetime import datetime
import pytz

cst = pytz.timezone('Asia/Shanghai')


class Calendar(icalendar.Calendar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add('prodid', '-//CDFMLR//coursesical//CN')
        self.add('VERSION', '2.0')
        self.add('X-WR-CALNAME', 'coursesical')
        self.add('X-APPLE-CALENDAR-COLOR', '#ff5a1d')
        self.add('X-WR-TIMEZONE', 'Asia/Shanghai')

    def add_event(self, event):
        self.add_component(event)


# def fCalendar():
#     cal = icalendar.Calendar()

#     cal.add('prodid', '-//CDFMLR//coursesical//CN')
#     cal.add('VERSION', '2.0')
#     cal.add('X-WR-CALNAME', 'coursesical')
#     cal.add('X-APPLE-CALENDAR-COLOR', '#ff5a1d')
#     cal.add('X-WR-TIMEZONE', 'Asia/Shanghai')

#     return cal


class Event(icalendar.Event):
    def __init__(self,
                 summary: str, start: datetime, end: datetime, location: str, description: str,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add('SUMMARY', summary)
        self.add('LOCATION', location)
        self.add('DESCRIPTION', description)
        self.add('DTSTART', datetime(start.year, start.month, start.day,
                                     start.hour, start.minute, start.second, tzinfo=cst))
        self.add('DTEND', datetime(end.year, end.month, end.day,
                                   end.hour, end.minute, end.second, tzinfo=cst))
        self.add('SEQUENCE', '0')
        self.add('UID', str(uuid.uuid3(uuid.NAMESPACE_DNS, f'{summary}{str(uuid.uuid4())}')))

    def alarm(self, before_minutes: int):
        alarm = icalendar.Alarm()

        alarm.add('UID', str(uuid.uuid3(
            uuid.NAMESPACE_DNS,
            str(self["summary"]) + str(uuid.uuid4()) + str(before_minutes)
        )))
        alarm.add('ACTION', 'DISPLAY')
        alarm['TRIGGER'] = f'-PT{before_minutes}M'
        alarm.add('DESCRIPTION', '提醒事项')

        self.add_component(alarm)

        return self

    def weekly_repeat(self, until: datetime):
        self.add('rrule', {'freq': 'WEEKLY',
                           'INTERVAL': 1,
                           'UNTIL': until})
        return self

