import sys
import time
import clr

clr.AddReference('EngineIO')

from EngineIO import *

livingRoomLight = MemoryMap.Instance.GetBit(0, MemoryType.Output)

A_Lights            = MemoryMap.Instance.GetBit(0, MemoryType.Output)
B_Lights_1          = MemoryMap.Instance.GetBit(19, MemoryType.Output)
B_Lights_2          = MemoryMap.Instance.GetBit(20, MemoryType.Output)
C_Lights            = MemoryMap.Instance.GetBit(30, MemoryType.Output)
D_Lights_1          = MemoryMap.Instance.GetBit(40, MemoryType.Output)
D_Lights_2          = MemoryMap.Instance.GetBit(41, MemoryType.Output)
E_Lights            = MemoryMap.Instance.GetBit(54, MemoryType.Output)
F_Lights_1          = MemoryMap.Instance.GetBit(68, MemoryType.Output)
F_Lights_2          = MemoryMap.Instance.GetBit(69, MemoryType.Output)
G_Lights            = MemoryMap.Instance.GetBit(83, MemoryType.Output)
H_Lights            = MemoryMap.Instance.GetBit(97, MemoryType.Output)
I_Lights_1          = MemoryMap.Instance.GetBit(110, MemoryType.Output)
I_Lights_2          = MemoryMap.Instance.GetBit(111, MemoryType.Output)
J_Lights            = MemoryMap.Instance.GetBit(122, MemoryType.Output)
K_Lights            = MemoryMap.Instance.GetBit(135, MemoryType.Output)
L_Lights            = MemoryMap.Instance.GetBit(146, MemoryType.Output)
M_Lights            = MemoryMap.Instance.GetBit(159, MemoryType.Output)
N_Lights_1          = MemoryMap.Instance.GetBit(172, MemoryType.Output)
N_Lights_2          = MemoryMap.Instance.GetBit(173, MemoryType.Output)
N_Lights_3          = MemoryMap.Instance.GetBit(174, MemoryType.Output)
O_Lights_Porch_1    = MemoryMap.Instance.GetBit(187, MemoryType.Output)
O_Lights_Porch_2    = MemoryMap.Instance.GetBit(188, MemoryType.Output)
O_Lights_Pool_      = MemoryMap.Instance.GetBit(189, MemoryType.Output)
O_Lights_Garden     = MemoryMap.Instance.GetBit(190, MemoryType.Output)
O_Lights_Entrance   = MemoryMap.Instance.GetBit(191, MemoryType.Output)
