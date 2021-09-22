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
    pesel BIGINT NOT NULL,
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
    CURSOR = DB.cursor()
    create_database()
    DB.select_db(DB_NAME)
    create_tables()


def add_job(name, hour_rate, extra=0):
    query = """INSERT INTO stanowiska(name, hour_rate, extra) VALUES(%s, %s, %s);
    """
    CURSOR.execute(query, (name, hour_rate, extra))
    DB.commit()


def add_etat(name, hour_count):
    query = """INSERT INTO etaty(name, hour_count) VALUES(%s, %s);
    """
    CURSOR.execute(query, (name, hour_count))
    DB.commit()


def add_worker(name, surname, pesel, hire_date, id_stanowisko, id_etat):
    query = """INSERT INTO pracownicy(name, surname, pesel, hire_date, id_stanowisko, id_etat) 
    VALUES(%s, %s, %s, %s, %s, %s);
    """
    CURSOR.execute(query, (name, surname, pesel, hire_date, id_stanowisko, id_etat))
    DB.commit()


def close_connection():
    if DB:
        DB.close()


def print_earnings(month, year):
    query = """SELECT pracownicy.name, pracownicy.surname, pracownicy.pesel,
    stanowiska.name, stanowiska.hour_rate, stanowiska.extra, etaty.hour_count 
    FROM pracownicy, stanowiska, etaty
    WHERE pracownicy.id_stanowisko = stanowiska.id AND pracownicy.id_etat = etaty.id
    """
    CURSOR.execute(query)
    print(CURSOR.fetchall())
