# coursesical

Courses to iCalendar.

【自用】爬取学校教务系统，获取课表，做成 iCalendar 文件 (.ics)，导入到系统日历 app。

适用于**华北电力大学（保定）**。其他学校改改爬虫模块，上个胶合层也能用（详见下文的 [For Developers](#for-developers)）。

## Dependence

- selenium
- lxml
- beautifulsoup4 
- icalendar
- chrome & chromedriver  (⚠️ manually install)

## Usage

```sh
python3 -m coursesical -s SID -p PASSWORD -f "2021-03-01"
# -f "yyyy-mm-dd" 是你这个学期第一周的周一的日期。
```

用日历 app 打开生成的 coursesical.ics 即可。

## For Developers

这个项目你至少可以复用 `ical.py`，这个文件里提供了比原本的 icalendar 库友好一些的日历接口：

```python
# 新建日历
cal1 = Calendar()

# 新建事件
event1 = Event(summary="课程: 通用魔法理论基础(2)",
                location="王立瑟雷斯特利亚魔法学院教七楼203",
                start=datetime(2031, 3, 4, 8, 0, 0),
                end=datetime(2031, 3, 4, 9, 40, 0),
                description="""
                通用魔法理论基础(2)
                教室: 王立瑟雷斯特利亚魔法学院教七楼B203
                任课老师: 伊蕾娜
                开课时间: 1-16(周) 
                """
                )

# event.alarm(x): 事件开始前 x 分钟提醒
event1.alarm(0)   
event1.alarm(10)

# 每周重复，直到给定日期时间 d
event1.weekly_repeat(until=datetime(2031, 6, 4, 8, 44, 31))

# 事件添加到日历
cal1.add_event(event1)

# 日历写入文件
with open(output, "wb") as f:
    f.write(cal.to_ical())
```

其他实现：

- `course.py`: 实现了课程结构体（类）：通过一个来自教务系统爬虫结果的数据类 RawCourse 和学期信息 Semester 可以构建出 Course，Course 带上了完整的日期时间信息，容易转化为日历时间。
- `jw.py`: 针对我们学校的教务网站的爬虫，用 selenium 自动化获取课表。
- `main.py`: 把 jw、course、ical 三个文件结合起来：爬教务，取课表，析课程，写日历。
- `__main__.py`: 命令行接口。

## References

- [rfc2445: iCalendar](https://tools.ietf.org/html/rfc2445)
- [iCalendar package docs](https://icalendar.readthedocs.io/en/latest/usage.html)
- [aruul: 使用python生成ical-ics-文件](https://aruul.github.io/2020/08/08/使用python生成ical-ics-文件/)
- [aruul: ical文件代码结构说明](https://aruul.github.io/2020/08/07/ical文件代码结构说明/)

## License

MIT License

Copyright (c) 2021 CDFMLR
