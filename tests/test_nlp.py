import os
from dotenv import load_dotenv
load_dotenv()
from aia_cortex_nlu.nlp.nlp_processor import NLPProcessor
import sys
from nltk import Tree
import json
from aia_utils.logs_cfg import config_logger
import logging
config_logger()
logger = logging.getLogger(__name__)


def getAiaMsg(jsonFile: str):
    logger.info("Read message from file:")
    f = open(jsonFile)
    logger.debug(jsonFile)
    data = json.load(f)
    logger.debug(data)
    return data


#poetry run pytest tests/test_nlp.py::test_process_nlu -s
def test_process_nlu():
    print("Process nlu")
    currentPath = os.getcwd()
    processor = NLPProcessor()
    aiamsg = getAiaMsg(currentPath+"/resources/test/message/wh40k_ancient.json")
    semanthicGraph = processor.process(aiamsg)
    logger.info(type(semanthicGraph))
    logger.debug(semanthicGraph)
    #print(nluSG.print_tree(light=True))
    print("=========================================")

#poetry run pytest tests/test_nlp.py::test_process_genera_aia -s
def test_process_genera_aia():
    print("Process genera aia")
    currentPath = os.getcwd()
    processor = NLPProcessor()
    aiamsg = getAiaMsg(currentPath+"/tests/resources/messages/email01.json")
    semanthicGraph = processor.generateAIASemanticGraph(aiamsg)

    logger.info(type(semanthicGraph))
    logger.debug(semanthicGraph)
    #print(nluSG.print_tree(light=True))
    print("=========================================")