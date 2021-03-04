from coursesical.jw import *
from coursesical.course import *
from coursesical.ical import *

# from jw import *
# from course import *
# from ical import *

# 默认的时间表
DEFAULT_TIME_TABLE = [("08:00", "09:40"),
                      ("10:00", "11:40"),
                      ("14:30", "16:10"),
                      ("16:30", "18:10"),
                      ("19:30", "21:10")]


def courses_from_table(semester: Semester, courses_table) -> List[Course]:
    """把教务爬虫拿到的数据转换成 Course
    courses_table: [[{"name": "通用魔法理论", "teacher": "...", ...}, {course@Tues}, ...星期x], ...第x大节]
    """
    courses = []

    for session, cs in enumerate(courses_table):  # session：“节次”（第x大节）
        for weekday, c in enumerate(cs):
            if not c:
                continue
            courses.extend(new_course(
                semester=semester,
                course=RawCourse(
                    name=c.get("name", ""),
                    group=c.get("group", ""),
                    teacher=c.get("teacher", ""),
                    zc=c.get("zc", ""),
                    classroom=c.get("classroom", ""),
                    weekday=weekday,
                    time=session,
                    text=c.get("text", "")
                )
            ))
    courses = filter(lambda c: c.name, courses)

    return courses


def event_from_course(course: Course) -> Event:
    """课程转化成日历事件

    按照 course.until 的指示安排每周重复；

    设置两次提醒：上课前10分钟提醒一次，上课时提醒一次。
    """
    event = Event(summary=course.name,
                  location=course.classroom,
                  start=course.class_begin,
                  end=course.class_over,
                  description=course.description
                  )

    event.alarm(0)
    event.alarm(10)

    if course.until:
        event.weekly_repeat(course.until)

    return event


def main(sid: str, password: str,
         semester_first_monday: str, courses_time: list = DEFAULT_TIME_TABLE,
         output: str = "coursesical.ics"):
    """爬教务，取课表，析课程，写日历。
    """
    time_table = TimeTable(courses_time)
    semester = Semester(semester_first_monday, time_table)

    crawler = CourseTableCrawler(sid, password)
    cs = crawler.run()

    courses = courses_from_table(semester, courses_table=cs)

    cal = Calendar()
    for c in courses:
        cal.add_event(event_from_course(c))

    with open(output, "wb") as f:
        f.write(cal.to_ical())

