import time,redis,os,requests
#=======================================================
server = redis.Redis('3.8.101.205', charset="utf-8", decode_responses=True,password='password', db=0)
var_current_price_vee = []
var_current_price_btc = []
var_result_list = {}
var_clear_data_list = [var_current_price_vee,
                       var_current_price_btc]
counter = 0
#=======================================================
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
def _take_data_from_server(server):
    var_DB_data = {}
    start_time_day = int(time.strftime('%d'))
    for i in range(start_time_day-3,start_time_day):
        key = str(i)+ time.strftime('.%m.%Y')
        try:
            arch_data = server.hgetall(key)
            if arch_data == {}:
                var_DB_data[key] = {'BTC': 0, 'VEE': 0}
            else:
                var_DB_data[key] = {'BTC':arch_data['BTC'],'VEE':arch_data['VEE']}
        except Exception:
            continue
    return var_DB_data, sorted(var_DB_data)
def _replace(string):
    delete = str(string)
    delete = delete.replace(",", " ")
    delete = delete.replace("'", "")
    delete = delete.replace('[', "")
    delete = delete.replace(']', "")
    return delete
def _first_loop():
    time_now = time.strftime("%H:%M:%S")
    print(time_now)
    try:
        print("""
        VEE: {} USD   {}$
        BTC : {} USD  {}$""".format(var_result_list['VEE'],round(var_result_list['VEE'] - float(var_result_list['VEE1']),ndigits=5),
                                    var_result_list['BTC'],
                                    round(var_result_list['BTC'] - float(var_result_list['BTC1']),ndigits=2)))
        print("""
        VEE Wallet : {}$""".format(int(var_result_list['VEE'] * 29965)))
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
def _data_to_lists(var_DB_data_sorted,var_DB_data):
    var_date_of_day = []
    var_arch_VEE_price = []
    var_arch_BTC_price = []
    for i in var_DB_data_sorted:
        var_date_of_day.append("{:>5s}".format(i))
        var_arch_BTC_price.append("{:>10s}".format(str(var_DB_data[i]['BTC'])))
        var_arch_VEE_price.append("{:>10s}".format(str(var_DB_data[i]['VEE'])))
    return var_date_of_day,var_arch_VEE_price,var_arch_BTC_price
def _clearing_current_session_data():
    for obj in var_clear_data_list:
        obj.clear()
#=======================================================
var_DB_data,var_DB_data_sorted = _take_data_from_server(server)
var_date_of_day,var_arch_VEE_price,var_arch_BTC_price =_data_to_lists(var_DB_data_sorted,var_DB_data)
var_result_list['VEE'] = _vee_checker()
var_result_list['VEE1'] = _vee_checker()
var_result_list['BTC'] = _btc()
var_result_list['BTC1'] = var_arch_BTC_price[-1]
while True:
    day_date = time.strftime("%d.%m.%Y")
    time_now = time.strftime("%H:%M:%S")
    time_H_M = time.strftime("%H:%M")
    try:
        if time_H_M == '00:01' and counter == 0:
            _clearing_current_session_data()
            _take_data_from_server(server)
            var_DB_data,var_DB_data_sorted = _take_data_from_server(server)
            var_date_of_day,var_arch_VEE_price,var_arch_BTC_price =_data_to_lists(var_DB_data_sorted,var_DB_data)
            counter = 1
        if time_H_M in ('00:02') and counter == 1:
            counter = 0
        else:
            _first_loop()
    except KeyboardInterrupt:
        exit()


