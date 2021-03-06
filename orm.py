from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, insert, select, and_, between, or_, join, \
    func, text, bindparam
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


def zad_2_2():
    connection = ENGINE.connect()
    joined_tables = join(Director, Movie)
    select_query = select(
        [func.count(Movie.movie_id), Director.name, Director.surname, func.avg(Movie.rating)]).select_from(
        joined_tables).group_by(Director.director_id)
    result = connection.execute(select_query)
    print(result.fetchall())
    connection.close()

    result = SESSION.query(func.count(Movie.movie_id), Director.name, Director.surname, func.avg(Movie.rating)).join(
        Director).group_by(Director.director_id).all()
    print(result)


def zad_2_3():
    joined_tables = join(Director, Movie)
    select_query = select(
        [func.count(Movie.movie_id), Director.name, Director.surname, func.avg(Movie.rating)]).select_from(
        joined_tables).group_by(Director.director_id)
    print(select_query)

    result = SESSION.query(func.count(Movie.movie_id), Director.name, Director.surname, func.avg(Movie.rating)).join(
        Director).group_by(Director.director_id)
    print(result)


def zad_2_4():
    q = text(
        'SELECT count(movies.movie_id) AS count_1, directors.name, directors.surname, avg(movies.rating) AS avg_1 FROM '
        'directors '
        'JOIN movies ON directors.director_id = movies.director_id '
        'WHERE movies.year '
        'BETWEEN :start_year AND :end_year '
        'GROUP BY directors.director_id')
    result = SESSION.query(text('count_1'), text('name'), text('surname'), text('avg_1')).from_statement(q).params(
        start_year=1950,
        end_year=2000).all()
    print(result)


def zad_2_5():
    q = text(
        'SELECT count(movies.movie_id) AS count_1, directors.name, directors.surname, avg(movies.rating) AS avg_1 FROM '
        'directors '
        'JOIN movies ON directors.director_id = movies.director_id '
        'WHERE movies.year '
        'BETWEEN :start_year AND :end_year '
        'GROUP BY directors.director_id')
    q.bindparams(
        bindparam('start_year', type_=Integer),
        bindparam('end_year', type_=Integer),
    )
    result = SESSION.query(text('count_1'), text('name'), text('surname'), text('avg_1')).from_statement(q).params(
        start_year=2000, end_year=2010).all()
    print(result)

    connection = ENGINE.connect()
    result = connection.execute(q, start_year=2000, end_year=2010)
    for row in result:
        print(f"{row.count_1, row.name, row.surname, row.avg_1}")
    print(result.fetchall())
    connection.close()


# ZAD 2.6
def get_directors_statistics(session, start_year, end_year):
    q = text(
        'SELECT count(movies.movie_id) AS count_1, directors.name, directors.surname, avg(movies.rating) AS avg_1 FROM '
        'directors '
        'JOIN movies ON directors.director_id = movies.director_id '
        'WHERE movies.year '
        'BETWEEN :start_year AND :end_year '
        'GROUP BY directors.director_id')
    q.bindparams(
        bindparam('start_year', type_=Integer),
        bindparam('end_year', type_=Integer),
    )
    result = session.query(text('count_1'), text('name'), text('surname'), text('avg_1')).from_statement(q).params(
        start_year=start_year, end_year=end_year).all()
    return result


def zad_2_7():
    subq = SESSION.query(Movie.director_id).filter(and_(Movie.year < 2001, Movie.title.like('T%'))).subquery()

    SESSION.query(Director).filter(Director.director_id.in_(subq)).update(
        {'rating': (Director.rating + 1)}, synchronize_session='fetch')
    SESSION.commit()


def zad_2_8(name):
    with SESSION.begin():
        subquery = SESSION.query(Director.director_id).filter(Director.name == name).subquery()
        SESSION.query(Movie).filter(Movie.director_id.in_(subquery)).delete(synchronize_session='fetch')
        SESSION.query(Director).filter(Director.name == name).delete()


def delete_director(**kwargs):
    if 'name' in kwargs:
        query = text('SELECT directors.director_id FROM directors WHERE directors.name = :name')
    elif 'surname' in kwargs:
        query = text('SELECT directors.director_id FROM directors WHERE directors.surname = :surname')
    else:
        return
    with SESSION.begin():
        director_id = SESSION.query(Director.director_id).from_statement(query).params(**kwargs).first()[0]
        SESSION.query(Movie).filter(Movie.director_id == director_id).delete()
        SESSION.query(Director).filter(Director.director_id == director_id).delete()


delete_director(surname='Nolan')
# print(get_directors_statistics(SESSION, 1950,2001))
# zad_2_7()
# print(get_directors_statistics(SESSION, 1950,2001))
