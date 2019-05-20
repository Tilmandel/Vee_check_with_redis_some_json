import requests,os,time,redis
from fbchat import Client
from fbchat.models import *
var_url_data = redis.Redis('3.8.101.205', charset="utf-8", decode_responses=True, db=0)

obj_dict = {'BTC': 8400,'VEE':0.00654}
var_url_data.hmset("19.05.2019", obj_dict)


current_day = var_url_data.hgetall("19.05.2019")
print(int(current_day['BTC']))