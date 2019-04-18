import socket


host = "127.0.0.1"
port = 7000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(1)
conn,addr = s.accept()

file = open("veriler2.txt", "r")

for line in file:
    print(line)
    conn.send(line.encode('utf-8'))

file.close()
conn.close()