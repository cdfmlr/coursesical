from coursesical.main import *

import argparse
import json


def cmd():
    description = "coursesical: courses to ical."
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-s", "--sid", action="store", required=True,
                        help="学号(教务账号)")
    parser.add_argument("-p", "--password", action="store", required=True,
                        help="教务密码")
    parser.add_argument("-f", "--semester-first-monday", action="store",
                        required=True, help="学期的第一周周一日期: YYYY-MM-DD")
    parser.add_argument("-t", "--courses-time", action="store",
                        help=f"作息时间表 (in JSON). \n Default: {json.dumps(DEFAULT_TIME_TABLE)}",
                        default=json.dumps(DEFAULT_TIME_TABLE))
    parser.add_argument("-o", "--output", action="store",
                        help="输出结果日历文件. \n Default: coursesical.ics",
                        default="coursesical.ics")

    args = parser.parse_args()

    main(sid=args.sid,
         password=args.password,
         semester_first_monday=args.semester_first_monday,
         courses_time=json.loads(args.courses_time),
         output=args.output)


if __name__ == "__main__":
    cmd()
