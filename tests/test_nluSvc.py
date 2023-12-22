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

def getSemanticGraph(jsonFile: str):
    logger.debug("Read message from file:")
    testFile = currentPath + "/resources/test/semanticGraphMail.json"
    #testFile = currentPath + "/resources/test/semanticGraphError.json"
    #testFile = currentPath + "/resources/test/semanticGraphWH40k.json"
    f = open(jsonFile)
    logger.debug(jsonFile)
    data = json.load(f)
    logger.debug(data)
    return data

#poetry run pytest tests/test_nluSvc.py::test_process_wh40k -s
def test_process_wh40k():
    logger.info("Test Process Main Msg")
    data = getSemanticGraph(currentPath + "/resources/test/semanticGraphWH40k.json")
    nluSvc = NLUService(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'], os.environ['CLOUDKAFKA_TOPIC_CONSUMER'], __version__)
    result = nluSvc.process(data, "resources/WH40K.csv")
    logger.info(result)
    assert (result["result"] == True)

#poetry run pytest tests/test_nluSvc.py::test_process_all -s
def test_process_all():
    logger.info("Test Process Main Msg")
    data = getSemanticGraph(currentPath + "/resources/test/semanticGraphWH40k.json")
    nluSvc = NLUService(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'], os.environ['CLOUDKAFKA_TOPIC_CONSUMER'], __version__)
    results = nluSvc.process_all(data)
    logger.info(results)
    #assert (result["result"] == True)

#poetry run pytest tests/test_nluSvc.py::test_process_email -s
def test_process_email():
    logger.info("Test Process Main Msg")
    data = getSemanticGraph(currentPath + "/resources/test/semanticGraphMail.json")
    nluSvc = NLUService(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'], os.environ['CLOUDKAFKA_TOPIC_CONSUMER'], __version__)
    result = nluSvc.process(data, "resources/EmailRead.csv")
    logger.info(result)
    assert (result["result"] == True)

#poetry run pytest tests/test_nluSvc.py::test_buildDataTest -s
def test_buildDataTest():
    logger.info("Test NLU SVC")
    data = getSemanticGraph()
    nluSvc = NLUService(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'], os.environ['CLOUDKAFKA_TOPIC_CONSUMER'], __version__)
    dictResp = nluSvc.buildDataTest(data['nodes'])
    logger.info(dictResp["root"])
    assert (dictResp["root"] == "leer")