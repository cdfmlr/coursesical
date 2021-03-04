from typing import List

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from bs4 import BeautifulSoup
import re


class CourseTableCrawler:
    """登教务，爬课表
    """
    BASE_URL = "https://jwxt.ncepu.edu.cn/jsxsd/xskb/xskb_list.do"
    COURSE_TABLE_URL = 'https://jwxt.ncepu.edu.cn/jsxsd/xskb/xskb_list.do'

    def __init__(self, sid, password) -> None:
        """
        sid: 学号
        password: 密码
        """
        self.sid = sid
        self.password = password

        self._driver = webdriver.Chrome()

    def _login(self) -> None:
        self._driver.get(self.BASE_URL)
        try:
            input_account = WebDriverWait(self._driver, timeout=5).until(
                lambda d: d.find_element_by_xpath('//*[@id="userAccount"]'))
            input_account.send_keys(self.sid)

            input_password = WebDriverWait(self._driver, timeout=5).until(
                lambda d: d.find_element_by_xpath('//*[@id="userPassword"]'))
            input_password.send_keys(self.password)

            btn_login = WebDriverWait(self._driver, timeout=5).until(
                lambda d: d.find_element_by_xpath('//*[@id="ul1"]/li[5]/button'))
            btn_login.click()

            # 等待完成
            WebDriverWait(self._driver, timeout=5).until(
                lambda d: d.find_element_by_xpath('//*[@id="btn_userLogout"]'))
        except Exception as e:
            raise TimeoutError(e)

    def _switch_to_course_table(self) -> None:
        """after _login
        """
        self._driver.get('https://jwxt.ncepu.edu.cn/jsxsd/xskb/xskb_list.do')

        try:
            # alert("离开此网站？", "系统可能不会保存您所做的更改。")
            self._driver.implicitly_wait(0.02)
            alert = self._driver.switch_to.alert
            alert.accept()
        except Exception as e:  # 也可能没有这个对话框。后来的update: 好吧，大概率是没有的，我把wait调低了，看它白白卡着难受
            pass

    def _fetch_course_table_page(self) -> str:
        """after _switch_to_course_table

        return: html of https://jwxt.ncepu.edu.cn/jsxsd/xskb/xskb_list.do'
        """
        try:
            table = WebDriverWait(self._driver, timeout=5).until(
                lambda d: d.find_element_by_xpath('//*[@id="kbtable"]'))
            # print(table.text)
            return self._driver.page_source
        except Exception as e:
            raise TimeoutError(e)

    def _parse_course(self, html) -> dict:
        """解析课表的一个单元格，即一节课
        html: 一个课程的 td

        return: {"name": "魔法解析入门", "teacher": "...", ...}
        """
        course = {}
        for div in html.find_all(name="div"):
            if '老师' not in str(div):  # 有老师的才是完整版的
                continue

            name = re.findall(
                'class="kbcontent".*?>.*?<br.?>(.*?)<br.?><font', str(div))
            if name:
                course["name"] = name[0]
                course["text"] = div.text

            # 解析其他字段：
            for field in div:
                if not hasattr(field, "get"):
                    continue
                title = field.get("title", None)
                if title == "分组名称":
                    course["group"] = field.text
                elif title == "老师":
                    course["teacher"] = field.text
                elif title == "周次(节次)":
                    course["zc"] = field.text
                elif title == "教室":
                    course["classroom"] = field.text

        return course

    def _parse_course_table(self, html) -> list:
        """解析课表
        html: 整个 https://jwxt.ncepu.edu.cn/jsxsd/xskb/xskb_list.do 的页面

        return: [[{course}, ...星期x], ...第x大节]
        """
        soup = BeautifulSoup(html, features="lxml")
        table = soup.find(attrs={'id': 'kbtable'})
        courses = []
        for tr in table.tbody.find_all(name='tr'):  # 星期, 第一大节, 第二大节, ...
            if not courses:  # 第一行：星期一 星期二 星期三 ... 没用
                courses.append([])
                continue

            # 后面每个 tr 就是 第一大节，第二大节，... 的行：里面 7 个 td 就是周1-7的第x大节课

            if '备注' in tr.text:  # 最后有个备注
                continue

            courses.append([])
            for td in tr.find_all(name='td'):
                courses[-1].append(self._parse_course(td))

        courses = courses[1:]

        # print(courses)
        return courses

    def run(self) -> List[List[dict]]:
        """运行爬虫：登陆教务，获取课表，解析数据
        return: 获取的课表 [[{course}, ...星期x], ...第x大节]
        """
        self._login()
        self._switch_to_course_table()
        html = self._fetch_course_table_page()
        courses = self._parse_course_table(html)

        return courses
