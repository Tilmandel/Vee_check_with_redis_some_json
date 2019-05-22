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
    var_DB_data = {}
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
    return data_json['result']['price']
