import sys
import time
import clr
import pymongo

clr.AddReference('EngineIO')

from EngineIO import *
from globals import *

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["shome"]
mycol = mydb["homeio"]
memcol = mydb["homeiomem"]


query_1 = {"appliance": {'$regex': '.*Light.*'}}

query_2 ={} 

start = time.time()

def j2kwh(x):
	return round(x * (2.778*(10**(-7))),2)

def k2cel(x):
	return round((x-273.15),2)

while(1):
	data = list(mycol.find(query_1).sort("address"))
	elapsed_time = time.time() - start
	for i in range(len(data)):
		temp = data[i]
		appl = MemoryMap.Instance.GetBit(int(temp['address']), MemoryType.Output)
		if temp['state'] == 'false':
			appl = MemoryMap.Instance.GetBit(int(temp['address']), MemoryType.Output)
			appl.Value = False
			MemoryMap.Instance.Update()
		elif temp['state'] == 'true':
			appl = MemoryMap.Instance.GetBit(int(temp['address']), MemoryType.Output)
			appl.Value = True
			MemoryMap.Instance.Update()
	if elapsed_time > 20:
			start = time.time()
			temp = MemoryMap.Instance.GetFloat(150, MemoryType.Memory)
			var = k2cel(temp.Value)
			print(var)
