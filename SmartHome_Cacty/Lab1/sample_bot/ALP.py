# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 15:18:46 2020

@author: dacca
"""
import tensorflow as tf

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

### TEMPORARY TO TEST BEFORE PLUGING TO DATABASE
from rasa.nlu.model import Interpreter

# run 'pip install pymongo' to install this lib
from pymongo import MongoClient
import json

MODEL_ADDR = "./NLU/models/nlu-20200216-142039/nlu"
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
#MONGODB_URL = "mongodb://0.tcp.ngrok.io:10277"
#MONGODB_URL = "mongodb://0.tcp.ngrok.io:11014/?compressors=disabled&gssapiServiceName=mongodb"
MONGODB_URL= "mongodb://0.tcp.ngrok.io:14723/?compressors=disabled&gssapiServiceName=mongodb"


LOCATION_TO_ZONE = {"living" : "A", # living room
                    "washroom" : "B", # washroom
                    "pantry" : "C", 
                    "kitchen" : "D", 
                    "entrance" : "E", # entrance hall
                    "garage" : "F", 
                    "hallway" : "G", 
                    "bedroom one" : "H", # kids room
                    "bathroom one" : "I", # bathroom
                    "bedroom two" : "J",  # single bedroom
                    "bathroom two" : "K", # bathroom
                    "bedroom three" : "L", # double bedroom
                    "laundry" : "M", 
                    "office" : "N",
                    "exterior" : "O"} # also include gate, pool and lights

ENTITY_TO_DATABASE_NAME = {
                "light" : "Light",
                "heater" : "Heater"
            }

HEATING_CHANGE_RATE = 0.2

ACTION_TO_DB_VALUE_MAPPING = {
        "turn on": lambda x: "true",
        "turn off": lambda x: "false",
        "increase": lambda x: x*(1+HEATING_CHANGE_RATE),
        "decrease": lambda x: x*(1-HEATING_CHANGE_RATE)
    }

THRESHOLD = 0.5

class ActionLanguageProcessor():
    
    
    def __init__(self, mongodb_url, model_file):
        self.DB_CLIENT = MongoClient(mongodb_url)
        # I created a database called simple_appliances_db
        self.db = self.DB_CLIENT.shome
        # loading the model from one directory or zip file
        self.interpreter = Interpreter.load(model_file)
        
        self.action_device_mapping = {
                        "light" : {
                                "actions":["turn on", "turn off"],
                                "collection": self.db.homeio
                                },
                      "heater" : {
                                  "actions":["increase", "decrease", "turn on", "turn off"],
                                  "collection": self.db.homeio
                                  }
                          }

    def __str__(self):
        return str(self.action_device_mapping)
    
    def analyse_utterance(self, utterance="can you give me an eco-friendly fact"):
        # parsing the utterance
        interpretation = self.interpreter.parse(utterance)
        
        if interpretation["intent"]['name'] == "take_action":
            return self._take_action(interpretation)
        elif interpretation["intent"]['name'] == "get_info":
            return self._eco_friendly_fact(interpretation)
        
        
    def _eco_friendly_fact(self, interpretation):
        collection = self.db.homeiofact

        answer = collection.aggregate([{ "$sample": { "size": 1 } }])

        fact = [tmp for tmp in answer][0]
        #answer.parse()
        return fact['Fact'] 
        
    def _take_action(self, interpretation):
        location, appliance, action = (None for _ in range(3))
        
        for entity in interpretation['entities'] :
            if entity['entity'] == "location" :
                location = entity['value'] if location is None else entity['value']+' '+location
            if entity['entity'] == "appliance" :
                appliance = entity['value']
            if entity['entity'] == "action" :
                action = entity['value']
            if entity['entity'] == "number":
                location = entity['value'] if location is None else location+' '+entity['value']
        

        location = ActionLanguageProcessor._maximumStrSimilarity(location,LOCATION_TO_ZONE.keys())    
        appliance = ActionLanguageProcessor._maximumStrSimilarity(appliance,ENTITY_TO_DATABASE_NAME.keys())    
        
        if location != None and appliance != None and action != None:
            print(location+" "+ appliance+" "+action)
            if (appliance.lower() in self.action_device_mapping.keys() #We check the appliance is managed (i.e in ACTION_DEVICE_MAPPING)
            and action.lower() in self.action_device_mapping[appliance]["actions"]): #We check the action is supported by the appliance
                
                
                 
                #CODE FOR DB QUERY
                collection = self.action_device_mapping[appliance.lower()]["collection"] 
                
                list_of_devices = collection.find({
                        "zone": LOCATION_TO_ZONE[location.lower()],#Everything that matches this zone requirements ,
                        "appliance": {'$regex':f'^{ENTITY_TO_DATABASE_NAME[appliance]}', "$options":"-i"}
                })

            
                for device in list_of_devices:
                    print(device)
                    collection.update({
                            "address": device["address"]#The device that matches this address
                            },{
                                "$set": {"state": ACTION_TO_DB_VALUE_MAPPING[action.lower()](device["state"]) }
                            })
                
                return f"Yes ! I {action} the {appliance} in {location}"
            
            #If incorrect, leaves the if and returns error NLG message
            
        # IN CASE OF WRONGLY SYNTAXED QUERIES
        print(interpretation)
        return "Sorry, I did not understand, could you repeat ?"
    
    def _maximumStrSimilarity(entity,keys):
        """
        find the location matching the most the available rooms
        if threshold is not met return None
        """
        percent = THRESHOLD
        key=None
        for word in keys:
            smallest = len(word) if len(word)<len(entity) else len(entity)
            temp=0
            for j in range(smallest):
                temp +=1 if entity[j].lower()==word[j].lower() else 0
            
            if (temp/smallest>percent):
                percent = temp/smallest
                key = word
                
        return key
            

if __name__ == "__main__":
    utterance = "can you turn on the light in the kitchen"
    alp = ActionLanguageProcessor(mongodb_url=MONGODB_URL, model_file=MODEL_ADDR)
    print(alp.analyse_utterance(utterance))
    