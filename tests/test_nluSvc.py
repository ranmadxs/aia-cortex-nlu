#https://api.cloudkarafka.com/
import json
import os
#import aia_cortex_nlu.nluSvc
import logging
import logging.config
from aia_cortex_nlu.nluSvc import NLUService
import yaml
from dotenv import load_dotenv
from aia_cortex_nlu import __version__
load_dotenv()

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

#poetry run pytest tests/test_nluSvc.py::test_process -s
def test_process():
    logger.info("Test Process Main Msg")
    data = getSemanticGraph()
    nluSvc = NLUService(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'], os.environ['CLOUDKAFKA_TOPIC_CONSUMER'], __version__)
    nluSvc.process(data)
    
#poetry run pytest tests/test_nluSvc.py::test_buildDataTest -s
def test_buildDataTest():
    logger.info("Test NLU SVC")
    data = getSemanticGraph()
    nluSvc = NLUService(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'], os.environ['CLOUDKAFKA_TOPIC_CONSUMER'], __version__)
    dictResp = nluSvc.buildDataTest(data['nodes'])
    logger.info(dictResp["root"])
    assert (dictResp["root"] == "leer")