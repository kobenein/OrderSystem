from tornado import web, ioloop
from time import strftime, strptime
import time, os, json
from operator import itemgetter
from collections import Counter


def Today0am():
    return strptime(strftime('%Y/%m/%d %a ') + '00:00:00','%Y/%m/%d %a %H:%M:%S')

def Today4pm():
    return strptime(strftime('%Y/%m/%d %a ') + '16:00:00','%Y/%m/%d %a %H:%M:%S')

with open('log.txt','a') as file:
    pass



Member_List = {'192.168.17.12': 'MichelleYu',
 '192.168.17.13': 'DannyRen',
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
 '192.168.17.45': 'PoloChuan',
 '192.168.17.46': 'LynnChiang',
 '192.168.17.50': 'PikaChien',
 '192.168.17.51': 'PingchengHuang',
 '192.168.17._1': 'LouisDai',
 '192.168.17.52': 'ReikenTsai',
 '192.168.17.53': 'ChrisWang',
 '192.168.17.54': 'TidoriHung',
 '192.168.17._7': 'EvanChang'}


def GetAllResult():
    result_all = dict()
    with open('log.txt') as f:
        for line in f:
            tmp = line.strip().split('; ')
            if tmp[2] in list(Member_List.keys()):
                key = Member_List[tmp[2]]
                val = tmp[1]
                result_all[key] = val
                
    result_all = sorted(result_all.items(), key=itemgetter(0))            
    return result_all

def GetSummary(result_all):
    result_all = {i[0]:i[1] for i in result_all}
    
    Summary = list(result_all.values())
    Summary = Counter(Summary)
    Summary = sorted(Summary.items(), key=itemgetter(0))

    return Summary



weekdays = {'星期一':'Mon','星期二':'Tue','星期三':'Wen','星期四':'Thu','星期五':'Fri'}

def GetDinner():
    Dinner_List = [[] for i in range(5)]

    with open('Dinner_List.txt','r',encoding='utf-8-sig',errors='ignore') as Dinner:
        for line in Dinner:
            FiveItem = line.split('\t')
            for idx,Item in enumerate(FiveItem):
                Item = Item.replace(' ','').replace('：',':').strip()
                Dinner_List[idx].append(Item)

    tmp = dict()
    for i in Dinner_List:
        key = weekdays[i[0]]
        val = i[1:]
        tmp[key] = val

    return tmp





#==========================================================================
#==========================================================================
class IndexHandler(web.RequestHandler):
    
    def get(self):
        dinner_list = GetDinner()[strftime('%a')]

        AllResult = GetAllResult()
        Summary = GetSummary(AllResult)

        OrderIp = self.request.remote_ip
        if OrderIp in Member_List.keys():
            OrderUser = Member_List[OrderIp]
        else:
            OrderUser = ''

        self.render("index.html",
                    weekday=strftime('%A'),dinner=dinner_list,Post=False,AllResult=AllResult,Summary=Summary,OrderUser=OrderUser)
            
    def post(self):
        dinner_list = GetDinner()[strftime('%a')]
      
        OrderTime = strftime('%Y/%m/%d %a %H:%M:%S')
        OrderChoise = int(self.get_argument('choise')) - 1 #from 0 -1:for cancel

        OrderIp = self.request.remote_ip
        
        OrderUser = self.get_argument('Name')
        OrderUser = OrderUser if OrderUser else 'anonymous'

        OrderMeal = dinner_list[OrderChoise] if OrderChoise>=0 else '取消今日點餐'

        Order = '{}; {}; {}; {}\n'.format(OrderTime,OrderMeal,OrderIp,OrderUser)

        with open('log.txt','a') as file:
            file.write(Order)

        AllResult = GetAllResult()
        Summary = GetSummary(AllResult)
        self.render("index.html",
                    weekday=strftime('%A'),dinner=dinner_list,Post=True,Choise=OrderMeal,AllResult=AllResult,Summary=Summary,OrderUser=OrderUser)
        

class LogHandler(web.RequestHandler):
    def get(self):
        Log = list()
        with open('log.txt') as f:
            for line in f:
                Log.append(line.strip().split('; '))
                self.write(line+'<br>')

##        print(Log[-1])
##            print(strptime(r[0],'%Y/%m/%d %a %H:%M:%S')>Today0am())



class ResultHandler(web.RequestHandler):
    def get(self):
        self.write('under construction')
                

#==========================================================================
#==========================================================================
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "autoreload": True
}

class Apps(web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/log/", LogHandler),
            (r"/result/", ResultHandler)
        ]
        web.Application.__init__(self, handlers, **settings)

def main():
    app = Apps()
    app.listen(8888)
    ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()







