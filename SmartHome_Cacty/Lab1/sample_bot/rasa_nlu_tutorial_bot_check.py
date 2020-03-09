

import json
import pymongo

myclient = pymongo.MongoClient("mongodb://0.tcp.ngrok.io:15028")
mydb = myclient["shome"]
mycol = mydb["homeio"]


def botCheck():
#    with open('testresponse.json', 'r') as json_file:
    json_file = open('testresponse.json','rt') 
    data = json.load(json_file)
    if (data.get('intent').get('name') == "take_action"):
        if (len(data['entities']) >= 3):
            print("good take action")
            myquery = { "address": 0 }
            newvalues = { "$set": { "state": "true" } }
            mycol.update_one(myquery, newvalues)
        else :
            print("bad get action")