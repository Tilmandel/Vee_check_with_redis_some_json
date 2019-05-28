import time,redis,os
from back_end_Vee_Checker import _take_data_from_server,_write_to_server,_vee_checker,_btc,_info_to_msg,_data_to_lists
#=======================================================
server = redis.Redis('3.8.101.205', charset="utf-8", decode_responses=True,password='password', db=0)
var_current_price_vee = []
var_current_price_btc = []
var_result_list = {}
var_clear_data_list = [var_current_price_vee,
                       var_current_price_btc]
counter = 0
var_DB_data,var_DB_data_sorted = _take_data_from_server(server)
var_date_of_day,var_arch_VEE_price,var_arch_BTC_price =_data_to_lists(var_DB_data_sorted,var_DB_data)
var_result_list['VEE'] = _vee_checker()
var_result_list['VEE1'] = _vee_checker()
var_result_list['BTC'] = _btc()
var_result_list['BTC1'] = var_arch_BTC_price[-1]
#=======================================================
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
def _clearing_current_session_data():
    for obj in var_clear_data_list:
        obj.clear()
#=======================================================
while True:
    day_date = time.strftime("%d.%m.%Y")
    time_now = time.strftime("%H:%M:%S")
    time_H_M = time.strftime("%H:%M")
    try:
        if time_H_M == '23:59' and counter == 0:
            _clearing_current_session_data()
            _take_data_from_server(server)
            var_DB_data,var_DB_data_sorted = _take_data_from_server(server)
            var_date_of_day,var_arch_VEE_price,var_arch_BTC_price =_data_to_lists(var_DB_data_sorted,var_DB_data)
            counter = 1
        if time_H_M in ('00:00') and counter == 1:
            counter = 0
        else:
            _first_loop()
    except KeyboardInterrupt:
        exit()


