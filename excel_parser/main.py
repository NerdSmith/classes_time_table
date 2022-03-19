

import re

import xlrd
book = xlrd.open_workbook("ФКН_Расписание_второе полугодие_2021-2022 (на сайт).xls", formatting_info=True)
sh = book.sheet_by_index(1)
rows = list(sh.get_rows())
# print(*list())
# exit(0)
# print(sh.row(12))
# for rx in range(sh.nrows):
#     s = sh.row(rx)
    # print(s)
cab_pattern = re.compile("[0-9]{3}[а-яА-Я]?")

def unmergedValue(rowx, colx, thesheet):
    for crange in thesheet.merged_cells:
        rlo, rhi, clo, chi = crange
        if rowx in range(rlo, rhi):
            if colx in range(clo, chi):
                return thesheet.cell_value(rlo, clo)
    return thesheet.cell_value(rowx, colx)

val = unmergedValue(10, 5, sh)
sp_val = val.split()
m_res = cab_pattern.match(sp_val[-1])
print(bool(m_res))

print("prints:", sh.merged_cells)
