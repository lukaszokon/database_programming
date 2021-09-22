import MySQLdb, earnings_calculation


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
        category VARCHAR(30), director_id INT NOT NULL, rating INT NOT NULL, 
        FOREIGN KEY (director_id) REFERENCES directors(director_id) 
    );
    """
    cursor.execute(create_directors_query)
    cursor.execute(create_movies_query)


def insert_default_data(cursor, connection):
    directors = [
        ('Frank', 'Darabont', 7),
        ('Francis Ford', 'Coppola', 8),
        ('Quentin', 'Tarantino', 10),
        ('Christopher', 'Nolan', 9),
        ('David', 'Fincher', 7)]

    movies = [('The Shawshank Redemption', 1994, 'Drama', 1, 8), ('The Green Mile', 1999, 'Drama', 1, 6),
              ('The Godfather', 1972, 'Crime', 2, 7), ('The Godfather III', 1990, 'Crime', 2, 6),
              ('Pulp Fiction', 1994, 'Crime', 3, 9), ('Inglourious Basterds', 2009, 'War', 3, 8),
              ('The Dark Knight', 2008, 'Action', 4, 9), ('Interstellar', 2014, 'Sci-fi', 4, 8),
              ('The Prestige', 2006, 'Drama', 4, 10), ('Fight Club', 1999, 'Drama', 5, 7),
              ('Zodiac', 2007, 'Crime', 5, 5),
              ('Seven', 1995, 'Drama', 5, 8), ('Alien 3', 1992, 'Horror', 5, 5)]

    insert_directors_query = """INSERT INTO directors (name, surname, rating) VALUES(%s, %s, %s)"""
    insert_movies_query = """INSERT INTO movies (title, year, category, director_id, rating) 
    VALUES(%s, %s, %s, %s, %s)"""

    cursor.executemany(insert_directors_query, directors)
    connection.commit()
    cursor.executemany(insert_movies_query, movies)
    connection.commit()


if __name__ == '__main__':
    earnings_calculation.connect_to_database()