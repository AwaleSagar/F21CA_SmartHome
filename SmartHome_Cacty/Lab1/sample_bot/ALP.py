# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 15:18:46 2020

@author: dacca
"""
import tensorflow as tf
import datetime
import requests
from word2number import w2n
import pandas as pd
from pprint import pprint
# import sklearn

# print('The scikit-learn version is {}.'.format(sklearn.__version__))

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

### TEMPORARY TO TEST BEFORE PLUGING TO DATABASE
from rasa.nlu.model import Interpreter

# run 'pip install pymongo' to install this lib
from pymongo import MongoClient

MODEL_ADDR = "./NLU/models/20200310-190259/nlu"
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
#MONGODB_URL = "mongodb://0.tcp.ngrok.io:10277"
MONGODB_URL = "mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb"

## WAGI API PARAMS
API_KEY = "dc7cf06b49047ee83091c9c350abcf80db6fbd43"
API_URL = f"https://api.waqi.info/feed/edinburgh/?token={API_KEY}"

## DATASET PARAMS
DATASET_FILE_NAME = "edi_air_quality.csv"
DATASET_PATH = f"NLU/data/{DATASET_FILE_NAME}"

THRESHOLD = 0.5

dataset = pd.read_csv(DATASET_PATH)

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

ENERGY_CONSUMPTION_ADDRESSES = {
    "hour":146,
    "day":147,
    "week":148,
    "month":149
        }

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
            
    
    def analyse_utterance(self, utterance="can you give me an eco-friendly fact"):
        # parsing the utterance
        interpretation = self.interpreter.parse(utterance)
        
        pprint(interpretation)
        
        if interpretation["intent"]['name'] == "take_action":
            return self._take_action(interpretation)
        elif interpretation["intent"]['name'] == "get_info":
            return self._eco_friendly_fact(interpretation)
        elif interpretation["intent"]["name"] == "air_quality_today":
            return self._get_today_air_quality(interpretation)
        elif interpretation["intent"]["name"] == "air_quality_historical":
            return self._get_historical_air_quality(interpretation)
        elif interpretation["intent"]["name"] == "get_info_energy":
            return self._get_energy_consumption(interpretation)

        
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
                location = entity['value']
            if entity['entity'] == "appliance" :
                appliance = entity['value']
            if entity['entity'] == "action" :
                action = entity['value']
                
        location = ActionLanguageProcessor._maximumStrSimilarity(location,LOCATION_TO_ZONE.keys())    
        appliance = ActionLanguageProcessor._maximumStrSimilarity(appliance,ENTITY_TO_DATABASE_NAME.keys())    
        

        if location != None and appliance != None and action != None:
            
            if (appliance.lower() in self.action_device_mapping.keys() #We check the appliance is managed (i.e in ACTION_DEVICE_MAPPING)
            and action in self.action_device_mapping[appliance]["actions"]): # We check the location exists
                #CODE FOR DB QUERY
                collection = self.action_device_mapping[appliance.lower()]["collection"] 
                
                list_of_devices = collection.find({
                        "zone": LOCATION_TO_ZONE[location.lower()],#Everything that matches this zone requirements ,
                        "appliance": {'$regex':f'^{ENTITY_TO_DATABASE_NAME[appliance]}$'}
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
        return "Sorry, I did not understand, could you repeat ?"

    def _get_today_air_quality(self, interpretation):
        r = requests.get(url=API_URL)
        response = r.json()
        #print(interpretation)
        returned_response = f"""
            Today's air is as follows:
            - h: {response['data']['iaqi']['h']['v']}
            - no2: {response['data']['iaqi']['no2']['v']}
            - o3: {response['data']['iaqi']['o3']['v']}
            - p: {response['data']['iaqi']['p']['v']}
            - pm10: {response['data']['iaqi']['pm10']['v']}
            - pm25: {response['data']['iaqi']['pm25']['v']}
            - so2: {response['data']['iaqi']['so2']['v']}
            """
        return returned_response
        
    def _get_historical_air_quality(self, interpretation):
                
        def row_is_between_dates(row, low_date, up_date):
            date_row = row["date"].split("/")
            
            true_date_row = datetime.date(int(date_row[2]), int(date_row[1]), int(date_row[0]))
        
            return true_date_row <= up_date and true_date_row > low_date
        
        returned_response = "I did not get that. Could you repeat ?"

        returned_response = ""

        number = None
        hierarchy_number = None
        time_measures = None
        for entity in interpretation['entities']:

            if entity["entity"] == "hierarchy_number":
                hierarchy_number = entity["value"]

            elif entity["entity"] == "time":
                time_measures = entity["value"]

            elif entity["entity"] == "number":
                number = entity["value"]

        if number is None and hierarchy_number is None and time_measures is None:
            returned_response = "Query not fully understood, returning last week data by default:"
            hierarchy_number = "last"
            time_measures = "week"

        # count the number of unit of time measures
        counter = 1
        # convert the unit of time measures as days
        time_measure_factor = 1

        if (time_measures[0:4] == "week"):
            time_measure_factor = 7
        elif (time_measures[0:5] == "month"):
            time_measure_factor = 30
        elif (time_measures[0:4] == "year"):
            time_measure_factor = 365

        # e.g. last week
        if (hierarchy_number == "last" and number is None):
            counter = 1    
        # e.g last 2 weeks
        elif (hierarchy_number == "last" and number is not None):
            try:
                counter = int(number)
            except:
                counter = w2n.word_to_num(number)
        elif (number is not None):
            try:
                counter = number
            except:
                counter = w2n.word_to_num(number)
        # e.g one month ago (we then check the date one month ago and move 7 days ahead)
        if (hierarchy_number != "last"):

            d_up = datetime.date.today() - datetime.timedelta(days=counter*time_measure_factor) + datetime.timedelta(days = 7)

        else:

            d_up = datetime.date.today() # to switch for interval of time

        d_down = d_up - datetime.timedelta(days=counter*time_measure_factor)

        rows_of_dataset = dataset[dataset.apply(lambda x: row_is_between_dates(x, low_date = d_down, up_date = d_up), axis=1)]

        print(rows_of_dataset)

        returned_response+=f"""
        \n
        Air quality of the last {counter*time_measure_factor} days was like this:

        """

        for column in dataset.columns:
            if column != "date" :
                print(rows_of_dataset[column])
                returned_response += f"""
                - The average value of {column} is {rows_of_dataset[column].mean()}
                """

        return returned_response
    
    
    def _get_energy_consumption(self, interpretation):
        
        collection = self.db.homeiomem
        
        time = None
        
        for entity in interpretation["entities"]:
            if entity["entity"] == "time":
                time = ActionLanguageProcessor._maximumStrSimilarity(entity["value"], ENERGY_CONSUMPTION_ADDRESSES.keys())
        print(time)
        
        if time != None:
            energy_con = collection.find_one({
                    "address":ENERGY_CONSUMPTION_ADDRESSES[time]
            })
        
            return energy_con["value"]
    
if __name__ == "__main__":
    utterance = "what is the energy consumption of last day"
    alp = ActionLanguageProcessor(mongodb_url=MONGODB_URL, model_file=MODEL_ADDR)
    print(alp.analyse_utterance(utterance))
    
    