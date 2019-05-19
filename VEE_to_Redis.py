import requests,os,time,redis
from fbchat import Client
from fbchat.models import *
client = Client('jaroszek15@poczta.fm', 'spajder21!')
thread_id = '1455530191166678'
thread_type = ThreadType.GROUP
var_alarm_vee = 0.006
var_alarm_btc = 8300
var_counter = 0
var_date_of_day = []
var_current_price_vee = []
var_current_price_btc = []
var_arch_VEE_price = []
var_arch_BTC_price = []
var_DB_data = {}
var_url_data = redis.Redis('3.8.101.205', charset="utf-8", decode_responses=True, db=0)
def _write_to_server(var_url_data,date,obj):
    avg_price =sum(obj)/len(obj)
    var_url_data.hmset(date,avg_price)
def _take_data_from_server(var_url_data):
    start_time_day = int(time.strftime('%d'))
    for i in range(start_time_day-7,start_time_day+1):
        k = str(i)
        key = k + time.strftime('.%m.%Y')
        try:
            arch_data = var_url_data.hgetall(key)
            var_DB_data[key] = arch_data
        except KeyError:
            var_DB_data[key] = {'BTC': 0, 'VEE': 0}
            continue
def _data_to_lists():
    for i in var_DB_data:
        var_date_of_day.append("{:^10s}".format(i))
        var_arch_BTC_price.append(var_DB_data[i]['BTC'])
        var_arch_VEE_price.append(var_DB_data[i]['VEE'])
    for i in var_arch_VEE_price:
        _i_aligated = "{:^10s}".format(i)
        var_arch_VEE_price.insert(var_arch_VEE_price.index(i), _i_aligated)
        var_arch_VEE_price.remove(i)
    for i in var_arch_BTC_price:
        _i_aligated = "{:^10d}".format(i)
        var_arch_BTC_price.insert(var_arch_BTC_price.index(i), _i_aligated)
        var_arch_BTC_price.remove(i)
def _replace(string):
    delete = str(string)
    delete = delete._replace(",", " ")
    delete = delete._replace("'", "")
    delete = delete._replace('[', "")
    delete = delete._replace(']', "")
    return delete
def _vee_checker():
    url = 'https://coinmarketcap.com/currencies/blockv/?fbclid=IwAR3itiEQqX-6bZeyEkB4Y4pocgVlxbtaRWiFtlrp8WfKWuuZ9SzcunXxg7s#charts'
    respond = requests.get(url)
    a = respond.text
    tekst_1 = 'data-currency-value'
    index = a.index(tekst_1)
    vee_price = [a[index+20:index+28]]
    return vee_price[0]
def _btc():
    url_cryptowatch = 'https://api.cryptowat.ch/markets/coinbase-pro/btcusd/price'
    respond_btc = requests.get(url_cryptowatch)
    data_json = respond_btc.json()
    return data_json['result']['price']
def _first_loop():
    time_now = time.strftime("%H:%M:%S")
    print(time_now)
    try:
        print("""
        VEE: {} USD   $
        BTC : {} USD  {}$""".format(var_result_list['VEE'],
                                    var_result_list['BTC'],
                                    float("{:.6f}".format(var_result_list['BTC'] - var_result_list['BTC1']))))
        print("""
        VEE Wallet : {}$""".format(int(float(var_result_list['VEE']) * 29965)))
        print(_replace(var_date_of_day))
        print(_replace(var_arch_BTC_price))
        print(_replace(var_arch_VEE_price))
        var_result_list['VEE'] = _vee_checker()
        var_result_list['BTC'] = _btc()
        time.sleep(3)
        os.system('cls')
    finally:
        _write_to_server(var_url_data,day_date,var_current_price_vee)
        _write_to_server(var_url_data, day_date, var_current_price_btc)
        client.logout()
        exit()
def _info_to_msg():
    client.send(Message(text='{} USD'.format(var_result_list['VEE'])), thread_id=thread_id, thread_type=thread_type)
    client.send(Message(text='{} USD'.format(var_result_list['BTC'])), thread_id=thread_id, thread_type=thread_type)
    client.logout()
var_result_list = {}
_take_data_from_server(var_url_data)
var_result_list['VEE'] = _vee_checker()
var_result_list['BTC'] = _btc()
var_result_list['BTC1'] = _btc()
var_result_list['VEE1'] = _vee_checker()
while True:
    day_date = time.strftime("%d.%m.%Y")
    time_now = time.strftime("%H:%M:%S")
    time_H_M = time.strftime("%H:%M")
    try:
        if float(var_result_list['VEE']) >= var_alarm_vee or var_result_list['BTC'] >= var_alarm_btc and var_counter == 0:
            _info_to_msg()
            var_alarm_vee += 0.006
            var_alarm_btc += 600
        if time_H_M == '12:00' or time_H_M == '18:00' or time_H_M == '23:40':
            var_current_price_vee.append(var_result_list['VEE'])
            var_current_price_btc.append(var_result_list['BTC'])
        if time_H_M == '23:55':
            _write_to_server(var_url_data, day_date, var_current_price_vee)
            _write_to_server(var_url_data, day_date, var_current_price_btc)
        else:
            _first_loop()
    finally:
        _write_to_server(var_url_data,day_date,var_current_price_vee)
        _write_to_server(var_url_data, day_date, var_current_price_btc)
        client.logout()
        exit()


