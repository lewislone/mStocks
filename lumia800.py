#coding: UTF-8
import os
import re
import sys
import time
import urllib
import urllib2

url_head_lumia = 'http://bbs.dospy.com/'
#url = 'http://bbs.dospy.com/forumdisplay.php?fid=141&filter=type&typeid=388&orderby=dateline&ascdesc=DESC'
url_lumia = 'http://bbs.dospy.com/forumdisplay.php?fid=141&filter=type&typeid=388&orderby=dateline&page='
url_psp = 'http://bbs.dospy.com//forumdisplay.php?fid=141&filter=type&typeid=391&orderby=dateline&page='
filter_lumia = ' <a href="thread-(.*?).html" target="_blank">(.*?)</a>'


stock_list = [
                {'name': 'sh',   'code': 'sh000001', 'mPrice': '0', 'mNu': '0'},
                {'name': 'sz',   'code': 'sz399001', 'mPrice': '0', 'mNu': '0'},
                {'name': 'nsly', 'code': 'sh600219', 'mPrice': '8.881', 'mNu': '500'},
                {'name': 'ylgf', 'code': 'sh600887', 'mPrice': '24.907', 'mNu': '0'},
                {'name': 'ypyl', 'code': 'sz300030', 'mPrice': '14.517', 'mNu': '0'},
                {'name': 'wskj', 'code': 'sz300017', 'mPrice': '0', 'mNu': '0'},
             ]
url_stock = 'http://hq.sinajs.cn/list='


def getPageSourceCode(url):
        login_data = urllib.urlencode({})
        login_headers = {'Referer':url, 'User-Agent':'Opera/9.60',}
        login_request = urllib2.Request(url, login_data, login_headers)
        html = urllib2.urlopen(login_request).read()
        return html.decode("gbk").encode("utf8")


def getLumiaInfo(url, keyword):
        html = getPageSourceCode(url)
        myItems = re.findall(filter_lumia.decode("gbk").encode("utf8"), html, re.S)
        for item in myItems:
            if item[1].find(keyword) != -1:
                print url_head_lumia + '/thread-' + item[0] + '.html'
                print item[1]

#var hq_str_sh600887="“¡¿˚π…∑›,26.40,26.48,25.94,26.41,25.80,25.94,25.95,24212839,632218400,3700,25.94,48100,25.93,65800,25.92,77968,25.91,121100,25.90,149288,25.95,500,25.97,4200,25.98,63000,25.99,52300,26.00,2014-10-10,14:06:58,00";
def getstockInfo(code):
    items = []
    codes = code.split(',')
    result = getPageSourceCode(url_stock + code)
    if len(codes) == 1:
       i = 0
    else:
       i = 1
    for item in result.split(";\n"):
        items.append(item[len(codes[i])+len('var hq_str_')+1:].split(','))
    return items;
    
    #return result[len(code)+len('var hq_str_')+1:].split(',') 

def getstockInfos(code):
    result = getstockInfo(code)
    return result 

def getstocksInfo():
    print 'Time' + '\t\t\t' + 'Name' + '\t' + 'Price' + '\t\t' + 'Persent' + '\t\t\t' + 'own' + '\t' + 'profit'
    code = "" 
    for item in stock_list:
        code = code + ',' + item['code']
    info = getstockInfos(code[1:])
    i = 0
    for item in info:
        if len(item) == 1:
           print "***\n"
           continue;
        persent = (float(item[3]) - float(item[2])) / float(item[2]) * 100
        if i == 0 or i == 1:
            print item[30] + ' ' + item[31] + ' ' + item[0][1:] + '\t' + item[3] + '\t\t' + str(persent)
        else:
            profit = (float(item[3]) - float(stock_list[i]['mPrice'])) * int(stock_list[i]['mNu'])
            print item[30] + ' ' + item[31] + ' ' + item[0][1:] + '\t' + item[3] + '\t\t' + str(persent) + '\t\t' + str(stock_list[i]['mNu']) + '\t' + str(profit) 
        i += 1

#    for item in stock_list:
#        info = getstockInfo(item['code'])
#        for item in info:
#            if len(item) == 1:
#               continue;
#            persent = (float(item[3]) - float(item[2])) / float(item[2]) * 100
#            print item[30] + ' ' + item[31] + ' ' + item[0][1:] + '\t' + item[3] + '\t\t' + str(persent) 

def print_help():
    print '''a kid tool'''

if __name__ == '__main__':
    if sys.argv[1] == '-h':
        print_help()
        sys.exit(1)

    if sys.argv[1] == '$':
       #while 1:
            getstocksInfo()
            #time.sleep(10)
            print 'done\n'
            sys.exit(1)
        

    if len(sys.argv[1]) != 0:
       #while 1:
            for i in [1,2,3,4,5,6,7]:
               #getLumiaInfo(url_lumia + str(i), sys.argv[1])
               getLumiaInfo(url_psp + str(i), sys.argv[1])
               print '\n'
            print 'done'
            #time.sleep(600)
            sys.exit(1)

