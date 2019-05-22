import requests,os,time,redis
from back_end_Vee_Checker import _take_data_from_server,_write_to_server,_vee_checker,_btc,_info_to_msg,_data_to_lists
#=======================================================
server = redis.Redis('3.8.101.205', charset="utf-8", decode_responses=True, db=0)
var_alarm_vee = 0.006
var_alarm_btc = 8300
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
        VEE: {} USD   $
        BTC : {} USD  {}$""".format(var_result_list['VEE'],
                                    var_result_list['BTC'],
                                    var_result_list['BTC'] - var_result_list['BTC1'])
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
def _clearing_current_session_data():
    for obj in var_clear_data_list:
        obj.clear()
#=======================================================
while True:
    day_date = time.strftime("%d.%m.%Y")
    time_now = time.strftime("%H:%M:%S")
    time_H_M = time.strftime("%H:%M")
    try:
        if var_result_list['VEE'] >= var_alarm_vee:
            _info_to_msg(var_result_list)
            var_alarm_vee += 0.006
        if var_result_list['BTC'] >= var_alarm_btc:
            _info_to_msg(var_result_list)
            var_alarm_btc += 600
        if time_H_M == '12:00' or time_H_M == '18:00' or time_H_M == '23:49'and counter == 0:
            var_current_price_vee.append(var_result_list['VEE'])
            var_current_price_btc.append(int(var_result_list['BTC']))
            counter = 1
        if time_H_M == '23:51' and counter == 0:
            temp_list = {'BTC':sum(var_current_price_btc), 'VEE': sum(var_current_price_vee)}
            _write_to_server(server, day_date, temp_list,len(var_current_price_vee),len(var_current_price_btc))
            _clearing_current_session_data()
            _take_data_from_server(server)
            var_DB_data,var_DB_data_sorted = _take_data_from_server(server)
            var_date_of_day,var_arch_VEE_price,var_arch_BTC_price =_data_to_lists(var_DB_data_sorted,var_DB_data)
            counter = 1
        if time_H_M == '12:01'or time_H_M == '18:51' or time_H_M == '18:01' or time_H_M == '23:50' and counter == 1:
            counter = 0
        else:
            _first_loop()
    except KeyboardInterrupt:
        exit()


