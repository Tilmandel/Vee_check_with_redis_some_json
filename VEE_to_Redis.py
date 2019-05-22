import requests,os,time,redis
from fbchat import Client
from fbchat.models import *
#=======================================================
thread_id = '1455530191166678'
thread_type = ThreadType.GROUP
var_alarm_vee = 0.006
var_alarm_btc = 8300
var_date_of_day = []
var_current_price_vee = []
var_current_price_btc = []
var_arch_VEE_price = []
var_arch_BTC_price = []
var_DB_data = {}
var_url_data = redis.Redis('3.8.101.205', charset="utf-8", decode_responses=True, db=0)
var_result_list = {}
var_clear_data_list = [var_date_of_day,
                       var_current_price_vee,
                       var_current_price_btc,
                       var_arch_VEE_price,
                       var_arch_BTC_price,
                       var_DB_data]
counter = 0
#=======================================================
def _write_to_server(var_url_data,date,obj):
    try:
        price_btc = obj['BTC']/len(var_current_price_vee)
        price_vee = obj['VEE']/len(var_current_price_vee)
        obj_dict = {'BTC':price_btc,'VEE':price_vee}
        var_url_data.hmset(date, obj_dict)
    except ZeroDivisionError:
        obj_dict = {'BTC':int(var_result_list['BTC']) , 'VEE': round(float(var_result_list['VEE']),ndigits=5)}
        var_url_data.hmset(date,obj_dict)
def _take_data_from_server(var_url_data):
    start_time_day = int(time.strftime('%d'))
    for i in range(start_time_day-3,start_time_day):
        key = str(i)+ time.strftime('.%m.%Y')
        try:
            arch_data = var_url_data.hgetall(key)
            if arch_data == {}:
                var_DB_data[key] = {'BTC': 0, 'VEE': 0}
            else:
                var_DB_data[k] = {'BTC':int(arch_data['BTC']),'VEE':float(arch_data['VEE'])}
        except Exception:
            continue
def _data_to_lists():
    for i in var_DB_data_sorted:
        var_date_of_day.append("{:>5s}".format(i))
        var_arch_BTC_price.append("{:>10d}".format(var_DB_data[i]['BTC']))
        var_arch_VEE_price.append("{:>10s}".format(str(var_DB_data[i]['VEE'])))
def _replace(string):
    delete = str(string)
    delete = delete.replace(",", " ")
    delete = delete.replace("'", "")
    delete = delete.replace('[', "")
    delete = delete.replace(']', "")
    return delete
def _vee_checker():
    url = 'https://coinmarketcap.com/currencies/blockv/?fbclid=IwAR3itiEQqX-6bZeyEkB4Y4pocgVlxbtaRWiFtlrp8WfKWuuZ9SzcunXxg7s#charts'
    respond = requests.get(url)
    a = respond.text
    tekst_1 = 'data-currency-value'
    index = a.index(tekst_1)
    vee_price = [a[index+20:index+28]]
    return float(vee_price[0])
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
                                    float(round(var_result_list['BTC'] - var_result_list['BTC1']),ndigits=2)))
        print("""
        VEE Wallet : {}$""".format(int((var_result_list['VEE']) * 29965)))
        print()
        print("Date:    ",_replace(var_date_of_day))
        print("BTC(USD):",_replace(var_arch_BTC_price))
        print("VEE(USD):",_replace(var_arch_VEE_price))
        var_result_list['VEE'] = _vee_checker()
        var_result_list['BTC'] = _btc()
        time.sleep(3)
        os.system('cls')
    except KeyboardInterrupt:
        exit()
def _info_to_msg():
    client = Client('jaroszek15@poczta.fm', 'Spajder2307!')
    client.send(Message(text='{} USD'.format(var_result_list['VEE'])), thread_id=thread_id, thread_type=thread_type)
    client.send(Message(text='{} USD'.format(var_result_list['BTC'])), thread_id=thread_id, thread_type=thread_type)
    client.logout()
def _clearing_current_session_data():
    for obj in var_clear_data_list:
        obj.clear()
#=======================================================
_take_data_from_server(var_url_data)
var_DB_data_sorted = sorted(var_DB_data)
_data_to_lists()
var_result_list['VEE'] = _vee_checker()
var_result_list['VEE1'] = _vee_checker()
var_result_list['BTC'] = _btc()
var_result_list['BTC1'] = int(var_arch_BTC_price[-1])

while True:
    day_date = time.strftime("%d.%m.%Y")
    time_now = time.strftime("%H:%M:%S")
    time_H_M = time.strftime("%H:%M")
    try:
        if float(var_result_list['VEE']) >= var_alarm_vee:
            _info_to_msg()
            var_alarm_vee += 0.006
        if var_result_list['BTC'] >= var_alarm_btc:
            _info_to_msg()
            var_alarm_btc += 600
        if time_H_M == '12:00' or time_H_M == '18:00' or time_H_M == '23:49'and counter == 0:
            var_current_price_vee.append(round(float(var_result_list['VEE']),ndigits=5))
            var_current_price_btc.append(int(var_result_list['BTC']))
            counter = 1
        if time_H_M == '23:51' and counter == 0:
            temp_list = {'BTC':sum(var_current_price_btc), 'VEE': round(float(sum(var_current_price_vee)),ndigits=5)}
            _write_to_server(var_url_data, day_date, temp_list)

            _clearing_current_session_data()

            _take_data_from_server(var_url_data)
            var_DB_data_sorted = sorted(var_DB_data)
            _data_to_lists()
            counter = 1
        if time_H_M == '12:01'or time_H_M == '18:51' or time_H_M == '18:01' or time_H_M == '23:50' and counter == 1:
            counter = 0
        else:
            _first_loop()
    except KeyboardInterrupt:
        exit()


