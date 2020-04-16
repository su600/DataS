from pylogix import PLC
import time
with PLC() as plc:
    plc.IPAddress="192.168.100.200"
    # a=plc.GetDeviceProperties()
    # b=plc.GetModuleProperties("1")
    while 1:
        try:
            c=plc.GetPLCTime()
            print(c)
            time.sleep(1)
        except Exception as c:
            print(c)
        else:
            pass
