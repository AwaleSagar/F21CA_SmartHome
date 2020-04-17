# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 15:18:46 2020

@author: dacca
"""
# LIB IMPORTS
# import tensorflow as tf
import datetime
import requests
import pandas as pd
from pprint import pprint
import os
import numpy as np

from rasa.nlu.model import Interpreter

# OWN FILES IMPORTS
from useful_functions import get_date_from_interpretation, two_arrays_random_permutation, get_air_quality_message
from constants import *


from calendarEvents.setting_google_api import service
from calendarEvents.read_events import get_next_event, get_all_day_events, get_last_event

### TEMPORARY TO TEST BEFORE PLUGING TO DATABASE
from rasa.nlu.model import Interpreter

# run 'pip install pymongo' to install this lib
from pymongo import MongoClient
import random

class ActionLanguageProcessor():
    
    
    def __init__(self, mongodb_url, model_file):
        self.DB_CLIENT = MongoClient(mongodb_url)
        #self.DB_CLIENT = MongoClient(mongodb_url, serverSelectionTimeoutMS=100)

        # I created a database called simple_appliances_db
        self.db = self.DB_CLIENT.shome
        # loading the model from one directory or zip file
        self.interpreter = Interpreter.load(model_file)
        self.welcome = ["Hello, nice to meet you! How can I help you?","Nice to meet you!","Welcome to Alana Eco bot application. Can I help you?","Hi! How are you?","Welcome to Alana app.","Hi, How can I help you?"]
        self.affirm = ["Nice !","Okay !","Good !"]
        self.deny = ["Ok", "No worries"]
        self.nicetomeeyou = ["Me too!", "I am happy to help you.","Feel free to ask for anyy help!"]
        self.react_positive = ["Hahahaha","Thats funny!","Thanks!","I am happy to help you."]
        self.thanking = ["You are welcome","I am happy to help you."] 
        self.goodbye = ["Bye bye!","See you soon","Take care","Good bye","See you tomorrow"] 
        self.sos = ["I am sending you the rescue (... ... not really)","The rescue have been informed (... ... not really)"] 

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
        # print(mongodb_url)
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

    def analyse_utterance(self, utterance="hello"):
        # parsing the utterance
        interpretation = self.interpreter.parse(utterance)

        # url = "http://18.219.152.221:5005/model/parse"
        # payload = "{\"text\":" + "\"{}\"".format(utterance) +"}"
        # r = requests.request("POST", url, data = payload)
        # interpretation = r.json()
        
        #pprint(interpretation)
        
        if interpretation["intent"]['name'] == "take_action":
            return self._take_action(interpretation)
        elif interpretation["intent"]['name'] == "action_variable":
             return self._take_action(interpretation)
        elif interpretation["intent"]['name'] == "take_action_variable":
            return self._take_action(interpretation)        
        elif interpretation["intent"]['name'] == "get_info":
            return self._eco_friendly_fact(interpretation)
        elif interpretation["intent"]["name"] == "air_quality_today":
            return self._get_today_air_quality(interpretation)
        elif interpretation["intent"]["name"] == "air_quality_historical":
            return self._get_historical_air_quality(interpretation)
        elif interpretation["intent"]["name"] == "get_info_energy":
            return self._get_energy_consumption_timespan(interpretation)
        elif interpretation["intent"]["name"] == "energy_consumption_report":
            return self._get_energy_consumption_report(interpretation)
        elif (interpretation["intent"]["name"] == "greet"):
            return self._greet_(interpretation)
        elif (interpretation["intent"]["name"] == "deny"):
            return self._deny_(interpretation)
        elif (interpretation["intent"]["name"] == "affirm"):
            return self._affirm_(interpretation)
        elif (interpretation["intent"]["name"] == "nicetomeeyou"):
            return self._nicetomeeyou_(interpretation)        
        elif (interpretation["intent"]["name"] == "react_positive"):
            return self._react_positive_(interpretation)  
        elif (interpretation["intent"]["name"] == "thanking"):
            return self._thanking_(interpretation)  
        elif (interpretation["intent"]["name"] == "goodbye"):
            return self._goodbye_(interpretation)  
        elif (interpretation["intent"]["name"] == "sos"):
            return self._sos_(interpretation)
        elif (interpretation["intent"]["name"] == "next_event"):
            return self._get_next_event(interpretation)
        elif (interpretation["intent"]["name"] == "first_last_event"):
            return self._get_first_last_event(interpretation)
        elif (interpretation["intent"]["name"] == "day_events"):
            return self._get_day_events(interpretation)
        else:
            return self._greet_(interpretation)
            
        
        

    def _greet_(self, interpretation):     
        return random.choice(self.welcome)
    def _affirm_(self, interpretation):
        return random.choice(self.affirm)
    def _deny_(self, interpretation):
        return random.choice(self.deny)
    def _nicetomeeyou_(self, interpretation):
        return random.choice(self.nicetomeeyou)
    def _react_positive_(self, interpretation):
        return random.choice(self.react_positive)
    def _thanking_(self, interpretation):
        return random.choice(self.thanking)
    def _goodbye_(self, interpretation):
        return random.choice(self.goodbye)
    def _sos_(self, interpretation):
        return random.choice(self.sos)


    #calendar related intents
    def _get_next_event(self, interpretation):
        now = datetime.datetime.now()
        time = None
        if len(interpretation["entities"]) > 0:
            for entity in interpretation["entities"]:
                if entity["entity"] == "time":
                    time = entity["value"]
        if time == "today":
            return get_next_event(service, now, 1)
        elif time == "tomorrow":
            return get_next_event(service, now, 2)
        else:
            return get_next_event(service, now)
    def _get_first_last_event(self, interpretation):
        now = datetime.datetime.now()
        time = None
        rank = None
        if len(interpretation["entities"]) > 0:
            for entity in interpretation["entities"]:
                if entity["entity"] == "time":
                    time = entity["value"]
                if entity["entity"] == "rank":
                    rank = entity["value"]
        if rank == "first":
            if time == "today" or time is None:
                return get_next_event(service, now, 1)
            elif time == "tomorrow":
                return get_next_event(service, now, 2)
            else:
                return "Time not defined."
        elif rank == "last":
            if time == "today" or time is None:
                return get_last_event(service, now, True)
            elif time == "tomorrow":
                return  get_last_event(service, now, False)
            else:
                return "Time not defined."
        else:
            return "Rank not defined."
    def _get_day_events(self, interpretation):
        now = datetime.datetime.now()
        time = None
        if len(interpretation["entities"]) > 0:
            for entity in interpretation["entities"]:
                if entity["entity"] == "time":
                    time = entity["value"]
        if time == "tomorrow":
            return get_all_day_events(service, now, False)
        else:
            return get_all_day_events(service, now, True)


    #not done
    def _take_action_duration_(self, interpretation):
        return "Not implemented yet 1"
    def _take_action_variable_(self, interpretation):
        return "Not implemented yet 2"
    def _inform_(self, interpretation):
        return "Not implemented yet 3"
    def _repair_inform_(self, interpretation):
        return "Not implemented yet 4"
    def _air_quality_forecast_(self, interpretation):
        return "Not implemented yet 5"



        
    def _eco_friendly_fact(self, interpretation):
        collection = self.db.homeiofact

        #answer = collection.aggregate([{ "$sample": { "size": 1 } }])
        for entity in interpretation['entities'] :
            if entity['entity'] == "appliance" :
                appliance = entity['value']
                try:
                    answer = collection.aggregate([{ "$match": { "Things": appliance } },{ "$sample": { "size": 1 } }])
                    fact = [tmp for tmp in answer][0]
                    return fact['Fact'] 
                except:
                    answer = collection.aggregate([{ "$match": { "Fact Category": "eco" } },{ "$sample": { "size": 1 } }])
                    fact = [tmp for tmp in answer][0]
                    return fact['Fact'] 
        
            
        answer = collection.aggregate([{ "$match": { "Fact Category": "eco" } },{ "$sample": { "size": 1 } }])
        fact = [tmp for tmp in answer][0]
        return fact['Fact']
        #answer.parse()
        

        
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
            and action.lower() in self.action_device_mapping[appliance]["actions"]): # We check the location exists
                #CODE FOR DB QUERY
                collection = self.action_device_mapping[appliance.lower()]["collection"] 

                #list_of_devices = collection.find()
                
                
                list_of_devices = collection.find({
                        "zone": LOCATION_TO_ZONE[location.lower()],#Everything that matches this zone requirements ,
                        "appliance": {'$regex':f'^{ENTITY_TO_DATABASE_NAME[appliance]}', "$options":"-i"}
                })
                
                """
                list_of_devices = collection.find({
                        "zone": LOCATION_TO_ZONE[location.lower()],#Everything that matches this zone requirements ,
                        "appliance": {'$regex':f'^{ENTITY_TO_DATABASE_NAME[appliance]}$'}
                })
                
                """


                #print(list_of_devices)
                for device in list_of_devices:
                    
                    # print("--------------------")
                    # print(device)
                    # print("--------------------")
                    
                    collection.update({
                            "address": device["address"]#The device that matches this address
                            },{
                                "$set": {"state": ACTION_TO_DB_VALUE_MAPPING[action.lower()](device["state"]) }
                            })
                
                location = LOCATION_TO_NAME[location]

                return f"Yes ! I {action} the {appliance} in {location}"
            
            #If incorrect, leaves the if and returns error NLG message
            
        # IN CASE OF WRONGLY SYNTAXED QUERIES
        return "Sorry, I did not understand, could you repeat ?"

    def _get_today_air_quality(self, interpretation):
        r = requests.get(url=API_URL)
        response = r.json()
        #print(interpretation)

        # RETRIEVING THE GASES LEVELS AND CREATING INFORMATION LEVELS
        ## OZONE
        try:
            ozone_val = response['data']['iaqi']['o3']['v']
            ozone_level, ozone_msg = get_air_quality_message(OZONE_DESC, ozone_val)
        except:
            ozone_msg = "the measure is unavailable"

        ## CARBON MONOXIDE
        try:
            carbon_monoxide_val = response['data']['iaqi']['co']['v']
            carbon_monoxide_level, carbon_monoxide_msg = get_air_quality_message(CARBON_MONOXIDE_DESC, carbon_monoxide_val)
        except:
            carbon_monoxide_msg = "the measure is unavailable"

        ## NITROGEN DIOXIDE
        try:
            nitrogen_dioxide_val = response['data']['iaqi']['no2']['v']
            nitrogen_dioxide_level, nitrogen_dioxide_msg = get_air_quality_message(NITROGEN_DIOXIDE_DESC, nitrogen_dioxide_val)
        except:
            nitrogen_dioxide_msg = "the measure is unavailable"
        

        gases = ["ozone","carbon monoxide", "nitrogen dioxide"]
        sentences = [ozone_msg, carbon_monoxide_msg, nitrogen_dioxide_msg]
        terms = ["For the ", "Concerning the ", "Finally, the "]# terms used to write the sentences

        gases, sentences = two_arrays_random_permutation(gases, sentences)

        final_msg = f"""
            For the {gases[0]} concentration, {sentences[0]}.
            Concerning the {gases[1]} concentration, {sentences[1]}.
            Finally, for the {gases[2]} concentration, {sentences[2]}.
            """

        return final_msg
        
    def _get_historical_air_quality(self, interpretation):
        """
        Gives back information of air quality other a provided time measures
        """
                
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

        d_down, d_up, day_count = get_date_from_interpretation(interpretation)

        rows_of_dataset = AIR_QUALITY_DATASET[AIR_QUALITY_DATASET.apply(lambda x: row_is_between_dates(x, low_date = d_down, up_date = d_up), axis=1)]

        mean_carbon_monoxide = round(rows_of_dataset[" co"].mean(), 1)
        mean_ozone = round(rows_of_dataset[" o3"].mean(), 1)
        mean_nitrogen_dioxide = round(rows_of_dataset[" no2"].mean(), 1)

        carbon_monoxide_level, _ = get_air_quality_message(CARBON_MONOXIDE_DESC, mean_carbon_monoxide)
        ozone_level, _ = get_air_quality_message(OZONE_DESC, mean_ozone)
        nitrogen_dioxide_level, _ = get_air_quality_message(NITROGEN_DIOXIDE_DESC, mean_nitrogen_dioxide)

        carbon_monoxide_level = LEVELS[carbon_monoxide_level].lower()
        ozone_level = LEVELS[ozone_level].lower()
        nitrogen_dioxide_level = LEVELS[nitrogen_dioxide_level].lower()

        if (carbon_monoxide_level == ozone_level and carbon_monoxide_level == nitrogen_dioxide_level):
        
            returned_response+=f"""
            Over the last {day_count} days, the average concentration of carbon monoxide, 
            ozone and nitrogen dioxide were all {ozone_level}.
            """

        else:

            returned_response+=f"""
            Over the last {day_count} days, the average concentration of carbon monoxide was {carbon_monoxide_level}, 
            while the concentration of ozone and nitrogn dixodie were mutually {ozone_level} and {nitrogen_dioxide_level}.
            """

        return returned_response
    
    def _get_energy_consumption_report(self, interpretation):
        """
            Retrieves statistics, as a report, for the total energy consumption in a specific time span
        """         

        appliance = None

        for entity in interpretation["entities"]:
            if entity["entity"] == "appliance":
                appliance = entity["value"]

        d_down, d_up, day_count = get_date_from_interpretation(interpretation)     
        plural = "s" if day_count > 1 else ""

        timestamps = TIMESTAMPS_DATASET["Timestamps"].to_numpy()

        df = CONSUMPTION_DATASET.copy()

        print(df.head())

        #Finds the timestamp between the limit dates when querying past consumption
        timestamps_conditioned = np.array( #converts timestamps in booleans if 
            [
                datetime.datetime.fromtimestamp(timestamp).date() >= d_down and datetime.datetime.fromtimestamp(timestamp).date() <= d_up for timestamp in timestamps
            ]
        )
        #sum is the sum of consumption over the asked period of time
        df["sum"] = df["values"].apply(lambda x: np.sum(np.extract(timestamps_conditioned, x)))

        max_light = df.iloc[df[df["appliance"].str.contains('light',case=False)]["sum"].idxmax()]
        max_heating = df.iloc[df[df["appliance"].str.contains('heat',case=False)]["sum"].idxmax()]

        collection = self.db.homeiovari

        light_room = collection.find_one({
                        "address": int(max_light["address"])
                })

        heating_room = collection.find_one({
                        "address": int(max_heating["address"])
                })

        light_room = ZONE_TO_LOCATION[light_room["zone"]]
        heating_room = ZONE_TO_LOCATION[heating_room["zone"]]

        return f"""
            Over {day_count} day{plural}, the most heated room was the {heating_room} while the room with the lights turned on for the longest time was the {light_room}.
            
        """


    def _get_energy_consumption_timespan(self, interpretation):
        """
            Retrieves statistics about the energy consumption in a specific time span
        """         

        appliance = None

        for entity in interpretation["entities"]:
            if entity["entity"] == "appliance":
                appliance = entity["value"]

        d_down, d_up, day_count = get_date_from_interpretation(interpretation)     
        plural = "s" if day_count > 1 else ""

        timestamps = TIMESTAMPS_DATASET["Timestamps"].to_numpy()

        if (appliance == None):
            #When no appliance is queried and a general house-wise energy consumption report is asked        
            arrs = CONSUMPTION_DATASET["values"].to_numpy()
            subject = "You"
    
        elif (appliance.lower()[:6] == "light"):
            # We retrieve multiple set of registered values as an array of array: [
            #   [values of light 1], [values of light 2] ...
            # ]
            arrs = CONSUMPTION_DATASET[CONSUMPTION_DATASET["appliance"].str.contains('light',case=False)]["values"].to_numpy()
            subject = "Your lights"

        elif (appliance.lower()[:4] == "heat"):
            arrs = CONSUMPTION_DATASET[CONSUMPTION_DATASET["appliance"].str.contains('heat',case=False)]["values"].to_numpy()       
            subject = "Your heaters"
            
        else:
            return f"Query misunderstood, please repeat"


        #Finds the timestamp between the limit dates when querying past consumption
        timestamps_conditioned = np.array( #converts timestamps in booleans if 
            [
                datetime.datetime.fromtimestamp(timestamp).date() >= d_down and datetime.datetime.fromtimestamp(timestamp).date() <= d_up for timestamp in timestamps
            ]
        )

        selected_timestamps = np.extract(timestamps_conditioned, timestamps)

        consumption_per_hour = {}

        total = 0
        for arr in arrs:
            extracted_cons = np.extract(timestamps_conditioned,arr)
            #for total
            total += np.sum(extracted_cons)
            #for a per-hour basis
            for idx, cons in enumerate(extracted_cons):
                timestamp = selected_timestamps[idx]
                hour_of_timestamp = datetime.datetime.fromtimestamp(timestamp).hour

                if hour_of_timestamp in consumption_per_hour.keys():
                    consumption_per_hour[hour_of_timestamp] += cons
                else:
                    consumption_per_hour[hour_of_timestamp] = cons

        most_cons_hour = max(consumption_per_hour, key=consumption_per_hour.get)
        cons_of_most_cons_hour = consumption_per_hour[most_cons_hour]

        mean_hour_cons = 0

        for hour in consumption_per_hour.keys():
            mean_hour_cons += consumption_per_hour[hour]

        mean_hour_cons /= len(consumption_per_hour.keys())

        excess = round((cons_of_most_cons_hour/mean_hour_cons) * 100 - 100, 1)

        return f"""
            {subject} consumed a total of {round(total, ndigits=2)} Watt hour over {day_count} day{plural}. 
            You consumed the most energy at {most_cons_hour} o'clock, with {cons_of_most_cons_hour:.2f} Watt hour which is {excess}% more that the average hourly consumption over this period.
            """

if __name__ == "__main__":
    #utterance = "turn on the ligh+t in the kitchen"

    # utterance = "turn on the light in living room"
    # utterance = "give me an eco fact about the heating"

    #utterance = "How good is the air right now?"

    # utterance = "what is my energy consumption report of the last three years"
    #utterance = "can you give me air quality of last week ?"

    # utterance = "what is my consumption these last two weeks"
    # utterance = "can you give me air quality of last week ?"
    # utterance = "turn off the living room light"
    # utterance = "what is my energy consumption last week"
    # utterance = "can you give me air quality of last week ?"
    # utterance = "turn off the living room light"
    # utterance = "what's my next event?"
    # utterance = "what's my agenda for today?"
    # utterance = "what's my last event tomorrow?"

    utterance = "Can you give me my energy consumption report ?"

    alp = ActionLanguageProcessor(mongodb_url=MONGODB_URL, model_file=MODEL_ADDR)
    print(alp.analyse_utterance(utterance))
    
    
