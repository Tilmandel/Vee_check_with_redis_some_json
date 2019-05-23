import requests,os,time,redis
from fbchat import Client
from fbchat.models import *
var_url_data = redis.Redis('3.8.101.205', charset="utf-8", decode_responses=True, db=0)




current_day = var_url_data.hgetall("23.05.2019")
print(var_url_data.keys('*'))
print(current_day)
print(type(current_day['VEE']))
