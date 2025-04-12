import psycopg2
import csv

conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    host='localhost',
    port=5432
)
cur = conn.cursor()


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
    try:
        cur.execute("INSERT INTO PhoneBook (name , number) VALUES (%s , %s)" , (name , number))
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        print("Already exists")
    else:
        conn.commit()



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
