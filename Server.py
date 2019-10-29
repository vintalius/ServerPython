#!/usr/bin/env python3

import sqlite3
import socket

def server():
    HOST = ''  # Standard loopback interface address (localhost)
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))

        while True:
            s.listen()
            conn, addr = s.accept()


            print('Connected by', addr)
            succsses = " OK!"
            succssesByte = succsses.encode()


            data = conn.recv(1024)
            ReadData = data.decode("utf-8")
            listOfTheData = ReadData.split(",")

            #Cheak with the Data base
            Db_value_Name = askDatabaseName(listOfTheData)
            if (Db_value_Name == []):
                conn.send("1".encode())
            else:
                Db_value_Door = askDataBaseDoor(listOfTheData)
                if (Db_value_Door == []):
                    conn.send("2".encode())
                else:
                    conn.send("0".encode())
            conn.close()







def askDatabaseName(listOfTheData):
    global DB_cursor
    print(listOfTheData[1])
    DB_cursor.execute("SELECT  ID, signature FROM Permission WHERE Name =:name", {'name': str(listOfTheData[1])})
    return DB_cursor.fetchall()

def askDataBaseDoor(listOfTheData):
    global DB_cursor
    print(listOfTheData[2] + " door")
    DB_cursor.execute("SELECT  ID, Dor_Name FROM DORS WHERE Dor_Num =:Dor_Num", {'Dor_Num': int(listOfTheData[2])})
    dbc =DB_cursor.fetchall()
    print(dbc, " the list")
    return dbc







if __name__ == "__main__":
    connDB = sqlite3.connect('dbSecurity.db')
    DB_cursor = connDB.cursor()
    server()

