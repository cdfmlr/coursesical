from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List
import re
from copy import copy


@dataclass
class RawCourse:
    """
    教务系统获取的课程表
    """
    name: str
    group: str  # 就是课堂派，它源码里 title 写的是 "分组名称"
    teacher: str
    zc: str
    classroom: str
    weekday: int
    time: int  # 第几节课
    text: str  # 那个框里完整的内容

    def get_zc(self) -> str:
        """周次，后面不要带 "(周)"
        """
        return re.sub(re.escape("(周)") + '$', '', self.zc)


def _split_rawcourse(course: RawCourse) -> List[RawCourse]:
    """这个函数把 zc="12,14(周)" 这种周次有逗号的 Course 分成多个课。
    """
    cs = []
    for z in course.get_zc().split(","):
        c = copy(course)
        c.zc = z
        cs.append(c)
    return cs


class TimeTable:
    """作息时间表
    """
    @dataclass
    class ClassTime:
        """一大节课
        """
        start: str
        end: str

    classes: List[ClassTime]

    def __init__(self, classes: list) -> None:
        """
        classes: [("08:00", "10:00"), ...]
        """
        self.classes = list(map(
            lambda c: TimeTable.ClassTime(start=c[0], end=c[1]),
            classes
        ))

    def __getitem__(self, index):
        return self.classes[index]


class Semester:
    """ 学期
    first_monday: "YYYY-MM-DD", 学期开始的第一周周一
    """

    def __init__(self, first_monday: str, time_table: TimeTable) -> None:
        self.first_monday = first_monday
        self.time_table = time_table

        # time_format = "%Y-%m-%d"
        # self.start_datetime = datetime.strptime(first_monday, time_format)


class Course:
    """ Course (View Model) for iCal

    # 课程

    class_begin, class_over 为首次上课时间；
    若 until != None 则每周重复，直到 until。
    """

    semester: Semester
    name: str
    teacher: str
    classroom: str
    class_begin: datetime
    class_over: datetime
    until: datetime = None  # None to not repeat
    description: str

    def __init__(self, semester: Semester, course: RawCourse) -> None:
        # emmm, 这个方法很爆炸啦，懒得重构
        self.semester = semester
        self.name = course.name
        self.teacher = course.teacher
        self.classroom = course.classroom
        self.description = course.text

        # zc 有两种可能: a-b or a
        zc = course.get_zc()
        try:
            first = int(zc)
            repeat = False
        except:
            first, last = re.findall("(\d+)-(\d+)", zc)[0]
            first, last = int(first), int(last)
            repeat = True

        semester_start = datetime.strptime(semester.first_monday, "%Y-%m-%d")

        first_class_date = semester_start + \
            timedelta(days=7) * (first - 1) + \
            timedelta(days=course.weekday)

        if repeat:
            self.until = semester_start + \
                timedelta(days=7) * (last - 1) + \
                timedelta(days=course.weekday + 1)

        class_time: TimeTable.ClassTime = semester.time_table[course.time]

        s = datetime.strptime(class_time.start, "%H:%M")
        e = datetime.strptime(class_time.end, "%H:%M")

        self.class_begin = first_class_date + \
            timedelta(hours=s.hour, minutes=s.minute)
        self.class_over = first_class_date + \
            timedelta(hours=e.hour, minutes=e.minute)


def new_course(semester: Semester, course: RawCourse) -> List[Course]:
    return list(map(
        lambda r: Course(semester, r),
        _split_rawcourse(course)
    ))
