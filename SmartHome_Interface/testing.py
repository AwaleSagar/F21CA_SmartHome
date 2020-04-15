# import psutil
# import clr
import pymongo

# clr.AddReference('EngineIO')

# from EngineIO import *
# from globals import *

# myclient = pymongo.MongoClient("mongodb://f21ca:heriot123@18.219.152.221:27017/")
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["shome"]
mycol = mydb["homeio"]
mycolvar = mydb["homeiovari"]
memcol = mydb["homeiomem"]


data = list(mycol.find().sort('address'))

print(data[0])