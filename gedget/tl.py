# -*- coding: utf-8 -*-
import web
import os
import urllib2,json

class simi:
    def __init__(self):
        self.base_api = 'http://www.tuling123.com/openapi/api?'
        self.key = 'ce17b73751111f069a7b940ace25860b'
        print 'init simi...' 

    def xiaohuangji(self, ask):
        ask = ask.encode('UTF-8')
        enask = urllib2.quote(ask)
        url = self.base_api+'key='+self.key+'&info='+enask
        print url
        resp = urllib2.urlopen(url)
        reson = json.loads(resp.read())
        print 'me: ' + ask
        print 'simi: ' + reson['text']#.encode('utf8')
        #return reson['response'].encode('utf8')
        print reson['code']

simi = simi()        
if __name__ == '__main__':
    ret = simi.xiaohuangji(u'讲个笑话')
