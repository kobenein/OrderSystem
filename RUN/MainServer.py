from tornado import web, ioloop
from time import strftime
import os

from MyShiftTime import MyShiftTime
from Member_List import Member_List
from Dinner_List import getTodayDinnerList
from Result import *
##from _MailTo import *





## 禮拜一 0, 禮拜二 1, 禮拜三 2, 禮拜四 3, 禮拜五 4
##
##
###==========================================================================
###==========================================================================
class IndexHandler(web.RequestHandler):
    def get(self):
        Temp4Get = dict()
        
        MST = MyShiftTime()
        state = MST.IsOrderAvbl()
                
        Temp4Get['POST'] = False
        Temp4Get['Avbl2Order'] = state['Avbl']
        Temp4Get['DinnerList'] = getTodayDinnerList()

        #=============================================================
        _UserTime = strftime('%Y/%m/%d %a %H:%M:%S')

        _UserIp = self.request.remote_ip
        if _UserIp in Member_List.keys():
            _UserName = Member_List[_UserIp]
        else:
            _UserName = 'anonymous'

        log = '{}, {}, {}\n'.format(_UserTime,_UserIp,_UserName)
        print('get: '+log.replace('\n',''))
        #=============================================================

        Temp4Get['User'] = _UserName
        logfile = state['FileName']
        with open(logfile+'.txt','a') as f:
            pass
        with open('alllog.txt','a') as f:
            pass
            
        Temp4Get['AllResult'] = GetAllResult(logfile+'.txt')
        Temp4Get['AllSummary'] = GetSummary(Temp4Get['AllResult'])

        self.render("index.html",Temp4Get=Temp4Get)
            
    def post(self):
        Temp4Get = dict()
        
        MST = MyShiftTime()
        state = MST.IsOrderAvbl()
                
        Temp4Get['POST'] = True
        Temp4Get['Avbl2Order'] = state['Avbl']
        Temp4Get['DinnerList'] = getTodayDinnerList()

        #=============================================================
        _UserTime = strftime('%Y/%m/%d %a %H:%M:%S')

        Choice = self.get_argument('choice')
        tmps = Temp4Get['DinnerList']['餐點']
        dinnersDict = {key:tmp[key] for tmp in tmps for key in tmp}

        _UserMeal = '取消今日點餐' if Choice=='0' else dinnersDict[Choice]

        _UserIp = self.request.remote_ip
        if _UserIp in Member_List.keys():
            _UserName = Member_List[_UserIp]
        else:
            _UserName = self.get_argument('Name')

        log = '{}, {}, {}, {}, {}\n'.format(_UserTime,_UserMeal,_UserIp,_UserName,Choice)
        print('post: '+log.replace('\n',''))
        #=============================================================
        Temp4Get['Meal'] = _UserMeal
            
        Temp4Get['User'] = _UserName
        logfile = state['FileName']
        with open(logfile+'.txt','a') as f:
            f.write(log)
        with open('alllog.txt','a') as f:
            f.write(log)

        Temp4Get['AllResult'] = GetAllResult(logfile+'.txt')
        Temp4Get['AllSummary'] = GetSummary(Temp4Get['AllResult'])

        self.render("index.html",Temp4Get=Temp4Get)

class LogHandler(web.RequestHandler):
    def get(self):
        with open('alllog.txt') as f:
            for line in f:
                self.write(line+'<br>')

class ResultHandler(web.RequestHandler):
    def get(self):
        self.write('under construction')

class MailHandler(web.RequestHandler):
    def get(self):
        to = 'nicole.chen@alcormicro.com'
        subject = '展顥訂便當 {}'.format(strftime('%m/%d'))
        html = '<a href="mailto:{0}?subject={1}" target="_top">Send Mail</a><br>'.format(to,subject)
        
        self.write(html)
        


##        self.write('<iframe width="1" height="1" frameborder="0" src="展顥訂便當_0107.xlsx"></iframe><br>')
##        self.write('<iframe width="1" height="1" frameborder="0" src="/展顥訂便當_0107.xlsx"></iframe><br>')
##        self.write('<iframe width="1" height="1" frameborder="0" src="XLSX/展顥訂便當_0107.xlsx"></iframe><br>')
##        self.write('<iframe width="1" height="1" frameborder="0" src="alllog.txt"></iframe><br>')
##        self.write('<iframe width="1" height="1" frameborder="0" src="/alllog.txt"></iframe><br>')
##        self.write('<iframe width="1" height="1" frameborder="0" src="XLSX/alllog.txt"></iframe><br>')
        
        
                

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
            (r"/mail/", MailHandler),
            (r"/", IndexHandler)
        ]
        web.Application.__init__(self, handlers, **settings)

def main():
    app = Apps()
    app.listen(8888)
    ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()

