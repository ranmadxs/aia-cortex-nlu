#https://api.cloudkarafka.com/
import json
import os
#import aia_cortex_nlu.nluSvc
from aia_cortex_nlu.nluSvc import NLUService
import yaml
from dotenv import load_dotenv
from aia_cortex_nlu import __version__
load_dotenv()
from aia_utils.logs_cfg import config_logger
import logging
config_logger()
logger = logging.getLogger(__name__)
import pandas as pd #for manipulating the csv data

currentPath = os.getcwd()

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

def getAiaMsg(jsonFile: str):
    logger.info("Read message from file:")
    f = open(jsonFile)
    logger.debug(jsonFile)
    data = json.load(f)
    logger.debug(data)
    return data

#poetry run pytest tests/test_nluSvc.py::test_algebra -s
def test_algebra():
    logger.info("Test algebra")
    nluSvc = NLUService(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'], os.environ['CLOUDKAFKA_TOPIC_CONSUMER'], __version__)
    train_data_m = pd.read_csv("resources/WH40K.csv") 
    nluSvc.propositionAlgebraTree(train_data_m)

#poetry run pytest tests/test_nluSvc.py::test_callback -s
def test_callback():
    logger.info("Test callback")
    nluSvc = NLUService(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'], os.environ['CLOUDKAFKA_TOPIC_CONSUMER'], __version__)
    aiamsg = getAiaMsg(currentPath+"/resources/test/message/wh40k_vyper.json")
    aiamsg = getAiaMsg(currentPath+"/resources/test/message/email01.json")
    resp = nluSvc.callback(aiamsg)
    logger.info(resp)


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