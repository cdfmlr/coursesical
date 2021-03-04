# from coursesical.jw import *
from jw import *

def test0():
    crawler = CourseTableCrawler("***", "***")
    courses = crawler.run()
    print(courses)

if __name__ == "__main__":
    test0()