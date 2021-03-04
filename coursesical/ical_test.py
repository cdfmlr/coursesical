# from coursesical.ical import *
from ical import *


def display(cal):
    print(cal.to_ical().decode().replace('\r\n', '\n').strip())


def test0():
    cal1 = Calendar()
    event1 = Event(summary="like",
                   location="it",
                   start=datetime(2021, 3, 4, 8, 23, 0),
                   end=datetime(2021, 3, 4, 8, 44, 31),
                   description="23333333"
                   )
    event1.alarm(0)
    event1.alarm(10)
    event1.weekly_repeat(until=datetime(2021, 4, 4, 8, 44, 31))

    cal1.add_component(event1)

    display(cal1)


if __name__ == "__main__":
    test0()