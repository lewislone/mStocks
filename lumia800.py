#coding: UTF-8
import os
import re
import sys
import time
import urllib
import urllib2

stock_list = [
                {'name': 'sh',   'code': 'sh000001', 'mPrice': '0', 'mNu': '0'},
                {'name': 'sz',   'code': 'sz399001', 'mPrice': '0', 'mNu': '0'},
                {'name': 'thgf', 'code': 'sz002419', 'mPrice': '7.485', 'mNu': '1000'},
                {'name': 'cqsw', 'code': 'sh601158', 'mPrice': '6.21', 'mNu': '500'},
                #{'name': 'ylny', 'code': 'sh600277', 'mPrice': '11.867', 'mNu': '300'},
                #{'name': 'zgpa', 'code': 'sh601318', 'mPrice': '88.907', 'mNu': '100'},
                #{'name': 'nmhd', 'code': 'sh600863', 'mPrice': '4.093', 'mNu': '0'},
                #{'name': 'sdgf', 'code': 'sh600820', 'mPrice': '14.5', 'mNu': '0'},
                #{'name': 'nsly', 'code': 'sh600219', 'mPrice': '8.817', 'mNu': '0'},
                #{'name': 'ylgf', 'code': 'sh600887', 'mPrice': '24.907', 'mNu': '0'},
                #{'name': 'ypyl', 'code': 'sz300030', 'mPrice': '14.517', 'mNu': '0'},
                #{'name': 'wskj', 'code': 'sz300017', 'mPrice': '48.54', 'mNu': '0'},
             ]
url_stock = 'http://qt.gtimg.cn/q='

def getPageSourceCode(url):
	response = urllib2.urlopen(url)
	html = response.read()
        return html.decode("gbk").encode("utf8")

#v_sz002419="51~Ììºç¹É·Ý~002419~7.61~7.66~7.58~331062~140295~190767~7.61~624~7.60~664~7.59~528~7.58~562~7.57~775~7.62~671~7.63~485~7.64~560~7.65~1085~7.66~2004~~20220216143330~-0.05~-0.65~7.66~7.41~7.61/331062/249256245~331062~24926~2.83~23.25~~7.66~7.41~3.26~88.93~88.95~2.15~8.43~6.89~0.62~-1652~7.53~26.00~35.10~~~0.30~24925.6245~0.0000~0~ ~GP-A~21.18~1.87~2.82~9.02~1.21~9.33~5.66~15.30~19.28~25.99~1168534766~1168847734~-20.76~9.18~1168534766";
def getstockInfo(code):
    items = []
    codes = code.split(',')
    result = getPageSourceCode(url_stock + code)
    #print result
    if len(codes) == 1:
       i = 0
    else:
       i = 1
    for item in result.split(";\n"):
        items.append(item[len('v_')+len(codes[i])+len('="'):].split('~'))
    return items;
    
def getstockInfos(code):
    result = getstockInfo(code)
    return result 

def getstocksInfo():
    print 'Time' + '\t\t' + 'Name' + '\t\t' + 'Price' + '\t\t' + 'Persent' + '\t\t\t' + 'own' + '\t' + 'profit' + '\t' + '%' + '\t' + 'mPrice'
    code = "" 
    for item in stock_list:
        code = code + ',' + item['code']
    info = getstockInfos(code[1:])
    i = 0
    for item in info:
        if len(item) == 1:
           print "***\n"
           continue;
        persent = (float(item[3]) - float(item[4])) / float(item[4]) * 100
        profit = (float(item[3]) - float(stock_list[i]['mPrice'])) * int(stock_list[i]['mNu'])
	if i > 1:
           profit_persent = (float(item[3]) - float(stock_list[i]['mPrice'])) / float(stock_list[i]['mPrice']) * 100
        else:
           profit_persent = 0
        print item[30] + '\t' + item[1]  + '\t' + item[3][0:7] + '\t\t' + str(persent) + '\t\t' + str(stock_list[i]['mNu']) + '\t' + str(profit) + '\t' + str(profit_persent)[0:5] + '\t' + stock_list[i]['mPrice'] 
        i = i + 1

def print_help():
    print '''a kid tool'''
    print '''python lumia800.py stock'''

if __name__ == '__main__':
    if sys.argv[1] == '-h':
        print_help()
        sys.exit(1)

    if sys.argv[1] == 'stock':
       getstocksInfo()
       sys.exit(1)
        
