#https://api.cloudkarafka.com/
import yaml
from kafka.Queue import QueueConsumer, QueueProducer
from logs.logs_cfg import getLogger
import os
from dotenv import load_dotenv
load_dotenv()
import json
from aia_cortex_nlu import __version__

currentPath = os.getcwd()
logger = getLogger()

def getSemanticGraph():
    logger.debug("Read message from file:")
    testFile = currentPath + "/resources/test/sgWh40kN1.json"
    f = open(testFile)
    logger.debug(testFile)
    data = json.load(f)
    logger.debug(data)
    return data

#poetry run pytest tests/test_queueProducer.py::test_produce -s
def test_produce():
    topicProducer = os.environ['TEST_CLOUDKAFKA_TOPIC_PRODUCER']
    logger.info("Test Produce queue " + topicProducer)
    queueProducer = QueueProducer(topicProducer, __version__, "aia-cortex-nlu")
    data = getSemanticGraph()
    #data = json.dumps(data)
    #data = data.replace("'", '\\"')
    queueProducer.send(data)
    queueProducer.flush()