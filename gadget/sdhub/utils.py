# -*- coding: utf-8 -*-
import time as time
import hashlib 
import pprint
import json

def pp(obj):
    pprint.pprint(obj)

def get_uid(key):
    return hashlib.md5(str(key)).hexdigest()

def get_ts():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def dump_json(list, file_name):
    file = open(file_name, "w")
    json.dump(list, file)
    file.close()

def load_json(file_name):
    file = open(file_name, "r")
    return json.load(open(file_name,"r"))
    #file.close()


def gen_patch(new_data, old_data_file):
    old_data = load_json(old_data_file)
    for new_item in new_data['data']:
        exist = 0
        changed = 0
        for old_item in old_data['data']:
            if new_item['value'][1] == old_data['value'][1]:
                if new_item['uid'] != old_data['uid']:
                    changed = 1
                    break
                else:
                    exist = 1
                    break
        if exist == 1:
            new_data['data'].remove(new_item)
        if changed == 1:
            new_item['opt'] = 1
        if changed == 0 and exist == 0:
            new_item['opt'] = 2

    return new_data
