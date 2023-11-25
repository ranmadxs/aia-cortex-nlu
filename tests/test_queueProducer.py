#https://api.cloudkarafka.com/
import yaml
from kafka.Queue import QueueConsumer, QueueProducer
import os
from dotenv import load_dotenv
load_dotenv()
import json
import logging
import logging.config
from aia_cortex_nlu import __version__

currentPath = os.getcwd()
with open(currentPath+"/resources/log_cfg.yaml", 'rt') as f:
    configLog = yaml.safe_load(f.read())
    logging.config.dictConfig(configLog)
logger = logging.getLogger(__name__)

def getSemanticGraph():
    logger.debug("Read message from file:")
    testFile = currentPath + "/tests/semanticGraphExample.json"
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
    data = json.dumps(getSemanticGraph())
    queueProducer.send(data.replace("'", '\\"'))
    queueProducer.flush()