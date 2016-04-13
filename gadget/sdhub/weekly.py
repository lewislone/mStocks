# -*- coding: utf-8 -*-
import tushare as ts
import time as time
import utils

industry_classified = {
 "table"    : 'industry_classified',
 "types"    : {"code":'int', "name":'string', "c_name":'string'},
 "data"     : []
}

item = {}
timestamp = utils.get_ts()
data = ts.get_industry_classified(raw=0)
for i in data.index:
    item['ts'] = timestamp
    item['opt'] = 0
    item['value'] = (data.loc[i, 'code'], data.loc[i, 'name'], data.loc[i, 'c_name'])
    item['uid'] = utils.get_uid(item['value']) 
     
    industry_classified['data'].append(item)

#utils.pp(industry_classified)
utils.dump_json(industry_classified, "industry_classified.json")
tmp = utils.load_json("industry_classified.json");
utils.pp(tmp)

#data.apply(px(data['code'],data['name'],data['c_name']))
