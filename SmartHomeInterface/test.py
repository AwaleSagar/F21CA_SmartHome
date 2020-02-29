import sys
import time
import clr

clr.AddReference('EngineIO')

from EngineIO import *



livingRoomLight = MemoryMap.Instance.GetFloat(56, MemoryType.Output)


print(dir(MemoryMap))



# for i in range(10):
# 	livingRoomLight.Value = i
# 	time.sleep(2)

# 	# When using a memory value before calling the Update method we are using a cached value.
# 	print("Light is on? " + str(livingRoomLight.Value))

# 	# Calling the Update method will write the livingRoomLight.Value to the memory map.
# 	MemoryMap.Instance.Update()
	
# 	time.sleep(1)

# # When we no longer need the MemoryMap we should call the Dispose method to release all the allocated resources.
# MemoryMap.Instance.Dispose()