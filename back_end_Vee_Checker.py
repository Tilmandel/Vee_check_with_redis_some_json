def _info_to_msg(var_result_list):
    from fbchat import Client
    from fbchat.models import *
    thread_id = '1455530191166678'
    thread_type = ThreadType.GROUP
    client = Client('login', 'password')
    client.send(Message(text='{} USD'.format(var_result_list['VEE'])), thread_id=thread_id, thread_type=thread_type)
    client.send(Message(text='{} USD'.format(var_result_list['BTC'])), thread_id=thread_id, thread_type=thread_type)
    client.logout()
def _data_to_lists(var_DB_data_sorted,var_DB_data):
    var_date_of_day = []
    var_arch_VEE_price = []
    var_arch_BTC_price = []
    for i in var_DB_data_sorted:
        var_date_of_day.append("{:>5s}".format(i))
        var_arch_BTC_price.append("{:>10f}".format(var_DB_data[i]['BTC']))
        var_arch_VEE_price.append("{:>10f}".format(var_DB_data[i]['VEE']))
    return var_date_of_day,var_arch_VEE_price,var_arch_BTC_price

def _write_to_server(server,date,obj,len_vee,len_btc,var_result_list):
    try:
        price_btc = obj['BTC']/len(len_btc)
        price_vee = obj['VEE']/len(len_vee)
        obj_dict = {'BTC':price_btc,'VEE':price_vee}
        var_url_data.hmset(date, obj_dict)
    except ZeroDivisionError:
        obj_dict = {'BTC':var_result_list['BTC'], 'VEE':var_result_list['VEE'] }
        server.hmset(date,obj_dict)
        
def _take_data_from_server(var_url_data):
    var_DB_data = {}
    start_time_day = int(time.strftime('%d'))
    for i in range(start_time_day-3,start_time_day):
        key = str(i)+ time.strftime('.%m.%Y')
        try:
            arch_data = var_url_data.hgetall(key)
            if arch_data == {}:
                var_DB_data[key] = {'BTC': 0, 'VEE': 0}
            else:
                var_DB_data[k] = {'BTC':arch_data['BTC'],'VEE':arch_data['VEE']}
        except Exception:
            continue
    return var_DB_data ,sorted(var_DB_data)
def _vee_checker():
    url = 'https://coinmarketcap.com/currencies/blockv/?fbclid=IwAR3itiEQqX-6bZeyEkB4Y4pocgVlxbtaRWiFtlrp8WfKWuuZ9SzcunXxg7s#charts'
    respond = requests.get(url)
    a = respond.text
    tekst_1 = 'data-currency-value'
    index = a.index(tekst_1)
    vee_price = [a[index+20:index+28]]
    return round(float(vee_price[0]),ndigits=5)
def _btc():
    url_cryptowatch = 'https://api.cryptowat.ch/markets/coinbase-pro/btcusd/price'
    respond_btc = requests.get(url_cryptowatch)
    data_json = respond_btc.json()
    return round(float(data_json['result']['price']),ndigits=2)
