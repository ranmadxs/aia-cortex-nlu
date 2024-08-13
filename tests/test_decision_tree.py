from aia_cortex_nlu.nlp.p_decision_tree import DecisionTree
import pandas as pd
from aia_utils.logs_cfg import config_logger
import logging
config_logger()
logger = logging.getLogger(__name__)
from graphviz import Digraph
import traceback 
import pydot
import json

#brew install graphviz   -> apt get install graphviz


#poetry run pytest tests/test_decision_tree.py::test_graphviz -s
def test_graphviz():
    (graph,) = pydot.graph_from_dot_file('resources/test/graphviz_sample.gv')
    graph.write_png('target/graphviz_sample.png')
    #graph.render('resources/test/graphviz_sample.gv', view=True)

#poetry run pytest tests/test_decision_tree.py::test_decision_tree -s
def test_decision_tree():
    logger.info("Test Decision Tree")
    #Reading CSV file as data set by Pandas
    data = pd.read_csv('resources/PlayTennis.csv')
    data = pd.read_csv('resources/EmailRead.csv')
    data = pd.read_csv('resources/WH40K.csv')
    columns = data.columns
    logger.debug(columns)
    #All columns except the last one are descriptive by default
    descriptive_features = columns[:-1]
    #The last column is considered as label
    label = columns[-1]

    #Converting all the columns to string
    for column in columns:
        data[column]= data[column].astype(str)
    
    data_descriptive = data[descriptive_features].values
    data_label = data[label].values

    print(f"data_descriptive= {data_descriptive}, data_label= {data_label}")

    #Calling DecisionTree constructor (the last parameter is criterion which can also be "gini")
    decisionTree = DecisionTree(data_descriptive.tolist(), descriptive_features.tolist(), data_label.tolist(), "entropy")
    
    #Here you can pass pruning features (gain_threshold and minimum_samples)
    decisionTree.id3(0,0)

    #Visualizing decision tree by Graphviz
    dot, resultPredict = decisionTree.get_visualTree()
    dot.render(directory='target', view=True, format='png', filename='ejem_decision_tree.gv')
    # When using Jupyter
    #display( dot )
    #try:
        #dot.render('output/visualTree.gv', view=True)
        #(graph,) = pydot.graph_from_dot_file('output/visualTree.gv')
        #graph.write_png('target/somefile.png')
    #except:
        #traceback.print_exc() 
        #print("You either have not installed the 'dot' to visualize the decision tree or the reulted .pdf file is open!")
    print("System entropy: ", format(decisionTree.entropy))
    print("System gini: ", format(decisionTree.gini))