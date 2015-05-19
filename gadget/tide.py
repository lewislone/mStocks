# -*- coding: utf-8 -*-
import os
from datetime import *

lunarInfos = [0x04bd8,0x04ae0,0x0a570,0x054d5,0x0d260,0x0d950,0x16554,0x056a0,0x09ad0,0x055d2,#1900-1909
            0x04ae0,0x0a5b6,0x0a4d0,0x0d250,0x1d255,0x0b540,0x0d6a0,0x0ada2,0x095b0,0x14977,#1910-1919
            0x04970,0x0a4b0,0x0b4b5,0x06a50,0x06d40,0x1ab54,0x02b60,0x09570,0x052f2,0x04970,#1920-1929
            0x06566,0x0d4a0,0x0ea50,0x06e95,0x05ad0,0x02b60,0x186e3,0x092e0,0x1c8d7,0x0c950,#1930-1939
            0x0d4a0,0x1d8a6,0x0b550,0x056a0,0x1a5b4,0x025d0,0x092d0,0x0d2b2,0x0a950,0x0b557,#1940-1949
            0x06ca0,0x0b550,0x15355,0x04da0,0x0a5b0,0x14573,0x052b0,0x0a9a8,0x0e950,0x06aa0,#1950-1959
            0x0aea6,0x0ab50,0x04b60,0x0aae4,0x0a570,0x05260,0x0f263,0x0d950,0x05b57,0x056a0,#1960-1969
            0x096d0,0x04dd5,0x04ad0,0x0a4d0,0x0d4d4,0x0d250,0x0d558,0x0b540,0x0b6a0,0x195a6,#1970-1979
            0x095b0,0x049b0,0x0a974,0x0a4b0,0x0b27a,0x06a50,0x06d40,0x0af46,0x0ab60,0x09570,#1980-1989
            0x04af5,0x04970,0x064b0,0x074a3,0x0ea50,0x06b58,0x055c0,0x0ab60,0x096d5,0x092e0,#1990-1999
            0x0c960,0x0d954,0x0d4a0,0x0da50,0x07552,0x056a0,0x0abb7,0x025d0,0x092d0,0x0cab5,#2000-2009
            0x0a950,0x0b4a0,0x0baa4,0x0ad50,0x055d9,0x04ba0,0x0a5b0,0x15176,0x052b0,0x0a930,#2010-2019
            0x07954,0x06aa0,0x0ad50,0x05b52,0x04b60,0x0a6e6,0x0a4e0,0x0d260,0x0ea65,0x0d530,#2020-2029
            0x05aa0,0x076a3,0x096d0,0x04bd7,0x04ad0,0x0a4d0,0x1d0b6,0x0d250,0x0d520,0x0dd45,#2030-2039
            0x0b5a0,0x056d0,0x055b2,0x049b0,0x0a577,0x0a4b0,0x0aa50,0x1b255,0x06d20,0x0ada0,#2040-2049
            #Add By JJonline@JJonline.Cn
            0x14b63,0x09370,0x049f8,0x04970,0x064b0,0x168a6,0x0ea50, 0x06b20,0x1a6c4,0x0aae0,#2050-2059
            0x0a2e0,0x0d2e3,0x0c960,0x0d557,0x0d4a0,0x0da50,0x05d55,0x056a0,0x0a6d0,0x055d4,#2060-2069
            0x052d0,0x0a9b8,0x0a950,0x0b4a0,0x0b6a6,0x0ad50,0x055a0,0x0aba4,0x0a5b0,0x052b0,#2070-2079
            0x0b273,0x06930,0x07337,0x06aa0,0x0ad50,0x14b55,0x04b60,0x0a570,0x054e4,0x0d160,#2080-2089
            0x0e968,0x0d520,0x0daa0,0x16aa6,0x056d0,0x04ae0,0x0a9d4,0x0a2d0,0x0d150,0x0f252,#2090-2099
            0x0d520]#2100
lunarMonths = [u"正月",u"二月",u"三月",u"四月",u"五月",u"六月",u"七月",u"八月",u"九月",u"十月",u"十一月",u"腊月"]
lunarDays = [u'初一',u'初二',u'初三',u'初四',u'初五',u'初六',u'初七',u'初八',u'初九',u'初十',
            u'十一',u'十二',u'十三',u'十四',u'十五',u'十六',u'十七',u'十八',u'十九',u'二十',
            u'廿一',u'廿二',u'廿三',u'廿四',u'廿五',u'廿六',u'廿七',u'廿八',u'廿九',u'三十',
            ]

BIG_LEAP = 0xF0000
IS_LEAP = 0x0000F
EVERY_M = 0x0FFF0

class lunar:
    def __init__(self):
        print 'init...'

    def get_today_solar_calendar(self):
        now = datetime.now()
        return(now.year, now.month, now.day, now.hour, now.minute, now.second)

    def offset_with_1900(self, when):
        offset = when - date(1900, 1, 31)
        return offset.days

    def get_solar_year_days(self, year):
        if year % 100 == 0:
            if year % 400 == 0:
                return 366
            else:
                return 365
        elif year % 4 == 0:
            return 366 
        else:
            return 365

    def get_solar_days_of_this_year(self, date):
        days = 0
        for month in range(1, date[1]):
            if month == 2 and ((date[0] % 4 == 0 and date[0] % 100 != 0) or (date[0] % 400 == 0)):
                days += 29
                continue
            if (month == 2 and (date[0] % 4 != 0 and date[0] % 100 != 0) or (date[0] % 100 == 0 and date[0] % 400 != 0)):
                days += 28
                continue
            if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 11:
                days += 31
            else:
                days += 30

        days += date[2]
        return days

    #fuck offset_with_1900
    def get_solar_days_between(self, start, end):
        days = 0
        for year in range(start[0], end[0]+1):
            days += self.get_solar_year_days(year)

        return days - self.get_solar_year_days(end[0]) - self.get_solar_days_of_this_year(start) + self.get_solar_days_of_this_year(end)

    def get_lunar_year_days(self, lunarInfo):
        days = 348 #29*12
        tmp = int((lunarInfo & BIG_LEAP)>>16)
        if lunarInfo & IS_LEAP != 0:
            days = days + tmp + 29 
        tmp = (lunarInfo & EVERY_M) >> 4
        for i in range(0, 12):
            days = days + int((tmp >> i) & 0x00001)
        return days

    def get_lunar_day_by_offset(self, offset):
        sum_days = 0
        for lunar in lunarInfos:
            sum_days += self.get_lunar_year_days(lunar)
            if sum_days >= offset:
                break

        days = 0
        tmp = (lunar & EVERY_M) >> 4
        dupMonth = (lunar & IS_LEAP)
        for i in range(0, 12):
            days += 29 + int((tmp >> (11-i)) & 0x00001)
            if i+1 == dupMonth:
                days = days + 29 + int((lunar & BIG_LEAP)>>16) 
                if days >= (offset - (sum_days - self.get_lunar_year_days(lunar))):
                    break
            if days >= (offset - (sum_days - self.get_lunar_year_days(lunar))):
                break
        #print lunarMonths[i]
        day = (29 + ((tmp >> 11-i) & 0x00001)) - (days - (offset - (sum_days - self.get_lunar_year_days(lunar))))

        return (lunarMonths[i], lunarDays[day], day)


lunar = lunar() 
if __name__ == '__main__':
    (y, m, d, h, mi, s) = lunar.get_today_solar_calendar()
    print (y, m , d)
    (M, D, d) = lunar.get_lunar_day_by_offset(lunar.offset_with_1900(date(y, m, d)))
    #(M, D, d) = lunar.get_lunar_day_by_offset(lunar.get_solar_days_between([1900, 1, 31], [y, m, d]))#count solar days by own
    print M + ' ' + D 
    print int(0.8 * (d - 15)) + 12 
    print ((0.8 * d) - int(0.8 * d))*60 + 25 

    d = d + 1
    if d >= 15: 
        h = int(0.8 * (d - 15)) + 12
    else:
        h = int(0.8 * d) + 12

    if d == 1:
        mi = ((0.8 * d) - int(0.8 * d))*60 - 25
    else:
        mi = ((0.8 * d) - int(0.8 * d))*60 + 25
    if mi >= 60:
        h = h + 1
        mi = mi - 60
    print "%d:%d" % (h, mi)
