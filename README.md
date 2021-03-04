# coursesical

Courses to iCalendar.

【自用】爬取学校教务系统，获取课表，做成 iCalendar 文件 (.ics)，导入到系统日历 app。

## Dependence

- selenium
- lxml
- beautifulsoup4 
- icalendar
- chrome & chromedriver  (⚠️ manually install)

## Usage

```sh
python3 -m coursesical -s SID -p PASSWORD -f "2021-03-01"
```

用日历 app 打开生成的 coursesical.ics 即可。
