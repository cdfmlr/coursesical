# from coursesical.course import *
from course import *


def test0():
    t = TimeTable([("08:00", "10:10")])
    s = Semester("2021-03-01", t)
    r = RawCourse(
        name="通用魔法理论基础(2)",
        group="(下课派:DD23333；疼逊会议)",
        teacher="伊蕾娜",
        zc="1-16(周)",
        classroom="王立瑟雷斯特利亚",
        weekday=0,
        time=0,
        text="""71010223-1
        通用魔法理论基础(2)
        (下课派:DD23333；疼逊会议)
        伊蕾娜
        1-16(周)
        王立瑟雷斯特利亚
        """
    )

    c = Course(s, r)
    print(c.name, c.class_begin, c.class_over, c.until)
    print(new_course(s, r))

def test1():
    t = TimeTable([("08:00", "09:40"), ("10:00", "11:40"), ("14:30", "16:10"), ("16:30", "18:10"), ("19:30", "21:10")])
    s = Semester("2021-03-01", t)
    r = RawCourse(
        name="形势与政策(20212)",
        group="",
        teacher="思政",
        zc="12,14-16(周)",
        classroom="教三十楼B座709",
        weekday=1,
        time=2,
        text="""71420212-41
        形势与政策(20212)
        思政
        12,14(周)
        教三十楼B座709
        星期六  第六大节
        """
    )

    for c in new_course(s, r):
        print(c.name, c.class_begin, c.class_over, c.until)
    print(new_course(s, r))

if __name__ == "__main__":
    print('---0:')
    test0()
    print('---1:')
    test1()