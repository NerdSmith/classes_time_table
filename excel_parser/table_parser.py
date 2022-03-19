import json

import xlrd
from datetime import time
from itertools import cycle

from excel_parser.re_utils import contains_cabinet

weekdays = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
# class_time = {
#     "800  -  935": (time(hour=8), time(hour=9, minute=35)),
#     "945 - 1120": (time(hour=9, minute=45), time(hour=11, minute=20)),
#     "1130-1305": (time(hour=11, minute=30), time(hour=13, minute=5)),
#     "1325-1500": (time(hour=13, minute=25), time(hour=15)),
#     "1510-1645": (time(hour=15, minute=10), time(hour=16, minute=45)),
#     "1655-1830": (time(hour=16, minute=55), time(hour=18, minute=30)),
#     "1840-2000": (time(hour=18, minute=40), time(hour=20)),
#     "2010-2130": (time(hour=20, minute=10), time(hour=21, minute=30)),
# }


class_time = {
    "800  -  935": "8:00-9:35",
    "945 - 1120": "9:45-11:20",
    "1130-1305": "11:30-13:05",
    "1325-1500": "13:25-15:00",
    "1510-1645": "15:10-16:45",
    "1655-1830": "16:55-18:30",
    "1840-2000": "18:40-20:00",
    "2010-2130": "20:10-21:30",
}


def unmergedValue(row_i, col_i, sh):
    for bound in sh.merged_cells:
        rlo, rhi, clo, chi = bound
        if row_i in range(rlo, rhi):
            if col_i in range(clo, chi):
                return sh.cell_value(rlo, clo)
    return sh.cell_value(row_i, col_i)


def is_time(e: str):
    return e in class_time


def is_wday(e: str):
    return e in weekdays


def parse_t(filename, idx):
    book = xlrd.open_workbook(filename, formatting_info=True)
    sh = book.sheet_by_index(idx)
    rows = list(sh.get_rows())

    classes_by_time = dict()

    wdays = iter(cycle(weekdays))
    curr_wday = None
    cls_time = None
    prev_cls_time = None
    r_counter = 0
    for row_i in range(len(rows)):

        r_wday = rows[row_i][1]
        if r_wday.ctype == 1 and r_wday.value in weekdays:
            curr_wday = next(wdays)

        r_cls_time = rows[row_i][2]

        if r_cls_time.value in class_time.keys():

            cls_time = r_cls_time.value
            prev_cls_time = cls_time
        else:
            cls_time = prev_cls_time

        if r_cls_time.value in class_time.keys() or r_counter == 1:
            line_classes = []
            for col_i in range(3, len(rows[row_i])):
                e = rows[row_i][col_i]
                unmerged_e = unmergedValue(row_i, col_i, sh)
                if e.ctype == 1 and not is_time(e.value) and not is_wday(e.value):
                    if contains_cabinet(e.value):
                        line_classes.append(e.value)
                elif unmerged_e != '' and not is_time(unmerged_e) and not is_wday(unmerged_e):
                    if contains_cabinet(unmerged_e):
                        line_classes.append(unmerged_e)

            if r_counter == 0:
                num_den = "n"
                r_counter += 1
            else:
                num_den = "d"
                r_counter = 0

            formatted_cls_time = class_time[cls_time]
            cls_times = classes_by_time.get(curr_wday)
            if cls_times is None: # если нет дня недели
                classes_by_time[curr_wday] = {}
                classes_by_time[curr_wday][num_den] = {}
                classes_by_time[curr_wday][num_den][formatted_cls_time] = []
                classes_by_time[curr_wday][num_den][formatted_cls_time] += line_classes
            else: # если есть день недели
                r_num_den = classes_by_time[curr_wday].get(num_den)
                if r_num_den is None:
                    classes_by_time[curr_wday][num_den] = {}
                    classes_by_time[curr_wday][num_den][formatted_cls_time] = []
                    classes_by_time[curr_wday][num_den][formatted_cls_time] += line_classes
                else:
                    classes_by_time[curr_wday][num_den][formatted_cls_time] = []
                    classes_by_time[curr_wday][num_den][formatted_cls_time] += line_classes
        else:
            r_counter = 0


    for wday in classes_by_time.keys():
        for num_den in classes_by_time[wday].keys():
            for cls_t in classes_by_time[wday][num_den].keys():
                classes_by_time[wday][num_den][cls_t] = list(set(classes_by_time[wday][num_den][cls_t]))

    return json.dumps(classes_by_time, ensure_ascii=False)

    # print(json.dumps(classes_by_time, ensure_ascii=False))






if __name__ == '__main__':
    parse_t("ФКН_Расписание_второе полугодие_2021-2022 (на сайт).xls", 1)
