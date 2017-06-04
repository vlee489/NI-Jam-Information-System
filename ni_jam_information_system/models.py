from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, BigInteger
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from ni_jam_information_system.secret.config import db_user, db_pass, db_name


engine = create_engine('mysql+pymysql://{}:{}@localhost/{}'.format(db_user, db_pass, db_name))
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()
metadata = Base.metadata


class Attendee(Base):
    __tablename__ = 'attendees'

    attendee_id = Column(Integer, primary_key=True, unique=True)
    first_name = Column(String(45), nullable=False)
    surname = Column(String(45), nullable=False)
    age = Column(Integer)
    email_address = Column(String(45), nullable=False)
    gender = Column(String(45))
    town = Column(String(45))
    experience_level = Column(String(45))
    school = Column(String(45))

    workshop_runs = relationship('RaspberryJamWorkshop', secondary='workshop_attendee')


class Group(Base):
    __tablename__ = 'groups'

    group_id = Column(Integer, primary_key=True, unique=True)
    group_name = Column(String(45))


class JamAttendance(Base):
    __tablename__ = 'jam_attendance'

    attendee_id = Column(ForeignKey('attendees.attendee_id'), primary_key=True, nullable=False, index=True)
    jam_id = Column(ForeignKey('raspberry_jam.jam_id'), primary_key=True, nullable=False, index=True)
    checked_in = Column(Integer)

    attendee = relationship('Attendee')
    jam = relationship('RaspberryJam')


class LoginCookie(Base):
    __tablename__ = 'login_cookie'

    cookie_id = Column(Integer, primary_key=True, unique=True)
    cookie_value = Column(String(45))
    cookie_expiry = Column(DateTime)


class LoginUser(Base):
    __tablename__ = 'login_users'

    user_id = Column(Integer, primary_key=True, nullable=False, unique=True)
    username = Column(String(45), nullable=False, unique=True)
    password_hash = Column(String(45), nullable=False)
    password_salt = Column(String(45), nullable=False)
    first_name = Column(String(45), nullable=False)
    surname = Column(String(45), nullable=False)
    volunteer = Column(Integer)
    login_cookie_id = Column(ForeignKey('login_cookie.cookie_id'), primary_key=True, nullable=False, index=True)
    group_id = Column(ForeignKey('groups.group_id'), primary_key=True, nullable=False, index=True)

    group = relationship('Group')
    login_cookie = relationship('LoginCookie')
    workshop_runs = relationship('RaspberryJamWorkshop', secondary='workshop_volunteers')


class PagePermission(Base):
    __tablename__ = 'page_permissions'

    page_id = Column(Integer, primary_key=True, nullable=False)
    page_name = Column(String(45), nullable=False)
    group_required = Column(ForeignKey('groups.group_id'), primary_key=True, nullable=False, index=True)

    group = relationship('Group')


class RaspberryJam(Base):
    __tablename__ = 'raspberry_jam'

    jam_id = Column(BigInteger, primary_key=True)
    name = Column(String(45), nullable=False)
    date = Column(DateTime, nullable=False)
    food_after = Column(Integer)


class RaspberryJamWorkshop(Base):
    __tablename__ = 'raspberry_jam_workshop'

    workshop_run_id = Column(Integer, primary_key=True, unique=True)
    jam_id = Column(ForeignKey('raspberry_jam.jam_id'), nullable=False, index=True)
    workshop_id = Column(ForeignKey('workshop.workshop_id'), nullable=False, index=True)
    workshop_room_id = Column(ForeignKey('workshop_room.room_id'), nullable=False, index=True)

    jam = relationship('RaspberryJam')
    workshop = relationship('Workshop')
    workshop_room = relationship('WorkshopRoom')


class VolunteerAttendance(Base):
    __tablename__ = 'volunteer_attendance'

    user_id = Column(ForeignKey('login_users.user_id'), primary_key=True, nullable=False, index=True)
    jam_id = Column(ForeignKey('raspberry_jam.jam_id'), primary_key=True, nullable=False, index=True)
    volunteer_attending = Column(Integer)
    setup_attending = Column(Integer)
    packdown_attending = Column(Integer)
    food_attending = Column(Integer)

    jam = relationship('RaspberryJam')
    user = relationship('LoginUser')


class Workshop(Base):
    __tablename__ = 'workshop'

    workshop_id = Column(Integer, primary_key=True)
    workshop_title = Column(String(45), nullable=False)
    workshop_limit = Column(Integer, nullable=False)
    workshop_description = Column(String(200))
    workshop_level = Column(String(45))


t_workshop_attendee = Table(
    'workshop_attendee', metadata,
    Column('attendee_id', ForeignKey('attendees.attendee_id'), primary_key=True, nullable=False, index=True),
    Column('workshop_run_id', ForeignKey('raspberry_jam_workshop.workshop_run_id'), primary_key=True, nullable=False, index=True)
)


class WorkshopRoom(Base):
    __tablename__ = 'workshop_room'

    room_id = Column(Integer, primary_key=True, unique=True)
    room_name = Column(String(45))
    room_capacity = Column(String(45))


t_workshop_volunteers = Table(
    'workshop_volunteers', metadata,
    Column('user_id', ForeignKey('login_users.user_id'), primary_key=True, nullable=False, index=True),
    Column('workshop_run_id', ForeignKey('raspberry_jam_workshop.workshop_run_id'), primary_key=True, nullable=False, index=True)
)