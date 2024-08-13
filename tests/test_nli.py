from transformers import pipeline
from transformers.pipelines import PIPELINE_REGISTRY, get_supported_tasks
from aia_cortex_nlu.nliSvc import NaturalLanguageInferenceSvc
from os import walk
import os
import json

# poetry run pytest tests/test_nli.py::test_pipe2 -s
def test_pipe2():
    print(get_supported_tasks())
    oracle = pipeline(task="zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli", framework = "pt")
    resp = oracle("puedes encender la bomba de agua del invernadero?", 
                candidate_labels=["ejecutar", "warhammer", "email", "conversación"])
    print(resp) 

    resp = oracle("puedes prender la luz del invernadero?", 
                candidate_labels=["ejecutar", "warhammer", "email", "conversación"])
    print(resp)     
    
    resp = oracle("modo warhammer aeldari vyper", 
                candidate_labels=["ejecutar", "warhammer", "email", "conversación"])
    print(resp) 


    resp = oracle("hey amanda puedes leer el email?", 
                candidate_labels=["ejecutar", "warhammer", "email", "conversación"])
    print(resp) 

    resp = oracle("hola cómo estas hoy?", 
                candidate_labels=["ejecutar", "warhammer", "email", "conversación"])
    print(resp) 

# poetry run pytest tests/test_nli.py::test_nli -s
def test_nli():
    print("Test NLI")
    nli = NaturalLanguageInferenceSvc()
    score = nli.score("hola cómo estas hoy?")
    print(score)


# poetry run pytest tests/test_nli.py::test_big_score -s
def test_big_score():
    print("Test NLI")
    nli = NaturalLanguageInferenceSvc()
    score = nli.bigScore("hola cómo estas hoy?")
    print(score)

# poetry run pytest tests/test_nli.py::test_all_msgs -s
def test_all_msgs():
    folder = "tests/resources/messages"
    nli = NaturalLanguageInferenceSvc()
    for filename in os.listdir(folder):
        with open(os.path.join(folder, filename), 'r') as f:
            text = f.read()
            #print (filename)
            #print (text)
            json_data = json.loads(text)
            score = nli.bigScore(json_data["body"]["cmd"])
            print(score)
# poetry run pytest tests/test_nli.py::test_ner -s
def test_ner():
    print("Test NER")
    nli = NaturalLanguageInferenceSvc()
    score = nli.get_classifier("hola cómo estas hoy?")
    print(score)