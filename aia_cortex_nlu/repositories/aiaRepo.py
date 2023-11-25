import os
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

class AIASemanticGraphRepository:
  aiaDB: None

  def __init__(self, connectionString):
    connectiondmr = MongoClient(connectionString)
    self.aiaDB = connectiondmr["aia-db"]


  def update(self, aiaMessage):
      _id = self.aiaDB["aIASemanticGraph"].insert_one(aiaMessage)
      return _id.inserted_id