import tushare as ts
import time as time

industry_classified = {
 "table"    : 'industry_classified',
 "types"    : {"code":'int', "name":'string', "c_name":'string'},
 "data"     : []
}

def px(code, name, c_name):
    print code,name,c_name

data = ts.get_industry_classified(raw=0)
for i in data.index:
    print data.loc[i, 'code'],data.loc[i, 'name'],data.loc[i, 'c_name']
    

#data.apply(px(data['code'],data['name'],data['c_name']))
