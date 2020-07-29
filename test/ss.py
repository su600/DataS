variable="Q 2.0"
data=True
variable2=[]
variable2.append(variable)
data2=[]
data2.append(data)
print(variable2)
print(data2)

cc=dict(zip(variable2,data2))
print(cc)
print("")
# 测试IO地址
address="7.12"

address2=float(address)
b = int(address2)
c = int(address2*10 - b* 10)
print(b,c)

address2=float(address)
# print(address2)
b = int(address2)
c = ((address2 - b)* 10)
print(b,c)

address2=str(address)
b = int(address2.split(".")[0])
c = int(address2.split(".")[1])
print(b,c)