from typing import List
from dotenv import load_dotenv
import pandas as pd #for manipulating the csv data
import os
import json
load_dotenv()
#driver = webdriver.Firefox()
from aia_utils.Queue import QueueConsumer, QueueProducer
from .id3Svc import id3, pretty_print_tree, predict, evaluate, get_decision_tree_graph
from aia_utils.logs_cfg import config_logger
import logging
from .nlp.nlp_processor import NLPProcessor
import traceback 
from PIL import Image
import base64
from io import BytesIO
from .nliSvc import NaturalLanguageInferenceSvc
from .nli.enum import NLI_LABELS

class NLUService:

    MIN_SCORE_ACURACY = 0.6

    def __init__(self, topic_producer, topic_consumer, version):
        self.topic_consumer = topic_consumer
        self.topic_producer = topic_producer
        self.queueProducer = QueueProducer(self.topic_producer, version, "aia-cortex-nlu")
        self.version = version
        self.filePath = os.environ['NLU_IMG_FILES_PATH']
        self.nlpProcessor = NLPProcessor()
        self.queueDevice = QueueProducer(os.environ['CLOUDKAFKA_TOPIC_DEVICE_PRODUCER'], version, "aia-cortex-nlu")
        config_logger()
        self.logger = logging.getLogger(__name__)
        self.nli = NaturalLanguageInferenceSvc()

    def kafkaListener(self):
        #queueConsumer = QueueConsumer(os.environ['CLOUDKARAFKA_TOPIC'])
        queueConsumer = QueueConsumer(self.topic_consumer)
        queueConsumer.listen(self.callback)

    def callback(self, aiaMessage: any):
        text = "Llegó un mensaje!"
        print(text)
        #print(str(aiaSemanticGraph))
        if "body" not in aiaMessage:
            self.logger.error("Message without body")
            return
        
        self.logger.info("Process message Aia Message")
        aiaSemanticGraph = self.nlpProcessor.process(aiaMessage)
        self.logger.debug(aiaSemanticGraph)
        self.logger.info("Process message Aia Semmantic Graph")
        result = self.process_all_v2(aiaSemanticGraph)
        
        #for result in results:
        self.logger.info(f"Process {result['body']['cmd']} [{result['result']}]")   
        if(result["result"] == True):
            topic_prod = NLI_LABELS.get_topic_by_enum_name(result['body']['cmd'])
            self.logger.info("Send message to queue " + topic_prod)
            self.logger.debug(result['body'])
            self.queueProducer.topic = topic_prod
            self.queueProducer.send(result['body'])
            #self.sendImgToDev(f"{result['dt_name']}.gv.png")
            #self.queueProducer.send({"body": {"cmd": "READ_YAHOO_MAIL"}})
            self.queueProducer.flush()

    def getChildNodes(self, node, parentIndex):
        if node.parent.index == parentIndex:
            return True
        else:
            return False
    #populated = filter(lambda c: c[1] > 300000000, countries)

    def getRecursiveChildNode(self, nodes: List, parentIndex: int) -> List:
        respNodes = []
        childNodes = list(filter(lambda node: node.__contains__('parent') 
                                 and node['parent'] is not None
                                 and "index" in node['parent']
                                 and node['parent']['index'] == parentIndex, nodes))
        if (len(childNodes) > 0) :
            for child in childNodes:
                recChilds = self.getRecursiveChildNode(nodes, child['index'])
                respNodes += recChilds
        respNodes += childNodes
        return respNodes


    def buildDataTest(self, listNodes: List, keys: List) -> List:
        rootNode = list(filter(lambda node: node['relationType'].lower() == "root", listNodes))
        nodeIdx = rootNode[0]['index']
        listChilds = self.getRecursiveChildNode(listNodes, nodeIdx)
        listChilds.reverse()
        rootNode += listChilds
        dictResp = {}
        for node in rootNode:
            dictResp[node["relationType"]] = node["originalText"]
        
        for key in keys:
            if key not in dictResp:
                dictResp[key] = 'nan'
        return dictResp

    def process_all_v2(self, aiaSemanticGraph):
        results = {}
        try:
            results = self.process_v2(aiaSemanticGraph)

        except Exception as e:
            self.logger.error("Error process_all(aiaSemanticGraph): " + str(e))
            traceback.print_exc() 
        return results
    
    def process_all(self, aiaSemanticGraph) -> List:
        results = []
        try:
            result = self.process(aiaSemanticGraph, "resources/EmailRead.csv")
            result['body']['cmd'] = 'READ_YAHOO_MAIL'
            results.append(result)
        except Exception as e:
            self.logger.error("Error process_all(EmailRead): " + str(e))
            traceback.print_exc() 
        try:
            result = self.process(aiaSemanticGraph, "resources/WH40K.csv")
            result['body']['cmd'] = 'WH40K'
            results.append(result)
        except Exception as e:
            self.logger.error("Error process_all(WH40K): " + str(e))
            traceback.print_exc() 
        return results

    def propositionAlgebraTree(self, train_data_m):
        mainResultNode = train_data_m.keys().to_list()[-1]
        tree, rootTree = id3(train_data_m, mainResultNode)
        print(tree)
        print(rootTree)
        print("#########################################")
        pretty_print_tree(rootTree)
        print("#########################################")
        return tree, rootTree

    def sendImgToDev(self, name: str, format: str = "PNG"):
        image = Image.open(f"{self.filePath}/{name}")
        buffered = BytesIO()
        image.save(buffered, format=format)
        img_str = base64.b64encode(buffered.getvalue())
        self.queueDevice.produce(img_str)
        self.queueDevice.flush()

    def process_v2(self, aiaSemanticGraph):
        self.logger.debug(f"############### Process NLU V2 #####################")
        score = self.nli.bigScore(aiaSemanticGraph["sentence"])

        #todo: en este lugar se debería imprimir el arbol semántico
        result = False
        self.logger.debug(score)
        if (self.MIN_SCORE_ACURACY <= score["score"]):
            result = True
        return {
            "result": result,
            "dataTest": None,
            "accuracy": score["score"],
            "dt_name": score["code"],
            "body": {"cmd": score["code"], "semanticGraph": aiaSemanticGraph},
        }


    def process(self, aiaSemanticGraph, csv):
        self.logger.info(f"############### Process NLU [{csv}] #####################")
        train_data_m = pd.read_csv(csv) #importing the dataset from the disk
        print(train_data_m.to_string()) #viewing some row of the dataset
        print(train_data_m.keys().to_list())
        mainResultNode = train_data_m.keys().to_list()[-1]
        print(mainResultNode)
        #tree, rootTree = self.propositionAlgebraTree(train_data_m)
        print("###################PREDICT 02######################")
        dt_name = csv.split("/")[-1].split(".")[0]
        dt_name = ''.join(dt_name.split())
        self.logger.info("Process NLU: " + dt_name) 
        aiaDataTest = self.buildDataTest(aiaSemanticGraph['nodes'], train_data_m.keys().to_list())
        dot, entropy, resultPredict = get_decision_tree_graph(
            dataTest=aiaDataTest, 
            train_data_m=train_data_m)
        dot.render(view=False, format='png', directory=self.filePath, filename=f"{dt_name}.gv")
        #self.sendImgToDev(f"{dt_name}.gv.png")

        print("----------------aiaDataTest------------------------")
        print(aiaDataTest)
        print(aiaSemanticGraph["sentence"])
        print(resultPredict)
        print("-----------------------------------------------------")
        self.logger.debug(aiaSemanticGraph['nodes'])
        print("")
        print("accuracy: " + str(entropy))
        return {"result": resultPredict, 
                "dataTest": aiaDataTest, 
                "accuracy": entropy,
                "dt_name": dt_name,
                "body": {"cmd":"", "semanticGraph": aiaSemanticGraph},
            }
        #quit() 
