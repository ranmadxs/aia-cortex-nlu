from aia_cortex_nlu.id3Svc import get_decision_tree_graph
from aia_utils.logs_cfg import config_logger
import logging
config_logger()
import pandas as pd

logger = logging.getLogger(__name__)

#poetry run pytest tests/test_id3.py::test_treeGraph -s
def test_treeGraph():
    logger.info("Test Tree Graph")
    trainData = pd.read_csv('resources/PlayTennis.csv')
    trainData = pd.read_csv('resources/EmailRead.csv')
    trainData = pd.read_csv('resources/WH40K.csv')
    dataTest = {}
    dot, entrop = get_decision_tree_graph(dataTest, trainData)
    dot.render(view=True, format='png', directory='target', filename='test_treeGraph')

#poetry run pytest tests/test_id3.py::test_treeGraph2DataTest -s
def test_treeGraph2DataTest():
    trainData = pd.read_csv('resources/WH40K.csv')
    dataTest = {'root': 'warhammer', 'obj': 'space', 'nsubj': 'modo', 'amod': 'marine'}
    dot, entrop = get_decision_tree_graph(dataTest, trainData)
    dot.render(view=True, format='png', directory='target', filename='test_treeGraph2.gv')