from fbchat import Client
from fbchat.models import *
import time,requests,redis
var_alarm_vee = 0.008
var_alarm_btc = 9500
var_current_price_vee = []
var_current_price_btc = []
var_result_list = {}
var_clear_data_list = [var_current_price_vee,
                       var_current_price_btc]
counter = 0
def _info_to_msg(VEE,BTC):
    thread_id = '1455530191166678'
    thread_type = ThreadType.GROUP
    client = Client('login', 'password')
    client.send(Message(text='{} USD'.format(VEE)), thread_id=thread_id, thread_type=thread_type)
    client.send(Message(text='{} USD'.format(BTC)), thread_id=thread_id, thread_type=thread_type)
    client.logout()
def _vee_checker():
    url = 'https://coinmarketcap.com/currencies/blockv/?fbclid=IwAR3itiEQqX-6bZeyEkB4Y4pocgVlxbtaRWiFtlrp8WfKWuuZ9SzcunXxg7s#charts'
    respond = requests.get(url)
    a = respond.text
    tekst_1 = 'data-currency-value'
    index = a.index(tekst_1)
    vee_price = [a[index+20:index+28]]
    return round(float(vee_price[0]),ndigits=5)
def _btc():
    try:
        url_cryptowatch = 'https://api.cryptowat.ch/markets/coinbase-pro/btcusd/price'
        respond_btc = requests.get(url_cryptowatch)
        data_json = respond_btc.json()
        return round(float(data_json['result']['price']),ndigits=2)
    except ValueError:
        return 0.00
def _write_to_server(date,obj,len_vee,len_btc,var_result_list):
    server = redis.Redis('localhost', charset="utf-8", decode_responses=True,password='password', db=0)
    try:
        price_btc = obj['BTC']/len_btc
        price_vee = obj['VEE']/len_vee
        obj_dict = {'BTC':round(float(price_btc),ndigits=2),'VEE':round(float(price_vee),ndigits=5)}
        server.hmset(date, obj_dict)
    except ZeroDivisionError:
        obj_dict = {'BTC':var_result_list['BTC'],'VEE':var_result_list['VEE']}
        server.hmset(date,obj_dict)
def _clearing_current_session_data():
    for obj in var_clear_data_list:
        obj.clear()
def _clear_0_digit(obj):
    for i in range(obj.count(0)):
        obj.remove(0)
    return obj


while True:
    var_result_list['VEE']=_vee_checker()
    var_result_list['BTC']=_btc()
    day_date = time.strftime("%d.%m.%Y")
    time_now = time.strftime("%H:%M:%S")
    time_H_M = time.strftime("%H:%M")
    if _vee_checker() >= var_alarm_vee:
        _info_to_msg(var_result_list['VEE'],var_result_list['BTC'])
        var_alarm_vee += 0.006
    if _btc() >= var_alarm_btc:
        _info_to_msg(var_result_list['VEE'],var_result_list['BTC'])
        var_alarm_btc += 600
    if time_H_M in ('01:02','07:01','09:25','10:45','12:01','18:25','20:25','23:49'):
        var_current_price_vee.append(float(var_result_list['VEE']))
        var_current_price_vee.append(float(var_result_list['BTC']))
        counter = 1
    if time_H_M == '23:59' and counter == 0:
        var_current_price_vee = _clear_0_digit(var_current_price_vee)
        var_current_price_btc = _clear_0_digit(var_current_price_btc)
        temp_list = {'BTC':sum(var_current_price_btc),'VEE':sum(var_current_price_vee)}
        _write_to_server(day_date,temp_list,len(var_current_price_vee),len(var_current_price_btc),var_result_list)
        _clearing_current_session_data()
    if time_H_M in ('01:03','00:01', '07:02', '09:26', '10:46', '12:02', '18:26', '20:26', '23:50'):
        counter = 0








