import os, sys, pyaudio, numpy
from sys import stdout
from optparse import OptionParser
# from ndev.core import NDEVCredentials, HEADER, red, green, magenta, blue
# from ndev.asr import ASR, ChunkedASRRequest
from scikits.samplerate import resample
from array import array

import json
import requests
import snowboydecoder
import sys
import signal
import paho.mqtt.client as mqtt
from uuid import getnode as get_mac

print("##########################################################")
print("####  Cognitiva APU - Conversation Desktop Handler #####")
print("##########################################################")

interrupted = False
mac = get_mac()
url = 'http://192.168.40.103/api/RZ2TW5pSvwu6gZYzvKDwHXdt6OY8WLhflUCRB2Bj/lights/1/state'

########### MQTT LOGIC ###############

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("[Cognitiva] Connected to Cognitiva Bridge")

def on_disconnect(client, userdata, rc):
    print("Unexpected disconnection.")
    client.connect_async("104.239.168.238", 1883, 60)
    client.loop_start()

client = mqtt.Client()
client.username_pw_set("mqttC", "Watson2016")
client.on_connect = on_connect
client.on_disconnect = on_disconnect

client.connect_async("104.239.168.238", 1883, 60)
client.loop_start()

def on_publish(client, userdata, mid):
    print("mid: " + str(mid))

########### MQTT LOGIC ###############

########### SNOWBOY LOGIC ###############

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)

model = sys.argv[1]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
print('[Cognitiva] Listening to Watson Hotword... Press Ctrl+C to exit')

# main loop
detector.start(detected_callback=report_hw_signal,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()

########### SNOWBOY LOGIC ###############
