'''
和前一个值比较 f和时刻相关 每次运行结果都不同
'''
import random

def f():
    a=list(range(5))
    b=["a","b","c","d","d"]
    for i in range(5):
        pass
        a[i] = random.randint(1, 10)
    a=dict(zip(b,a))
    # print(a)
    return a

def rr():
    result = random.sample(range(1, 20), 10)
    # print(result)
    return result

# a0={'a': 0, 'b': 0, 'c': 0, 'd': 0}
a0=[0,0,0,0,0,0,0,0,0,0]

for n in range(5):
    # t1=f()
    # s=t1-a
    t1=rr()
    # print(t1)
    print(a0,t1)
    t1=set(t1)
    a0=set(a0)
    cc=t1-a0
    print("更新的数据",cc)
    # if s!=0:
    #     print("不等于 就写入数据库",a0,t1)
    # else:
    #     print("等于，不写入",a0,t1)
    a0=t1
