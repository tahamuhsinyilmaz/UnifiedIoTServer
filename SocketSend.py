import socket
from Categorization import Categorization
import pyfpgrowth


host = "127.0.0.1"
fpDataPort = 7000
streamDataPort = 7001
transactions = []
subtransaction=[]
count=0
fpDataFile = open("gunlukVeri.txt", "r")
streamDataFile = open("gunlukVeri.txt", "r")
cat = Categorization()

    #Socket for sending FP pattern
fpDataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
fpDataSocket.bind((host, fpDataPort))
fpDataSocket.listen(1)
fpConn, addr = fpDataSocket.accept()


    # FP-Data Categorization
for line in fpDataFile:

    fields = line.split("\"")
    field = fields[1].split(",")
    record = field[0].split(":")

    # 3-Grouping and categorization
    if count < 3:
        if cat.categorize(record[1], record[3]) not in subtransaction:
            subtransaction.append(cat.categorize(record[1], record[3]))
        count += 1
    else:
        if cat.categorize(record[1], record[3]) not in subtransaction:
            subtransaction.append(cat.categorize(record[1], record[3]))
        transactions.append(subtransaction)
        count = 0
        subtransaction = []


    # creating fp-growth and frequency patterns
patterns = pyfpgrowth.find_frequent_patterns(transactions, 20)

    # Sending FP Patterns
for keys in patterns:
    if len(keys)>=2:
        x=str(keys)+";"
        print(x)
        fpConn.send(x.encode('utf-8'))


#Closing fpPattern files and connections
fpDataFile.close()
fpConn.close()

#Socket for sending stream data
streamDataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
streamDataSocket.bind((host, streamDataPort))
streamDataSocket.listen(1)
streamConn, addr2 = streamDataSocket.accept()

    # Sending real stream data
for line in streamDataFile:

    fields = line.split("\"")
    field = fields[1].split(",")
    record = field[0].split(":")
    print(cat.categorize(record[1], record[3]))
    streamConn.send(cat.categorize(record[1], record[3]).encode('utf-8'))


# Closing stream files and connections
streamDataFile.close()
streamConn.close()

