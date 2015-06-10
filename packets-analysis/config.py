#coding: UTF-8
import ConfigParser

configFile='config.ini'

def get_butlers_from_ini():
    parser = ConfigParser.ConfigParser()
    try:
        parser.readfp(open(configFile))
        modules = parser.get("Cases","modules")
        return modules.split(",")
    except:
        print "Read config.ini error"
