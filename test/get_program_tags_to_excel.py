'''
the following import is only necessary because eip.py is not in this directory
'''
import sys
sys.path.append('..')

'''
Get tag list from specific program

In this case, I had a program named MiscHMI,
this retrives the program scoped tags from
just that program

NOTE: This actually reads all of the tags from the
PLC, it returns only the list of tags from the
program you specified.
'''
from pylogix import PLC

with PLC() as comm:
    comm.IPAddress = '192.168.100.200'
    tags = comm.GetModuleProperties(slot=3)
    aa=comm.GetDeviceProperties()
    # print(aa)
    print(tags.TagName)
    print(tags.Value)
    print(tags.Status)
    # for t in tags.Value:
    #     print(t.TagName, t.DataType)

