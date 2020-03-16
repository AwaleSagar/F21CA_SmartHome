import sys
import time
import psutil
import clr
import pymongo

clr.AddReference('EngineIO')

from EngineIO import *
from globals import *

# myclient = pymongo.MongoClient("mongodb://0.tcp.ngrok.io:16959")
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["shome"]
mycol = mydb["homeio"]
mycolvar = mydb["homeiovari"]
memcol = mydb["homeiomem"]


# query_1 = {"appliance": {'$regex': '.*Light.*'}}


start = time.time()

def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def getmemval(x):
	temp = MemoryMap.Instance.GetFloat(int(x), MemoryType.Memory)
	return temp.Value

def j2kwh(x):
	return round(x * (2.778*(10**(-7))),2)

def k2cel(x):
	return round((x-273.15),2)

while(1):
	# process = "notepad++.exe"
	# print(checkIfProcessRunning(process))
	data = list(mycol.find().sort("address"))
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
	datavar = list(mycolvar.find().sort("address"))
	for i in range(len(datavar)):
		temp = datavar[i]
		appl = MemoryMap.Instance.GetFloat(int(temp['address']), MemoryType.Output)
		appl.Value = temp['value']
		MemoryMap.Instance.Update()
		# print(temp['value'])
		# time.sleep(1)
	if elapsed_time > 10:
			start = time.time()
			for x in memoryAdd:
				if x[1] == 0:
					tem = getmemval(x[0])
					query = { "address": x[0] }
					newvalues = { "$set": { "value": tem } }
					memcol.update_one(query, newvalues)
					# print(tem)
				elif x[1] == 1:
					tem = getmemval(x[0])
					temc = j2kwh(tem)
					query = { "address": x[0] }
					newvalues = { "$set": { "value": temc } }
					memcol.update_one(query, newvalues)
					# print(temc)
				elif x[1] == 2:
					tem = getmemval(x[0])
					temc = k2cel(tem)
					query = { "address": x[0] }
					newvalues = { "$set": { "value": temc } }
					memcol.update_one(query, newvalues)
					# print(temc)