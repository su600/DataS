import socket


s = socket.socket()
print("Scoekt successfully created")

port = 54321
s.bind(('', port))
print("socket binded to %s" % (port))

s.listen(5)
print("socket is listening")

while True:
    c, addr = s.accept()
    
    print()
    print("Got connection from", addr)

    print("s: ", s)
    print("c: ", c)
    print("addr: ", addr)

    c.send("Thank you for connecting".encode())

    c.close()