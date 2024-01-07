from typing import List
from dotenv import load_dotenv
import pandas as pd #for manipulating the csv data
import os
import json
load_dotenv()
#driver = webdriver.Firefox()
from aia_utils.Queue import QueueConsumer, QueueProducer
from .id3Svc import id3, pretty_print_tree, predict, evaluate
from aia_utils.logs_cfg import config_logger
import logging
from .nlp.nlp_processor import NLPProcessor
import traceback 

class NLUService:

    def __init__(self, topic_producer, topic_consumer, version):
        self.topic_consumer = topic_consumer
        self.topic_producer = topic_producer
        self.queueProducer = QueueProducer(self.topic_producer, version, "aia-cortex-nlu")
        self.version = version
        self.nlpProcessor = NLPProcessor()
        config_logger()
        self.logger = logging.getLogger(__name__)

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
        results = self.process_all(aiaSemanticGraph)
        
        for result in results:
            self.logger.info(f"Process {result['body']['cmd']} [{result['result']}]")   
            if(result["result"] == True):
                self.logger.info("Send message to queue " + self.topic_producer)
                self.logger.debug(result['body'])
                self.queueProducer.send(result['body'])
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


    def buildDataTest(self, listNodes: List) -> List:
        rootNode = list(filter(lambda node: node['relationType'].lower() == "root", listNodes))
        nodeIdx = rootNode[0]['index']
        listChilds = self.getRecursiveChildNode(listNodes, nodeIdx)
        listChilds.reverse()
        rootNode += listChilds
        dictResp = {}
        for node in rootNode:
            dictResp[node["relationType"]] = node["originalText"]
        return dictResp

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

    def process(self, aiaSemanticGraph, csv):
        self.logger.info("Process NLU")
        train_data_m = pd.read_csv(csv) #importing the dataset from the disk
        print(train_data_m.to_string()) #viewing some row of the dataset
        mainResultNode = train_data_m.keys().to_list()[-1]
        print(mainResultNode)
        tree, rootTree = id3(train_data_m, mainResultNode)
        print(tree)
        print(rootTree)
        print("#########################################")
        pretty_print_tree(rootTree)
        print("")
        print("###################PREDICT 02######################")
        #for node in aiaSemanticGraph['nodes']:
        #    print(node)

        #print(aiaSemanticGraph['nodes'])    
        #rootNodes = filter(getRootNode, aiaSemanticGraph['nodes'])
        #filtered_arr = [node for node in aiaSemanticGraph['nodes'] if node.relationType == "root"]

        #print("-------------rootNode---------------------------")
        self.logger.debug(aiaSemanticGraph['nodes'])
        aiaDataTest = self.buildDataTest(aiaSemanticGraph['nodes'])
        '''
        dataTest = {
            'root': 'leer',
            'obj': 'noticias',
            'nmod': 'yahoo',
            'case': 'None',
        }
        resultPredict = predict(tree, dataTest)
        print("------------------dataTest----------------------")
        print(dataTest)
        print(resultPredict)
        '''
        print("----------------aiaDataTest------------------------")
        resultPredict = predict(tree, aiaDataTest)
        print(aiaDataTest)
        print(resultPredict)
        print("-----------------------------------------------------")
        accuracy = evaluate(tree, train_data_m, mainResultNode) #evaluating the test dataset
        print("")
        print("accuracy: " + str(accuracy))
        return {"result": resultPredict, 
                "dataTest": aiaDataTest, 
                "accuracy": accuracy,
                "body": {"cmd":"", "semanticGraph": aiaSemanticGraph},
            }
        #quit() 
