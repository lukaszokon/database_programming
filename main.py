import MySQLdb


def connect_to_database():
    return MySQLdb.connect('localhost', 'root', 'lukasz', database='cinematic')


def create_default_tables(cursor):
    create_directors_query = """
    CREATE TABLE directors(
        director_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL, name VARCHAR(40) NOT NULL, surname VARCHAR(40) NOT NULL,
        rating INT NOT NULL 
    );
    """
    create_movies_query = """
    CREATE TABLE movies(
        movie_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL, title VARCHAR(30) NOT NULL, year INT UNSIGNED NOT NULL,
        director_id INT NOT NULL, rating INT NOT NULL, 
        FOREIGN KEY (director_id) REFERENCES directors(director_id) 
    );
    """
    cursor.execute(create_directors_query)
    cursor.execute(create_movies_query)


if __name__ == '__main__':
    connection = connect_to_database()
    with connection:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS cinematic;")
        create_default_tables(cursor)
