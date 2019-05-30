# Vee_check_with_redis_some_json

#Back_end_that_runs_on_server
""" this should be runned on server as process.
collecting data for prive of BTC and VEE,
BTC with api and JSon
VEE is scraping from sitecode.
Everything is saved on redis server with Key(date) : Value pairs (where values is two Dict one For VEE and one for BTC.)
Saving time is 23:59 just before day ends."""


#Front_end_dis_back_end_for_it
"""
This is client that can be runned on user PC, this is only taking data from redis server,
add them to list wit aligation to fit display correctly
unwanted signs are removed do the replacmant function, After that everything land on display.
Current price is displayed on 5s base.

Time of reload archive Data is 00:01 to take new data from server.
"""
