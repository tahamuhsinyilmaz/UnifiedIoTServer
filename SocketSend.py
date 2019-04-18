import socket
import json
import pickle

host = "127.0.0.1"
port = 7000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(1)
conn,addr = s.accept()

file = open("gün.txt", "r")
#file2 = open("veriler.json","r")
#jsonObj = json.load(file2)

# Repeat for each song in the text file
for line in file:
    # Let's split the line into an array called "fields" using the ";" as a separator:
    fields = line.split("\t")
    records = fields[1][1:len(fields[1])-1]
    record = records.split(":")
    print(record[1]+record[2])


file.close()
conn.close()