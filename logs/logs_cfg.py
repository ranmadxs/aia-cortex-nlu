from dotenv import load_dotenv
import logging
import logging.config
import yaml
import os

def getLogger():
    currentPath = os.getcwd()
    with open(currentPath+"/resources/log_cfg.yaml", 'rt') as f:
        configLog = yaml.safe_load(f.read())
        logging.config.dictConfig(configLog)
    logger = logging.getLogger(__name__)
    return logger