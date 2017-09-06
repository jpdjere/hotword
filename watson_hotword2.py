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

import urllib
import urllib2

import transcribe_streaming_mic

from os import system
from AppKit import NSSpeechSynthesizer
import ast

#Cargo el audio
import pygame
import time
pygame.init()
pygame.mixer.music.load("siri1.wav")




# print blue("##########################################################")
# print blue("####  Cognitiva APU - Conversation Desktop Handler #####")
# print blue("##########################################################")
# print ""


interrupted = False

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

def restCall():
    print("Escuchando")
    #system('say Hola!')
    voice='Diego'
    #Sonido que esta escuchando
    pygame.mixer.music.play()
    #Activo el GoogleSTT y guardo el resultado en speech_transcript
    speech_transcript = urllib2.urlopen('http://localhost:3000/').read()
    # os.system("say -v "+voice+" Sobre quien queres buscar informacion? ")
    print(speech_transcript)
    speech_transcript = ast.literal_eval(speech_transcript)
    print(speech_transcript)
    #Creo los parametros para enviar a EMQTT y lo envio
    params = urllib.urlencode(speech_transcript)
    sent_data = urllib2.urlopen('http://localhost:1880/init?'+params).read()

    # transcribe_streaming_mic.recognize()

if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)

model = sys.argv[1]

signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)


print('Listening... Press Ctrl+C to exit')

detector.start(
               detected_callback=restCall,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
