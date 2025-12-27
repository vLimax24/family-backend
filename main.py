import sqlite3
from time import strftime

sql_statements = [
    """CREATE TABLE IF NOT EXISTS person (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        role TEXT NOT NULL
    );""",
    """CREATE TABLE IF NOT EXISTS chore (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        interval INTEGER NOT NULL,
        last_done INTEGER,
        worker_id INTEGER,
        FOREIGN KEY(worker_id) REFERENCES person(id)
    );""",
    """CREATE TABLE IF NOT EXISTS plant (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        image TEXT,
        last_pour INTEGER,
        interval INTEGER NOT NULL,
        owner_id INTEGER,
        FOREIGN KEY(owner_id) REFERENCES person(id)
    );"""
]



with sqlite3.connect('main.db') as connection:
    cursor = connection.cursor()

    for i in sql_statements:
        cursor.execute(i)

    # Person Methods

    def getPersonById(person_id):
        cursor.execute("""SELECT * FROM person WHERE id = ?""", (person_id, ))
        return cursor.fetchone()

    def getAllPersons():
        cursor.execute("""SELECT * from person""")
        return cursor.fetchall()

    # Chore Methods

    def getChoresOfPerson(person_id):
        cursor.execute("""SELECT * FROM chore WHERE worker_id = ?""", (person_id, ))
        return cursor.fetchall()

    def getDueChoresOfPerson(person_id):
        cursor.execute("""SELECT * FROM chore WHERE worker_id = ? AND (last_done IS NULL OR last_done + interval*86400 <= CAST(strftime('%s', 'now') AS INTEGER))""", (person_id, ))
        return cursor.fetchall()

    def markChoreDone(chore_id):
        cursor.execute("""UPDATE chore SET last_done = CAST(strftime('%s', 'now') AS INTEGER) WHERE id = ?""", (chore_id, ))
        connection.commit()

    def addChore(name, interval, worker_id):
        cursor.execute("""INSERT INTO chore (name, interval, worker_id) VALUES (?, ?, ?)""", (name, interval, worker_id))
        connection.commit()

    def removeChore(chore_id):
        cursor.execute("""DELETE FROM chore WHERE id = ?""", (chore_id,))
        connection.commit()


    # Plant Methods

    def getPlantsOfPerson(person_id):
        cursor.execute("""SELECT * FROM plant WHERE owner_id = ?""", (person_id, ))
        return cursor.fetchall()

    def getDuePlantsOfPerson(person_id):
        cursor.execute("""SELECT * FROM plant WHERE owner_id = ? AND (last_pour IS NULL OR last_pour + interval*86400 <= CAST(strftime('%s', 'now') AS INTEGER))""", (person_id, ))
        return cursor.fetchall()

    def markPlantWatered(plant_id):
        cursor.execute("""UPDATE plant SET last_pour = CAST(strftime('%s', 'now') AS INTEGER) WHERE id = ?""", (plant_id, ))
        connection.commit()

    def addPlant(name, interval, image, owner_id):
        cursor.execute("""INSERT INTO plant (name, interval, image, owner_id) VALUES (?, ?, ?, ?)""", (name, interval, image, owner_id))
        connection.commit()

    def removePlant(plant_id):
        cursor.execute("""DELETE FROM plant WHERE id = ?""", (plant_id,))
        connection.commit()


    connection.commit()

