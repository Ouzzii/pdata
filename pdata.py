import sqlite3
import struct
from sys import argv
import pandas as pd
from os.path import exists
from string import digits


choices = "Usable arguments:\n\t-add,remove,show,create"

print(argv)

def Create(name):
    con = sqlite3.connect(name)
    cur = con.cursor()
    con.close()

def AddTable(TableName):
    try:
        print(con)
        print("for exit: exit-to-add")
        values = []
        for i in range(101):
            value = input(f"{i}. value:")
            if value.lower() == "exit-to-add":
                break
            values.append([value])
        print("TEXT-blob-integer-real-numeric")
        for i in values:
            type = input(f"{i[0]} type:")
            if type in ["TEXT","blob","integer","real","numeric"]:
                i.append(type)
            else:
                print("Please choose a correct type")
                break
        structure = []
        for i in values:
            print(" ".join(i))
            structure.append(" ".join(i))
        structure = ",".join(structure)
        cur.execute(f'''CREATE TABLE {TableName} ({structure})''')
    except sqlite3.OperationalError:
        print("Table already exists")
    except KeyboardInterrupt:
        print("\nthe program has been closed")
def Add(file):
    try:
        cur.execute(f"SELECT * FROM {file}")
        data = []
        for values in(cur.description):
            value = input(f"insert value for {values[0]}:")
            data.append(f"'{value}'")
        cur.execute(f"INSERT INTO {argv[3]} VALUES ({','.join(data)})")
        con.commit()
        con.close()
    except KeyboardInterrupt:
        print("\nthe program has been closed")
    except IndexError:
        print("usage: pdata add file tableName")

def Delete(table):
    try:
        cur.execute(f"SELECT * FROM '{table}'")
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
        for num in range(len(list(data.keys()))):
            deletedLine.update({list(data.keys())[num]:[rows[int(line)][num]]})
            #print(list(data.keys())[num],rows[int(line)][num])
        deletedLine = pd.DataFrame(deletedLine)
        #print(list(data.keys())[0],data[list(data.keys())[0]][int(line)])
        rows = cur.fetchall()
        task = f"DELETE FROM {table} WHERE {list(data.keys())[0]} = '{data[list(data.keys())[0]][int(line)]}';"
        cur.execute(task)
        con.commit()

        print(f"deleted data\n{deletedLine}")
    except KeyboardInterrupt:
        print("\nthe program has been closed")

def ShowAll(table):
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()

    data = {}


    for des in cur.description:
        #print(des[0])
        data.update({des[0]:[]})
    for i in rows:                    #print(i)
        for per in range(len(cur.description)):
            pass
            data[list(data.keys())[per]].append(i[per])
    #print(data)
    print(pd.DataFrame(data))
def ShowIndex(table,Index):
    cur.execute(f"SELECT {Index} FROM {table}")
    rows = cur.fetchall()

    data = {}


    for des in cur.description:
        #print(des[0])
        data.update({des[0]:[]})
    for i in rows:                    #print(i)
        for per in range(len(cur.description)):
            pass
            data[list(data.keys())[per]].append(i[per])
    #print(data)
    print(pd.DataFrame(data))
def Update(table):
    try:
        cur.execute(f"SELECT * FROM {table}")
        keys = []
        structure = []
        line = int(input("Line to change:"))

        for key in cur.description:
            keys.append(key[0])

        all = cur.fetchall()
        print(all[line])

        print("!!!If you don't want to change just press enter")
        for num in range(len(keys)):
            value = input(f"insert new value for {keys[num]} (default:{all[line][num]}):")
            if value == "":
                structure.append(str(all[line][num]))
            else:
                structure.append(value)
        
        newRow = []
        oldRow = []
        for num in range(len(keys)):
            #print(keys[num],structure[num])
            if not structure[num] in digits:
                newRow.append(f"{keys[num]} = '{structure[num]}'")
            elif structure[num] in digits:
                newRow.append(f"{keys[num]} = {structure[num]}")
            oldRow.append(f"{keys[num]} = '{list(all[line])[num]}'")
        cur.execute(f"Update {table} set {','.join(newRow)} where {' AND '.join(oldRow)}")
        con.commit()
    except KeyboardInterrupt:
        print("\nthe program has been closed")


def Info(table):
    cur.execute(f"SELECT * FROM *")
    print(cur.description)



if "help" == argv[1].lower() or len(argv) < 3:
    info = "options:\n\tcreate -- Create a new data file (with extension)\n\tadd-table -- Create a new table in the data file\n\tadd -- Add a new value to the data table\n\tremove -- Remove a specific row from the data table\n\tshow -- Print the entire data table\n\tupdate -- Modify a specific row from the data table\n\nusage: pdata option file tableName"
    print(info)

elif "create" == argv[1].lower() and not exists(argv[2]):
    if argv[2] == "":
        print("Please enter a valid filename")
    else:
        Create(argv[2])

elif "create" == argv[1].lower() and exists(argv[2]):
    print(f"{argv[2]} already exists")
else:
    if exists(argv[2]):
        con = sqlite3.connect(argv[2])
        cur = con.cursor()
        if "add-table" == argv[1].lower():
            try:
                AddTable(argv[3])
            except IndexError:
                print("usage: pdata add-table file.db tableName")
        elif "add" == argv[1].lower():
            try:
                Add(argv[3])
            except IndexError:
                print("usage: pdata add file.db tableName")
        elif "remove" == argv[1].lower():
            try:
               Delete(argv[3])
            except IndexError:
                print("usage: pdata remove file.db tableName")
        elif "show" == argv[1].lower():
            #try:
            if len(argv) == 4:
                ShowAll(argv[3])
            elif len(argv) == 5:
                print("Use , to select multiple indexes")
                ShowIndex(argv[3],argv[4])
            else:
                #except IndexError:
                print("usage: pdata show file.db tableName\n\t\tos\nusage: pdata show file.db tableName Index")
        elif "update"== argv[1].lower():
            try:
                Update(argv[3])
            except IndexError:
                print("usage: pdata update file.db tableName")
        elif "info" == argv[1].lower():
            Info(argv[2])
        con.close()
