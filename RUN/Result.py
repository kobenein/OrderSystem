from Member_List import Member_List
from operator import itemgetter
from collections import Counter


def GetAllResult(logfile):
    result_all = dict()
    with open(logfile) as f:
        for line in f:
            tmp = line.strip().split(', ')
            if tmp[2] in list(Member_List.keys()):
                key = Member_List[tmp[2]]
                val = tmp[1]
                result_all[key] = val
                
    result_all = sorted(result_all.items(), key=itemgetter(0))

    for idx,i in enumerate(result_all):
        if '取消今日點餐' in i:
            result_all.pop(idx)

    return result_all


def GetSummary(result_all):
    result_all = {i[0]:i[1] for i in result_all}
    
    Summary = list(result_all.values())
    Summary = Counter(Summary)
    Summary = sorted(Summary.items(), key=itemgetter(0))

    return Summary




##AllResult = GetAllResult()
##Summary = GetSummary(AllResult)
##
##print(AllResult)
##print(Summary)
##print(type(AllResult))
##print(type(AllResult[0]))
##print(type(Summary))
##print(type(Summary[0]))
