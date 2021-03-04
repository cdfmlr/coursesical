# from coursesical.main import *
# from coursesical.course import *
# from coursesical.course import TimeTable
from main import *
from course import *


data = [
    [
        {'name': '通用魔法理论基础(2)', 'group': '(疼逊会议)', 'teacher': '伊蕾娜',
         'zc': '1-16(周)', 'classroom': '和平国罗贝塔501'},
        {'name': '模糊魔法', 'group': '(疼逊会议)', 'teacher': '席拉',
            'zc': '11-18(周)', 'classroom': '王立瑟雷斯特利亚226'},
        {'name': '高阶魔法方程', 'group': '(疼逊会议)', 'teacher': ' 沙耶',
            'zc': '2-17(周)', 'classroom': '深邃森林比拉B座502'},
        {'name': '模糊魔法', 'group': '(疼逊会议)', 'teacher': '席拉',
            'zc': '11-18(周)', 'classroom': '王立瑟雷斯特利亚226'},
        {},
        {},
        {}
    ], [
        {'name': '高阶魔法方程', 'group': '(疼逊会议)', 'teacher': ' 沙耶',
         'zc': '2-17(周)', 'classroom': '深邃森林比拉B座502'},
        {'name': '法阵分析', 'group': '(疼逊会议)', 'teacher': '维多利加',
            'zc': '3-18(周)', 'classroom': '和平国罗贝塔301'},
        {'name': '通用魔法理论基础(2)', 'group': '(疼逊会议)', 'teacher': '伊蕾娜',
            'zc': '1-16(周)', 'classroom': '和平国罗贝塔501'},
        {},
        {'name': '黑魔法学选讲', 'group': '(疼逊会议)', 'teacher': '扫帚',
            'zc': '1-8(周)', 'classroom': '王立瑟雷斯特利亚216'},
        {},
        {}
    ], [
        {},
        {'name': '形势与政策(20212)', 'teacher': '艾丝黛儿(思政)',
         'zc': '12,14(周)', 'classroom': '深邃森林比拉B座101'},
        {'name': '黑魔法学选讲', 'group': '(疼逊会议)', 'teacher': '扫帚',
         'zc': '1-8(周)', 'classroom': '王立瑟雷斯特利亚216'},
        {},
        {'name': '法阵分析', 'group': '(疼逊会议)', 'teacher': '维多利加',
         'zc': '3-18(周)', 'classroom': '和平国罗贝塔301'},
        {},
        {}
    ], [
        {}, {}, {}, {}, {}, {}, {}
    ], [
        {'name': '改变世界的魔药学', 'group': '(疼逊会议)', 'teacher': '芙兰',
         'zc': '5-12(周)', 'classroom': '自由之城克诺兹B座601'},
        {},
        {'name': '改变世界的魔药学', 'group': '(疼逊会议)', 'teacher': '芙兰',
                 'zc': '5-12(周)', 'classroom': '自由之城克诺兹B座601'},
        {},
        {},
        {},
        {}
    ]
]


if __name__ == "__main__":
    cs = courses_from_table(semester=Semester("2021-03-01", TimeTable(DEFAULT_TIME_TABLE)), courses_table=data)

    cal = Calendar()
    for c in cs:
        e = event_from_course(c)
        print("-------\n", c.name, c.class_begin, "\n", e.to_ical().decode())
        cal.add_event(e)

    with open("output.ics", "wb") as f:
        f.write(cal.to_ical())

