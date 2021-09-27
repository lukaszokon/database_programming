from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, insert, select, and_, between, or_, join
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

ENGINE = create_engine('mysql://user:lukasz@localhost:3306/cinematic')
base = declarative_base()


class Director(base):
    __tablename__ = 'directors'

    director_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), nullable=False)
    surname = Column(String(40), nullable=False)
    rating = Column(Integer, nullable=False)
    movies = relationship('Movie', back_populates='director')


class Movie(base):
    __tablename__ = 'movies'

    movie_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(40), nullable=False)
    year = Column(Integer, nullable=False)
    category = Column(String(20), nullable=False)
    director_id = Column(Integer, ForeignKey('directors.director_id'), nullable=False)
    rating = Column(Integer, nullable=False)
    director = relationship('Director', back_populates='movies')

    def __repr__(self):
        return f"Tytuł: {self.title} Kategoria: {self.category}"


# base.metadata.create_all(ENGINE)
Session = sessionmaker(bind=ENGINE)
SESSION = Session()


def add_default_data():
    directors = [{'name': 'Frank', 'surname': 'Darabont', 'rating': 7},
                 {'name': 'Francis Ford', 'surname': 'Coppola', 'rating': 8},
                 {'name': 'Quentin', 'surname': 'Tarantino', 'rating': 10},
                 {'name': 'Christopher', 'surname': 'Nolan', 'rating': 9},
                 {'name': 'David', 'surname': 'Fincher', 'rating': 7}]

    SESSION.add_all((Director(**director) for director in directors))
    SESSION.commit()

    movies = [{'title': 'The Shawshank Redemption', 'year': 1994, 'category': 'Drama', 'director_id': 1, 'rating': 8},
              {'title': 'The Green Mile', 'year': 1999, 'category': 'Drama', 'director_id': 1, 'rating': 6},
              {'title': 'The Godfather', 'year': 1972, 'category': 'Crime', 'director_id': 2, 'rating': 7},
              {'title': 'The Godfather III', 'year': 1990, 'category': 'Crime', 'director_id': 2, 'rating': 6},
              {'title': 'Pulp Fiction', 'year': 1994, 'category': 'Crime', 'director_id': 3, 'rating': 9},
              {'title': 'Inglourious Basterds', 'year': 2009, 'category': 'War', 'director_id': 3, 'rating': 8},
              {'title': 'The Dark Knight', 'year': 2008, 'category': 'Action', 'director_id': 4, 'rating': 9},
              {'title': 'Interstellar', 'year': 2014, 'category': 'Sci-fi', 'director_id': 4, 'rating': 8},
              {'title': 'The Prestige', 'year': 2006, 'category': 'Drama', 'director_id': 4, 'rating': 10},
              {'title': 'Fight Club', 'year': 1999, 'category': 'Drama', 'director_id': 5, 'rating': 7},
              {'title': 'Zodiac', 'year': 2007, 'category': 'Crime', 'director_id': 5, 'rating': 5},
              {'title': 'Seven', 'year': 1995, 'category': 'Drama', 'director_id': 5, 'rating': 8},
              {'title': 'Alien 3', 'year': 1992, 'category': 'Horror', 'director_id': 5, 'rating': 5}]

    connection = ENGINE.connect()

    insert_movies = insert(Movie)
    connection.execute(insert_movies, movies)

    connection.close()


def zad_6():
    connection = ENGINE.connect()

    select_query = select([Movie]).where(and_(Movie.category == 'Drama', Movie.year > 1994))
    result = connection.execute(select_query)
    print(result.fetchall())
    connection.close()

    result = SESSION.query(Movie).filter(and_(Movie.category == 'Drama', Movie.year > 1994)).all()
    print(result)


def zad_7():
    connection = ENGINE.connect()

    select_query = select([Movie.category, Movie.rating]).where(
        and_(Movie.rating > 7, between(Movie.year, 2000, 2010))).order_by(Movie.rating.desc())
    result = connection.execute(select_query)
    print(result.fetchall())
    connection.close()

    result = SESSION.query(Movie.category, Movie.rating).filter(
        and_(Movie.rating > 7, between(Movie.year, 2000, 2010))).order_by(Movie.rating.desc()).all()
    print(result)


def zad_8():
    connection = ENGINE.connect()

    select_query = select([Director.surname]).where(
        and_(Director.rating >= 6, or_(Director.name.like('D%'), Director.name.like('%n'))))
    result = connection.execute(select_query)
    print(result.fetchall())
    connection.close()

    result = SESSION.query(Director.surname).filter(
        and_(Director.rating >= 6, (Director.name.like('D%') | Director.name.like('%n')))).all()
    print(result)


def zad_2_1():
    connection = ENGINE.connect()
    joined_tables = join(Director, Movie)
    select_query = select([Director.name, Director.surname]).select_from(joined_tables).where(
        and_(Movie.rating < 9, between(Movie.year, 2011, 2014))
    )
    result = connection.execute(select_query)
    print(result.fetchall())
    connection.close()

    result = SESSION.query(Director.name, Director.surname).join(Movie).filter(
        and_(Movie.rating < 9, between(Movie.year, 2011, 2014))).all()
    print(result)


zad_2_1()
