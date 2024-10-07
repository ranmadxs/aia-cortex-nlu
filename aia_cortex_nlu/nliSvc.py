from aia_utils.logs_cfg import config_logger
import logging
from transformers import pipeline
from transformers.pipelines import PIPELINE_REGISTRY, get_supported_tasks
from .nli.enum import NLI_LABELS

class NaturalLanguageInferenceSvc:
    
    def __init__(self, model: str = "MoritzLaurer/mDeBERTa-v3-base-mnli-xnli", task: str="zero-shot-classification"):
        config_logger()
        self.logger = logging.getLogger(__name__)
        self.pipeline = pipeline(task=task, model=model, framework = "pt")
        #self.classifier = pipeline("ner", model="stevhliu/my_awesome_wnut_model")
        self.ner = pipeline("ner", model=model)
        self.logger.info(f"[LOAD] pipeline task={task} > model={model}")
        self.candidate_labels =  [e.value['label'] for e in NLI_LABELS]
        self.logger.debug(self.candidate_labels)

    def addCandidateLabels(self, candidate_labels= []):
        self.candidate_labels.extend(candidate_labels)

    def get_classifier(self, msg):
        classi = self.ner(msg)
        return classi

    def bigScore(self, msg):
        resp = self.score(msg)
        resp = list(zip(resp["labels"], resp["scores"]))
        max_score = max(resp, key=lambda x: x[1])
        self.logger.debug(f"max_score={max_score}")
        enum_name = NLI_LABELS.find_enum_by_label(max_score[0])
        self.logger.debug(enum_name)
        ret = {
            "text": msg,
            "label": max_score[0],
            "score": max_score[1],
            "code": enum_name
        }
        return ret


    def score(self, msg):
        resp = self.pipeline(msg, 
                candidate_labels=self.candidate_labels)
        return resp
    