from pymongo import MongoClient
import csv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import os
from dotenv import load_dotenv

DB_NAME = 'CarletonPathwaysDB'

class MongoSaver:
    def __init__(self):
        load_dotenv()

        #Connects to the Mongo client
        self.client = MongoClient(os.getenv('URI'), server_api=ServerApi('1'))
        
    def save_csv_to_mongo(self, collection_name, csv_path): 
        
        #Specifies what Database and collection to add to
        self.client.admin.command('ping')
        database = self.client[DB_NAME]
        collection = database[collection_name]
        try:
            #Opens CSV and adds to MongoDB
            with open(csv_path, 'r',encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    collection.insert_one(row)

            print("Sucessfully connected and inserted data")
            
        except Exception as e:
            print(e)

    def delete_all(self):
        # Access the desired database
        database = self.client[DB_NAME]

        # Access the collection
        collection = database["crns"]

        # Delete all documents in the collection
        collection.delete_many({})
        
        # Access the collection
        collection = database["courses"]

        # Delete all documents in the collection
        collection.delete_many({})

        print("Deleted all documents in Courses and Crns")
    


    def close_mongo_connection(self):
        self.client.close() 