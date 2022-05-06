import sqlite3
from sys import argv
import pandas as pd
from os.path import exists

from requests import delete

choices = "Usable arguments:\n\t-add,remove,show,create"


if "create" == argv[1] and not exists(argv[2]):
    con = sqlite3.connect(argv[2])
    cur = con.cursor()
    con.close()
else:
    if exists(argv[2]):
        con = sqlite3.connect(argv[2])
        cur = con.cursor()
        if "add-table" == argv[1]:
            cur.execute(f'''CREATE TABLE {argv[3]} (Producer text, Stars text,Name text, OriginalLink text, Link text,Account text,Password text)''')

        elif "add" == argv[1]:
            try:
                cur.execute(f"INSERT INTO {argv[3]} VALUES ('{input('Producer:')}','{input('Stars:')}','{input('Name:')}','{input('Original:')}','{input('Link:')}','{input('Account:')}','{input('Password:')}')")
                con.commit()
                con.close()
            except:
                print("usage: pdata add file.db tableName")   
        elif "remove" == argv[1]:
            cur.execute(f"SELECT * FROM '{argv[3]}'")
            rows = cur.fetchall()

            data = {}


            for des in cur.description:
                #print(des[0])
                data.update({des[0]:[]})
            for i in rows:
                #print(i)
                for per in range(len(cur.description)):
                    pass
                    data[list(data.keys())[per]].append(i[per])
            #print(data)
            line = input("line to be deleted:")

            deletedLine = {}
            for num in range(len(rows)):
                deletedLine.update({list(data.keys())[num]:[rows[int(line)][num]]})
                #print(list(data.keys())[num],rows[int(line)][num])
            deletedLine = pd.DataFrame(deletedLine)
            #print(list(data.keys())[0],data[list(data.keys())[0]][int(line)])
            rows = cur.fetchall()
            task = f"DELETE FROM {argv[3]} WHERE {list(data.keys())[0]} = '{data[list(data.keys())[0]][int(line)]}';"
            cur.execute(task)
            con.commit()

            print(f"deleted data\n{deletedLine}")

        elif "show" == argv[1]:
            try:
                cur.execute(f"SELECT * FROM {argv[3]}")
                rows = cur.fetchall()

                data = {}


                for des in cur.description:
                    #print(des[0])
                    data.update({des[0]:[]})
                for i in rows:
                    #print(i)
                    for per in range(len(cur.description)):
                        pass
                        data[list(data.keys())[per]].append(i[per])
                #print(data)
                print(pd.DataFrame(data))
            except:
                print("usage: pdata show file.db tableName")
        con.close()