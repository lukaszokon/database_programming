import MySQLdb

DB_NAME = "company"

DB = None
CURSOR = None


def create_database():
    CURSOR.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")


def create_tables():
    create_etaty_query = """
    CREATE TABLE IF NOT EXISTS etaty(
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    name VARCHAR(50) NOT NULL,
    hour_count FLOAT(10,1) NOT NULL
    );"""
    CURSOR.execute(create_etaty_query)

    create_stanowiska_query = """
    CREATE TABLE IF NOT EXISTS stanowiska(
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    name VARCHAR(50) NOT NULL,
    hour_rate FLOAT(10,2) NOT NULL,
    extra FLOAT(10,2) DEFAULT(0.0) NOT NULL
    );"""
    CURSOR.execute(create_stanowiska_query)

    create_pracownicy_query = """
    CREATE TABLE IF NOT EXISTS pracownicy(
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    pesel INT NOT NULL,
    hire_date DATE NOT NULL,
    id_stanowisko INT NOT NULL,
    id_etat INT NOT NULL,
    FOREIGN KEY (id_stanowisko) REFERENCES stanowiska(id),
    FOREIGN KEY (id_etat) REFERENCES etaty(id)
    );"""
    CURSOR.execute(create_pracownicy_query)


def connect_to_database():
    global DB, CURSOR
    DB = MySQLdb.connect('localhost', 'root', 'lukasz')
    with DB:
        CURSOR = DB.cursor()
        create_database()
        DB.select_db(DB_NAME)
        create_tables()
