# This is script that run when device boot up or wake from sleep.
import gc
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
from machine import Pin
from time import sleep
from machine import Pin, ADC
from time import sleep

esp.osdebug(None)
gc.collect()

led = Pin(2, Pin.OUT, value=1)
sensor_2_pw = Pin(13, Pin.OUT, value=1)
sensor_12_pw = Pin(12, Pin.OUT, value=1)


# ssid = 'SPWN_H36_E5B8E2'
# password = '9amfeyrjry66eh4'
# mqtt_server = '192.168.100.100'

ssid = '3104145E'
password = '0850023821'
mqtt_server = '192.168.43.43'

# EXAMPLE IP ADDRESS
# mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub_1 = b'home/plant_1/control'
topic_pub_1 = b'home/plant_1/humidity'
topic_pub_2 = b'home/plant_2/humidity'


state = b'off'
station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)
print('Connecting..........')
while station.isconnected() == False:
    pass

print('Connection successful')
print(station.ifconfig())
led.value(0)


def convert_to_percent(value, min_val, max_val):
    if value > min_val:
        value = min_val
    if value < max_val:
        value = max_val

    sub = value - min_val
    range_sensor = max_val - min_val
    output = sub * 100 / range_sensor
    return int(output)


def get_Value_humidity():
    pass


def sub_cb(topic, msg):

    print((topic, msg))
    if msg == b"on":
        led.value(1)
        # control_pumer('on')
    elif msg == b"off":
        led.value(0)

        # control_pumer('off')
    else:
        pass


def connect_and_subscribe():
    global client_id, mqtt_server, topic_sub_1
    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub_1)
    print('Connected to %s MQTT broker, subscribed to %s topic' %
          (mqtt_server, topic_sub_1))
    return client


def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()


try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()
last_message = 0
time_delay_state = 1
time_count_down = 0



max_value_plant_1 = 1200
min_value_plant_1 = 2500


max_value_plant_2 = 1000
min_value_plant_2 = 2500


humidity_Plant_1 = ADC(Pin(34))
humidity_Plant_2 = ADC(Pin(35))
humidity_Plant_1.atten(ADC.ATTN_11DB)  # Full range: 3.3v
humidity_Plant_2.atten(ADC.ATTN_11DB)  # Full range: 3.3v

while True:


    try:
        client.check_msg()
        led.value(0)
        time_count_down = time_delay_state - (time.time() - last_message)
        if time_count_down < 0:
            led.value(1)
            last_message = time.time()
            pot_value_1 = humidity_Plant_1.read()
            pot_value_2 = humidity_Plant_2.read()
            percent_humidity_1 = convert_to_percent(
                pot_value_1, min_value_plant_1, max_value_plant_1)
            percent_humidity_2 = convert_to_percent(
                pot_value_2, min_value_plant_2, max_value_plant_2)

            client.publish(topic_pub_1, str(percent_humidity_1))
            client.publish(topic_pub_2, str(percent_humidity_2))

            print(percent_humidity_1)
            print(percent_humidity_2)
            print(int(pot_value_1))
            print(int(pot_value_2))
    except OSError as e:
        restart_and_reconnect()
