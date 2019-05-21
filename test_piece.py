import requests,os,time,redis
from fbchat import Client
from fbchat.models import *
var_url_data = redis.Redis('3.8.101.205', charset="utf-8", decode_responses=True, db=0)




current_day = var_url_data.hgetall("21.05.2019")
print(current_day)