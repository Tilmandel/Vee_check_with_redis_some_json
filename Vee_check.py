import requests
import os
import time
from fbchat import Client
from fbchat.models import *
client = Client('jaroszek15@poczta.fm', 'spajder21!')
thread_id = '1455530191166678'
thread_type = ThreadType.GROUP
alarm_vee = 0.006
alarm_btc = 8300
counter = 0
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
def first_loop():

       time_now = time.strftime("%H:%M:%S")
       print(time_now)
       try:
           print("""
           VEE: {} USD   $
           BTC : {} USD  {}$""".format(result_list['VEE'],
                                       result_list['BTC'],
                                       float("{:.6f}".format(result_list['BTC'] - result_list['BTC1']))))
           print("""
           VEE Wallet : {}$""".format(int(float(result_list['VEE']) * 29965)))

           result_list['VEE'] = _vee_checker()
           result_list['BTC'] = _btc()
           time.sleep(3)
           os.system('cls')
       except KeyboardInterrupt:
           exit()
def _info_to_msg():
           client.send(Message(text='{} USD'.format(result_list['VEE'])), thread_id=thread_id, thread_type=thread_type)
           client.send(Message(text='{} USD'.format(result_list['BTC'])), thread_id=thread_id, thread_type=thread_type)
           client.logout()
result_list = {}
result_list['VEE'] = _vee_checker()
result_list['BTC'] = _btc()
result_list['BTC1'] = _btc()
result_list['VEE1'] = _vee_checker()
while True:
    time_now = time.strftime("%H:%M:%S")
    try:
        if float(result_list['VEE']) >= alarm_vee or result_list['BTC'] >= alarm_btc and counter == 0:
            _info_to_msg()
            alarm_vee += 0.006
            alarm_btc += 600
        else:
            first_loop()
    except KeyboardInterrupt:
        client.logout()
        exit()























