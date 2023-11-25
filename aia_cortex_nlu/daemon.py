from argparse import ONE_OR_MORE, ArgumentParser
from . import __version__
from .nluSvc import NLUService
import os
from dotenv import load_dotenv
load_dotenv()

def run():
    """
    entry point
    """
    parser = ArgumentParser(prog="daemon", description="cortex-nlu-daemon")
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    #parser.add_argument(dest="users", nargs=ONE_OR_MORE, type="User", help="your name")
    #args = parser.parse_args()
    print ("Start Daemon cortex NLU")
    nluSvc = NLUService(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'], os.environ['CLOUDKAFKA_TOPIC_CONSUMER'], __version__)
    nluSvc.kafkaListener()