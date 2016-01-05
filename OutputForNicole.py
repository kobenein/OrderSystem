import xlsxwriter

from TimeCheck import IsTimeAvailable
from Result import *



ITA = IsTimeAvailable()

logfile = ITA[ITA['filechoise']]


AllResult = GetAllResult(logfile + '.txt')
Summary = GetSummary(AllResult)


#====================================================================
FileName = '便當訂購表格_{}.xlsx'.format(logfile)
workbook = xlsxwriter.Workbook(FileName)
worksheet = workbook.add_worksheet()
worksheet.set_column(0, 0, 30)

for idx,i in enumerate(Summary):
    row = idx+1
    col = 0

    worksheet.write(row,col, i[0])
    worksheet.write(row,col+1, i[1])

worksheet.write(row+2,0, '總共')
worksheet.write(row+2,1, len(AllResult))

workbook.close()
