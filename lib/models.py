from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

watchlist = Table(
    'watchlist',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('series_id', ForeignKey('series.id'), primary_key=True)
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)

    reviews = relationship("Review", back_populates="user")
    series = relationship("Series", back_populates="user")
    statuses = relationship("Status", back_populates="user")
    series = relationship('Series', secondary=watchlist, back_populates='users')


    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

    @classmethod
    def create(cls, session: Session, username):
        user = cls(username=username)
        session.add(user)
        session.commit()
        return user

    @classmethod
    def get_by_id(cls, session: Session, user_id):
        return session.query(cls).get(user_id)

    @classmethod
    def delete(cls, session: Session, user_id):
        user = cls.get_by_id(session, user_id)
        if user:
            session.delete(user)
            session.commit()
            return True
        return False

class Series(Base):
    __tablename__ = 'series'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    genre = Column(String)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="series")
    users = relationship('User', secondary=watchlist, back_populates='series')

    seasons = relationship("Season", back_populates="series", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="series", cascade="all, delete-orphan")
    statuses = relationship("Status", back_populates="series", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Series(id={self.id}, title='{self.title}', genre='{self.genre}')>"

    @classmethod
    def create(cls, session: Session, title, genre, description, user_id):
        series = cls(title=title, genre=genre, description=description, user_id=user_id)
        session.add(series)
        session.commit()
        return series

    @classmethod
    def get_by_id(cls, session: Session, series_id):
        return session.query(cls).get(series_id)

    @classmethod
    def delete(cls, session: Session, series_id):
        series = cls.get_by_id(session, series_id)
        if series:
            session.delete(series)
            session.commit()
            return True
        return False

class Season(Base):
    __tablename__ = 'seasons'

    id = Column(Integer, primary_key=True)
    season_number = Column(Integer, nullable=False)
    series_id = Column(Integer, ForeignKey('series.id'))

    series = relationship("Series", back_populates="seasons")
    episodes = relationship("Episode", back_populates="season", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Season(id={self.id}, season_number={self.season_number}, series_id={self.series_id})>"

    @classmethod
    def create(cls, session: Session, season_number, series_id):
        season = cls(season_number=season_number, series_id=series_id)
        session.add(season)
        session.commit()
        return season

    @classmethod
    def get_by_id(cls, session: Session, season_id):
        return session.query(cls).get(season_id)

    @classmethod
    def delete(cls, session: Session, season_id):
        season = cls.get_by_id(session, season_id)
        if season:
            session.delete(season)
            session.commit()
            return True
        return False

class Episode(Base):
    __tablename__ = 'episodes'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    episode_number = Column(Integer)
    duration_mins = Column(Integer)
    season_id = Column(Integer, ForeignKey('seasons.id'))

    season = relationship("Season", back_populates="episodes")

    def __repr__(self):
        return f"<Episode(id={self.id}, title='{self.title}', episode_number={self.episode_number})>"

    @classmethod
    def create(cls, session: Session, title, episode_number, duration_mins, season_id):
        episode = cls(title=title, episode_number=episode_number, duration_mins=duration_mins, season_id=season_id)
        session.add(episode)
        session.commit()
        return episode

    @classmethod
    def get_by_id(cls, session: Session, episode_id):
        return session.query(cls).get(episode_id)

    @classmethod
    def delete(cls, session: Session, episode_id):
        episode = cls.get_by_id(session, episode_id)
        if episode:
            session.delete(episode)
            session.commit()
            return True
        return False

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    rating = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    series_id = Column(Integer, ForeignKey('series.id'))

    user = relationship("User", back_populates="reviews")
    series = relationship("Series", back_populates="reviews")

    def __repr__(self):
        return f"<Review(id={self.id}, rating={self.rating})>"

    @classmethod
    def create(cls, session: Session, content, rating, user_id, series_id):
        review = cls(content=content, rating=rating, user_id=user_id, series_id=series_id)
        session.add(review)
        session.commit()
        return review

    @classmethod
    def delete(cls, session: Session, review_id):
        review = session.query(cls).get(review_id)
        if review:
            session.delete(review)
            session.commit()
            return True
        return False

class Status(Base):
    __tablename__ = 'statuses'

    id = Column(Integer, primary_key=True)
    watch_status = Column(String)

    user_id = Column(Integer, ForeignKey('users.id'))
    series_id = Column(Integer, ForeignKey('series.id'))

    user = relationship("User", back_populates="statuses")
    series = relationship("Series", back_populates="statuses")

    def __repr__(self):
        return f"<Status(id={self.id}, user_id={self.user_id}, series_id={self.series_id}, watch_status='{self.watch_status}')>"

    @classmethod
    def create(cls, session: Session, watch_status, user_id, series_id):
        status = cls(watch_status=watch_status, user_id=user_id, series_id=series_id)
        session.add(status)
        session.commit()
        return status

    @classmethod
    def delete(cls, session: Session, status_id):
        status = session.query(cls).get(status_id)
        if status:
            session.delete(status)
            session.commit()
            return True
        return False
