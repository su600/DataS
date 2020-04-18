from pylogix import PLC
import time
with PLC() as plc:
    plc.IPAddress="192.168.200.1"
    # a=plc.GetDeviceProperties()
    # b=plc.GetModuleProperties("1")
    while 1:
        try:
            c=plc.GetPLCTime()
            print(c.Status)
            time.sleep(3)
        except Exception as c:
            print(c)
        else:
            pass
