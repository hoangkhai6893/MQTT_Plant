# # This is script that run when device boot up or wake from sleep.
# import gc
# import time
# from umqtt.simple import MQTTClient
# import ubinascii
# import machine
# import micropython
# import network
# import esp
# from machine import Pin
# from time import sleep
# from machine import Pin, ADC
# from time import sleep

# esp.osdebug(None)
# gc.collect()

# led = Pin(2, Pin.OUT, value=1)
# sensor_2_pw= Pin(13, Pin.OUT, value=1)


# # ssid = 'SPWN_H36_E5B8E2'
# # password = '9amfeyrjry66eh4'
# # mqtt_server = '192.168.100.100'

# ssid = '3104145E'
# password = '0850023821'
# mqtt_server = '192.168.43.43'

# # EXAMPLE IP ADDRESS
# #mqtt_server = '192.168.1.144'
# client_id = ubinascii.hexlify(machine.unique_id())
# topic_sub_1 = b'home/plant_1/control'
# topic_pub_1 = b'home/plant_1/humidity'
# topic_sub_2 = b'home/plant_2/control'
# topic_pub_2 = b'home/plant_2/humidity'

# last_message = 0
# time_delay_state = 5
# counter = 0
# state = b'off'
# station = network.WLAN(network.STA_IF)

# station.active(True)
# station.connect(ssid, password)
# print('Connecting..........')
# while station.isconnected() == False:
#     pass

# print('Connection successful')
# print(station.ifconfig())
# led.value(0)