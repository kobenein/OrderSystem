from operator import itemgetter
from time import strftime
import xlsxwriter
from collections import Counter




Member_List = {'192.168.17.13': 'DannyRen',
 '192.168.17.15': 'GinCheng',
 '192.168.17.19': 'KobeNein',
 '192.168.17.20': 'NeilShen',
 '192.168.17.22': 'CPHsu',
 '192.168.17.25': 'ChichengTing',
 '192.168.17.26': 'JoshuaHuang',
 '192.168.17.28': 'MaxChen',
 '192.168.17.29': 'AngusKu',
 '192.168.17.31': 'AaronLin',
 '192.168.17.33': 'JosephLin',
 '192.168.17.35': 'CaseyWang',
 '192.168.17.44': 'MingshuanLee',
 '192.168.17.46': 'LynnChiang',
 '192.168.17.50': 'PikaChien',
 '192.168.17.51': 'PingchengHuang',
 '192.168.17._1': 'LouisDai',
 '192.168.17._2': 'MichelleYu',
 '192.168.17._3': 'ReikenTsai',
 '192.168.17._4': 'PoloChuan',
 '192.168.17._5': 'ChrisWang',
 '192.168.17._6': 'TidoriHung',
 '192.168.17._7': 'EvanChang'}


##with open('Member_List.txt') as f:
##    for line in f:
##        tmp = line.split()
##        Member_List[tmp[0]] = tmp[1]
##from pprint import pprint
##pprint(Member_List)

        

result_all = dict()
with open('log.txt') as f:
    for line in f:
        tmp = line.strip().split('; ')
        if tmp[2] in list(Member_List.keys()):
            key = Member_List[tmp[2]]
            val = tmp[1]
            result_all[key] = val


result_for_Nicole = list(result_all.values())
result_for_Nicole = Counter(result_for_Nicole)

result_for_Nicole = sorted(result_for_Nicole.items(), key=itemgetter(0))

result_all = sorted(result_all.items(), key=itemgetter(0))            




#====================================================================
FileName = '便當訂購表格_{}.xlsx'.format(strftime('%Y-%m-%d_(%a)'))
workbook = xlsxwriter.Workbook(FileName)
worksheet = workbook.add_worksheet()
worksheet.set_column(0, 0, 30)

for idx,i in enumerate(result_for_Nicole):
    row = idx+1
    col = 0

    worksheet.write(row,col, i[0])
    worksheet.write(row,col+1, i[1])

worksheet.write(row+2,0, '總共')
worksheet.write(row+2,1, len(result_all))

workbook.close()
#====================================================================
FileName = '{}.xlsx'.format(strftime('%Y-%m-%d_(%a)'))
workbook = xlsxwriter.Workbook(FileName)
worksheet = workbook.add_worksheet()
worksheet.set_column(0, 0, 16)
worksheet.set_column(1, 1, 30)

for idx,i in enumerate(result_all):
    row = idx+1
    col = 0

    worksheet.write(row,col, i[0])
    worksheet.write(row,col+1, i[1])

workbook.close()
#====================================================================
