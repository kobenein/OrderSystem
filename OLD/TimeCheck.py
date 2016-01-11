import time
from time import mktime
from datetime import datetime
from datetime import timedelta



def IsTimeAvailable(DL_Order='14:59:59',DL_View='18:59:59'):
    TodayStart = time.strftime('%Y/%m/%d ') + '00:00:01'
    TodayStart = time.strptime(TodayStart,'%Y/%m/%d %H:%M:%S') # str to time.struct_time

    TodayEnd = time.strftime('%Y/%m/%d ') + '23:59:59'
    TodayEnd = time.strptime(TodayEnd,'%Y/%m/%d %H:%M:%S') # str to time.struct_time    

    TodayTag1 = time.strftime('%Y/%m/%d ') + DL_Order
    TodayTag1 = time.strptime(TodayTag1,'%Y/%m/%d %H:%M:%S') # str to time.struct_time

    TodayTag2 = time.strftime('%Y/%m/%d ') + DL_View
    TodayTag2 = time.strptime(TodayTag2,'%Y/%m/%d %H:%M:%S') # str to time.struct_time

    TodayNow = time.localtime()


    tmp = datetime.fromtimestamp(mktime(TodayNow))
    tmp += timedelta(days=1)
    tomorrow = tmp.strftime('%Y-%m-%d(%a)')
    
  


##    print('now:' + time.strftime('%Y/%m/%d %H:%M:%S'))

    # tm_wday : 禮拜一 0, 禮拜二 1, 禮拜三 2, 禮拜四 3, 禮拜五 4
   
    if TodayNow>TodayStart and TodayNow<TodayTag1:
        weekday_for_Order = TodayNow.tm_wday
        filechoice = 'today'
##        print('可以訂今天的晚餐')
    elif TodayNow>TodayTag2 and TodayNow<TodayEnd:
        weekday_for_Order = TodayNow.tm_wday + 1
        weekday_for_Order = 0 if weekday_for_Order in [5,6] else weekday_for_Order
        filechoice = 'tomorrow'
##        print('可以訂明天的晚餐')
    else:
        weekday_for_Order = None
##        print('非點餐時間')
    
    if TodayNow>TodayStart and TodayNow<TodayTag2:
        weekday_for_View = TodayNow.tm_wday
        filechoice = 'today'
##        print('可以看今天的晚餐')
    elif TodayNow>TodayTag2 and TodayNow<TodayEnd:
        weekday_for_View = TodayNow.tm_wday + 1
        weekday_for_View = 0 if weekday_for_View in [5,6] else weekday_for_View
        filechoice = 'tomorrow'
##        print('可以看明天的晚餐')
    else:
        weekday_for_View = TodayNow.tm_wday
        filechoice = 'today'


    return {'weekday_for_Order':weekday_for_Order , 'weekday_for_View':weekday_for_View ,
            'today':time.strftime('%Y-%m-%d(%a)') , 'tomorrow':tomorrow , 'filechoice':filechoice}




##a = IsTimeAvailable()
##print(a)
