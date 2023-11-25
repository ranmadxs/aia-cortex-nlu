#!/usr/bin/env python3
# coding: utf8

import pyttsx3
from dotenv import load_dotenv
from kafka.Queue import QueueConsumer
import os
import gtts
from playsound import playsound

load_dotenv()


queueConsumer = QueueConsumer(os.environ['CLOUDKARAFKA_TOPIC'])

def callback(msgDict):
    text = "Llegó un mensaje!"
    print(text)


queueConsumer.listen(callback)

