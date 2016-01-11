from tornado import web, ioloop
from time import strftime, strptime
import time, os

from TimeCheck import IsTimeAvailable
from Member_List import Member_List
from Result import *





weekdays = {'星期一':0,'星期二':1,'星期三':2,'星期四':3,'星期五':4}
# tm_wday : 禮拜一 0, 禮拜二 1, 禮拜三 2, 禮拜四 3, 禮拜五 4

def GetGetDinner_List():
    tmp = [[] for i in range(5)]

    with open('Dinner_List.txt','r',encoding='utf-8-sig',errors='ignore') as DinnerFile:
        for line in DinnerFile:
            FiveItem = line.split('\t')
            for idx,Item in enumerate(FiveItem):
                Item = Item.replace(' ','').replace('：',':').strip()
                tmp[idx].append(Item)

    Dinner_List = dict()
    for i in tmp:
        key = weekdays[i[0]]
        val = i[1:]
        Dinner_List[key] = val

    return Dinner_List


#==========================================================================
#==========================================================================
class IndexHandler(web.RequestHandler):
    def get(self):
        ITA = IsTimeAvailable()

        with open(ITA['today']+'.txt','a') as file:
            pass
        with open(ITA['tomorrow']+'.txt','a') as file:
            pass        
        
        if ITA['weekday_for_Order']:
            dinner_list = GetGetDinner_List()[ITA['weekday_for_Order']]
        else:
            dinner_list = 'none'

        logfile = ITA[ITA['filechoice']]
        
        AllResult = GetAllResult(logfile+'.txt')
        Summary = GetSummary(AllResult)

        OrderIp = self.request.remote_ip
        if OrderIp in Member_List.keys():
            OrderUser = Member_List[OrderIp]
        else:
            OrderUser = ''

        self.render("index.html",
                    dinner=dinner_list,Post=False,
                    AllResult=AllResult,Summary=Summary,OrderUser=OrderUser)
            
    def post(self):
        ITA = IsTimeAvailable()

        with open(ITA['today']+'.txt','a') as file:
            pass
        with open(ITA['tomorrow']+'.txt','a') as file:
            pass

        if ITA['weekday_for_Order']:
            dinner_list = GetGetDinner_List()[ITA['weekday_for_Order']]
        else:
            dinner_list = 'none'
        

        OrderTime = strftime('%Y/%m/%d %a %H:%M:%S')
        OrderChoice = int(self.get_argument('choice')) - 1 #from 0 -1:for cancel

        OrderIp = self.request.remote_ip
        
        OrderUser = self.get_argument('Name')
        OrderUser = OrderUser if OrderUser else 'anonymous'

        OrderMeal = dinner_list[OrderChoice] if OrderChoice>=0 else '取消今日點餐'

        Order = '{}; {}; {}; {}\n'.format(OrderTime,OrderMeal,OrderIp,OrderUser)

        logfile = ITA[ITA['filechoice']]
        with open(logfile+'.txt','a') as file:
            file.write(Order)
        with open('log.txt','a') as file:
            file.write(Order)     
        
        AllResult = GetAllResult(logfile+'.txt')
        Summary = GetSummary(AllResult)

        self.render("index.html",
                    dinner=dinner_list,Post=True,Choice=OrderMeal,
                    AllResult=AllResult,Summary=Summary,OrderUser=OrderUser)
        

class LogHandler(web.RequestHandler):
    def get(self):
        Log = list()
        with open('log.txt') as f:
            for line in f:
                Log.append(line.strip().split('; '))
                self.write(line+'<br>')

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
            (r"/log/", LogHandler),
            (r"/result/", ResultHandler),
            (r"/", IndexHandler)
        ]
        web.Application.__init__(self, handlers, **settings)

def main():
    app = Apps()
    app.listen(8888)
    ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()







