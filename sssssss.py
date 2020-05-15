# tag_list=['1','2','3','4','5']
tag_list=['1','2','3','4','5','6','7','8','9','10','11','12']

l = len(tag_list)  # 变量表长度，如果大于10 必须分批读取保证不报错
x,y=divmod(l,10) # Python内置函数返回 整除和余数
# x = l // 10  # 取整
# y = l % 10  # 取余数
# x=x+1
if x==0:x=1
# print(x,y)
# for i in range(1):
#     print(i)
a = 0  # 每一组变量的上标
val = []  # 初始化列表 每一组变量值
for n in range(x):
    # print(n)
    # print(n,(range(x+1)))
    if n < x:
        val=val+(tag_list[10 * a:10 * (a + 1)])
        a += 1
        n += 1
    if n == x and y != 0:
        val=val+(tag_list[10 * a:10 * a + y])
vall = val
print(vall)