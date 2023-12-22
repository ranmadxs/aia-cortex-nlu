#!/usr/bin/env python3
# coding: utf8

from dotenv import load_dotenv
import sys
import os
from confluent_kafka import Consumer, KafkaException, KafkaError, Producer
import json
import time
from datetime import datetime

load_dotenv()

class QueueConsumer:
    
    def __init__(self, topic):
        self.topic = topic
        self.conf = {
            'client.id': 'python1Client',            
            'bootstrap.servers': os.environ['CLOUDKARAFKA_BROKERS'],
            'group.id': "%s-consumer2" % (os.environ['CLOUDKARAFKA_USERNAME']),            
            'session.timeout.ms': 6000,
            'default.topic.config': {'auto.offset.reset': 'smallest'},
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'SCRAM-SHA-512',
            'sasl.username': os.environ['CLOUDKARAFKA_USERNAME'],
            'sasl.password': os.environ['CLOUDKARAFKA_PASSWORD']            
        }
        self.consumer = Consumer(**self.conf)
        print("Topic Consumer = " + topic)
        self.consumer.subscribe([topic])

    def validateJSON(self, jsonData):
        try:
            json.loads(jsonData)
        except ValueError as err:
            print(err)
            return False
        return True

    def listen(self, callback_queue = None):
        print('Listener Queue Ready')
        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    # Error or event
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                        (msg.topic(), msg.partition(), msg.offset()))
                    elif msg.error():
                        # Error
                        raise KafkaException(msg.error())
                else:
                    # Proper message
                    #sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
                    #                (msg.topic(), msg.partition(), msg.offset(),
                    #                str(msg.key())))
                    msgValue = msg.value().decode('utf-8').replace("'", '"')
                    print(msgValue)
                    if self.validateJSON(msgValue):
                        res = json.loads(msgValue)
                        callback_queue(res)
                    else:
                        print("[WARN] Not JS Valid")
        except Exception as e:
            print('Error en recibir mensaje')
            print(e)

class QueueProducer:
    def __init__(self, topic, version = None, project_name = "unknown"):
        self.version = version
        self.topic = topic
        self.conf = {
            'bootstrap.servers': os.environ['CLOUDKARAFKA_BROKERS'],
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'SCRAM-SHA-512',
            'sasl.username': os.environ['CLOUDKARAFKA_USERNAME'],
            'sasl.password': os.environ['CLOUDKARAFKA_PASSWORD']            
        }
        self.project_name = project_name
        self.producer = Producer(**self.conf)

    def msgBuilder(self, bodyObject):
        now = datetime.now()
        objMessage = {
            "head": {
                "producer": self.project_name,
                "creationDate": now.strftime("%Y-%m-%d %H:%M:%S"),
                "version": self.version
            }, 
            "body": bodyObject,
            "breadcrumb": [{
                "creationDate": now.strftime("%Y-%m-%d %H:%M:%S"),
                "name": self.project_name
            }],
            "status": {
                "creationDate": now.strftime("%Y-%m-%d %H:%M:%S"),
                "code": "SEND",
                "description": "AIA new message arrived"
            }
        }
        return objMessage

    def sendMsg(self, bodyObject, callback_queue = None):
        objStr = self.msgBuilder(bodyObject)
        self.send(objStr, callback_queue)

    def send(self, msg, callback_queue = None):
        msg_str = json.dumps(msg)
        #msg_str = str(msg)
        print(msg_str)
        self.producer.produce(self.topic, msg_str, callback=callback_queue)
        self.producer.poll(0)
    
    def flush(self):
        self.producer.flush()