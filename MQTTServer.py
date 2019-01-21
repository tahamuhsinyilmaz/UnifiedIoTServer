import paho.mqtt.subscribe as subscribe
import datetime
from database import database


def print_msg(client, userdata, message):
    # print("%s : %s" % (message.topic, message.payload))
    database().insert_value('MQTT',datetime.datetime.now(), str(message.payload))
    # print("TARİH SAAT:" + str(datetime.datetime.now()))
def main():
    subscribe.callback(print_msg, "test",
                   hostname="192.168.1.21")

