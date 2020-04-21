a=2100483647
b = ('{:032b}'.format(a))[::-1]  # 转二进制并 高位补零 IO逆序输出
b = list(b)
b.insert(4, '/')
b.insert(9, '/')
b.insert(14, '/')
b.insert(19, '/')
b.insert(24, '/')
b.insert(29, '/')
b.insert(34, '/')
a = ''.join(b)
print(a)