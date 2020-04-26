from pylogix import *
# todo 可以通过扫描所有模块属性，生成IO变量表
# 但是扫描不出来变量表中所显示的TagType

with PLC() as comm:
    print('请输入设备IP')
    comm.IPAddress = input()
    print(f'IP地址为 {comm.IPAddress} 的设备模块如下：')
    i=0
    while 1:
        module = comm.GetModuleProperties(slot=i)
        if module.Status=='Success':
            print(f'slot:{i} {module.Value.Device} - {module.Value.ProductName}')
        else:
            break
        i+=1
