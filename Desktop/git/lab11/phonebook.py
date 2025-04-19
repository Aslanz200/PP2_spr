import psycopg2
import csv

conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    host='localhost',
    port=5432
)
cur = conn.cursor()



def get_starting_with(letter: str):
    cur.execute("SELECT name FROM PhoneBook WHERE name LIKE %s", (letter + '%',))
    result = cur.fetchall()
    return result



def find_pattern(pattern : str):
    cur.execute("SELECT * FROM PhoneBook WHERE name LIKE %s" , (f'%{pattern}%' , ))
    result = cur.fetchall()
    return result



def insertCSV(filepath):
    with open(filepath) as sometable:
        read = csv.reader(sometable)
        for row in read:
            try:
                cur.execute("INSERT INTO PhoneBook (name, number) VALUES (%s, %s)", (row[0], row[1]))
            except psycopg2.errors.UniqueViolation:
                conn.rollback()
                print("already exists")
            else:
                conn.commit()



def insertFromConsole():
    name = input("Name: ")
    number = input("Number: ")
    
    cur.execute("SELECT * FROM PhoneBook WHERE name = %s", (name,))
    result = cur.fetchone()

    if result:
        cur.execute("UPDATE PhoneBook SET number = %s WHERE name = %s", (number, name))
        conn.commit()
    else: 
        try:
            cur.execute("INSERT INTO PhoneBook (name, number) VALUES (%s, %s)", (name, number))
            conn.commit()
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            print("Already exists")

    


def updateData(column , old , new):
    if column == "name":
        cur.execute("UPDATE PhoneBook SET name = %s WHERE name ILIKE %s" , (new , old))
    elif column == "number":
        cur.execute("UPDATE PhoneBook SET number = %s WHERE number ILIKE %s" , (new , old))
    conn.commit()



def query(filter , value):
    if filter == "name":
        cur.execute("SELECT * FROM PhoneBook WHERE name ILIKE %s", (f"%{value}%",))
    elif filter == "number":
        cur.execute("SELECT * FROM PhoneBook WHERE number ILIKE %s", (f"%{value}%",))
    else:
        cur.execute("SELECT * FROM PhoneBook")
    
    results = cur.fetchall()
    for row in results:
        print(row)




def deleteData(data):
    cur.execute("DELETE FROM PhoneBook WHERE name = %s OR number = %s" , (data , data))
    conn.commit()



data = [("aslan" , 777) , ("beka" , 888) , ("toha" , 999)]
def insert_list(arr : list):
    for tuples in arr:
        if len(tuples) == 2 and isinstance(tuples[0], str) and isinstance(tuples[1], int):
            name = tuples[0]
            number = tuples[1]
            try:
                cur.execute("INSERT INTO PhoneBook(name , number) VALUES (%s , %s)" , (name , number))
            except psycopg2.errors.UniqueViolation:
                conn.rollback()
                print("Already exists")
            else:
                conn.commit()

        else:
            print(f"incorrect data : {tuples}")




def get_paginated_contacts(limit: int, offset: int) -> list:
    try:
        cur.execute("SELECT * FROM PhoneBook ORDER BY id LIMIT %s OFFSET %s", (limit, offset))
        return cur.fetchall()
    except Exception as e:
        print(f"Database error: {e}")
        conn.rollback()
        return []



def delete_row(data):
    if isinstance(data, int):
        cur.execute("DELETE FROM Phonebook WHERE number = %s", (data,))
    elif isinstance(data, str):
        cur.execute("DELETE FROM Phonebook WHERE name = %s", (data,))
    conn.commit()


cur.execute("""
    CREATE TABLE IF NOT EXISTS PhoneBook (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        number VARCHAR(25),
        UNIQUE (name , number)
    );
""")



conn.commit()

cur.close()
conn.close()