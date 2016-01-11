import datetime as DT


output1 = '''
現在時間(真)：{0.today_real}
現在時間(假)：{0.today}
'''
output2 = '''{0.DL4View}後可訂明日餐點
{0.DL4Order}截止訂餐'''

class MyShiftTime:
    def __init__(self):
        self.DL4View = DT.time(19,00,0)
        self.DL4Order = DT.time(15,5,0)

        self.shift = self.tm2dttm(DT.time.max) - self.tm2dttm(self.DL4View)

        self.__DL4View = self.tm2dttm(self.DL4View) + self.shift
        self.__DL4Order = self.tm2dttm(self.DL4Order) + self.shift
        

        self.today_real = DT.datetime.today()
        self.today = self.today_real + self.shift
        self.weekday = self.today.weekday()
        self.isoweekday = self.today.isoweekday()


    def __str__(self):
        return output2.format(self)

    def tm2dttm(self,TIME):
        if isinstance(TIME , DT.time):
            return DT.datetime.combine(DT.date.today(),TIME)

    def IsOrderAvbl(self):
##        print(DT.time.min)
##        print(self.today.time())
##        print(self.__DL4Order.time())
        
        if MyShiftTime().weekday == 5:
            self.today += DT.timedelta(days=2)
        elif MyShiftTime().weekday == 6:
            self.today += DT.timedelta(days=1)
        
        if DT.time.min<self.today.time() and self.today.time()<=self.__DL4Order.time():

            return {'Avbl':True ,'FileName':self.today.strftime('%Y-%m-%d(%a)') }
        else:
 
            return {'Avbl':False ,'FileName':self.today.strftime('%Y-%m-%d(%a)') }

##print(MyShiftTime())
##print(MyShiftTime().IsOrderAvbl())





