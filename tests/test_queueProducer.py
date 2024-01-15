#https://api.cloudkarafka.com/
import yaml
from aia_utils.Queue import QueueConsumer, QueueProducer
import os
from dotenv import load_dotenv
load_dotenv()
import json
from aia_cortex_nlu import __version__
from aia_utils.logs_cfg import config_logger
import logging
config_logger()
logger = logging.getLogger(__name__)
currentPath = os.getcwd()


def getSemanticGraph():
    logger.debug("Read message from file:")
    testFile = currentPath + "/resources/test/message/wh40k_sm.json"
    testFile = currentPath + "/resources/test/message/wh40k_ancient.json"
    testFile = currentPath + "/resources/test/message/wh40k_rhino.json"
    testFile = currentPath + "/resources/test/message/wh40k_vyper.json"
   # testFile = currentPath + "/resources/test/message/wh40k_predator.json"
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