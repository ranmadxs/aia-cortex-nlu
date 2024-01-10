from aia_utils.logs_cfg import config_logger
import logging
import spacy
import sys
from nltk import Tree
from aia_cortex_nlu.model import AIASemanticGraph, AIASemanticGraphNode, AIAMessageHeader, AIABreadcrumb
from typing import List
from nltk.tree.prettyprinter import TreePrettyPrinter
from io import StringIO
from aia_cortex_nlu import __version__
import datetime
from aia_utils.repositories.aia_semantic_repo import AIASemanticGraphRepository
import os
from spacy import displacy

class NLPProcessor:
    def __init__(self) -> None:
        config_logger()
        self.logger = logging.getLogger(__name__)
        self.nlp = spacy.load("es_core_news_sm")
        self.aiaRepo = AIASemanticGraphRepository(os.environ['MONGODB_URI'])

    def tok_format(self, tok):
        return "_".join([tok.orth_, tok.dep_])


    def to_nltk_tree(self, node):
        if node.n_lefts + node.n_rights > 0:
            return Tree(self.tok_format(node), [self.to_nltk_tree(child) for child in node.children])
        else:
            return self.tok_format(node)

    def showTree(self, sent):
        def __showTree(token, result = ''):
            #sys.stdout.write("{")
            result += "{"
            for t in token.lefts:
                result += __showTree(t)
            #sys.stdout.write("%s->%s(%s)" % (token,token.dep_,token.tag_))
            result += "%s->%s(%s)" % (token,token.dep_,token.tag_)
            for t in token.rights:
                result += __showTree(t)            
            #[__showTree(t, result) for t in token.rights]
            #sys.stdout.write("}")
            result += "}"
            return result
        return __showTree(sent)

    def process(self, aiaMsg: any) -> None:
        aiaSemanticGraph = None
        if ("cmd" in aiaMsg['body'] 
            and "isAia" in aiaMsg['body'] 
            and aiaMsg['body']['isAia'] == True):
            
            aiaSemanticGraph = self.generateAIASemanticGraph(aiaMsg)
        else:
            self.logger.error("Message is not aia format")

        return aiaSemanticGraph
    
    def generateAIASemanticGraph(self, aiaMsg: any):
        id = None
        listNodes = []
        text = aiaMsg['body']['cmd']
        if text[-1] != ".":
            text += "."
        classification = aiaMsg['body']['classification']

        if "id" in aiaMsg:
            id = aiaMsg['id']
        if "_id" in aiaMsg:
            id = aiaMsg['_id']
        nluSG = self.nlp(text)
        self.logger.debug(nluSG.to_json())
        semanticTree = None
        dotFormat = None
        self.logger.info(type(nluSG.sents))
        arraySents = []
        for sent in nluSG.sents:
            print("====sents=====")
            self.logger.info(type(sent))
            self.logger.debug(sent)
            self.logger.debug(sent.root)
            arraySents.append(sent)
        print(">>>>>>>>>>>>>>> TOKENS <<<<<<<<<<<<<<<<<")
        print([f"{token.text} tag:{token.pos_} index:{token.i} {token.dep_}" for token in nluSG])
        #displacy.serve(nluSG, style="dep", port=8082)
        semanticTree = ""
        dotFormat = ""
        for sent in nluSG.sents:
            #self.logger.info(type(sent.root))
            #self.logger.debug(sent)
            semanticTree = str(semanticTree) + str(self.showTree(sent.root))
            textToPrint = ""
            streamPrint = StringIO(textToPrint)
            nltk_tree = self.to_nltk_tree(sent.root)
            if isinstance(nltk_tree, str):
                #print(dir(sent.sent))
                dotFormat = f"{dotFormat} {sent.text}"
            else:
                self.to_nltk_tree(sent.root).pretty_print(stream=streamPrint)
                dotFormat = f"{dotFormat} {streamPrint.getvalue()}"
        print("=========================================")
        print(semanticTree)
        print(dotFormat)
        for nluDoc in nluSG:
            #print("-----------------------------------------")
            #print(f"{type(nluDoc)}", nluDoc.text, nluDoc.pos_, nluDoc.dep_, nluDoc.i)
            semanticNodeTree = self.showTree(nluDoc)
            #print("")
            #print(type(nluDoc.ancestors))
            ancestors = []
            #[print(f"{type(t)}", t.text, t.pos_, t.dep_, t.i) for t in nluDoc.ancestors]
            [ancestors.append({"originalText": t.text, "tag": t.pos_, "index": t.i}) for t in nluDoc.ancestors]
            #print("-----------------------------------------")
            parent = None
            if len(ancestors) > 0:
                parent = ancestors[0]
            aIASemanticGraphNode = AIASemanticGraphNode(
                nluDoc.text.lower(), 
                nluDoc.pos_.lower(), 
                nluDoc.i, 
                nluDoc.dep_.lower(), 
                parent, 
                semanticNodeTree)
            listNodes.append(aIASemanticGraphNode)

        dateNow = datetime.datetime.now()
        aiaHeader = AIAMessageHeader("aia_cortex_nlu", dateNow, __version__)
        aiaBread = AIABreadcrumb("aia_cortex_nlu", dateNow)
        aIASemanticGraph = AIASemanticGraph(
            aiaHeader,
            [aiaBread],
            semanticTree, 
            dotFormat, 
            nluSG.to_json(), 
            text, 
            id, 
            listNodes, 
            classification, 
            None)
        idAia= self.aiaRepo.save(aIASemanticGraph)
        merged_dict = aIASemanticGraph.dict()
        merged_dict['id'] = idAia
        return merged_dict