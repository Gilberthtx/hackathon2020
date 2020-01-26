from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
import datetime
from peewee import *

# create database
DATABASE = SqliteDatabase('app.db')


'''MODEL FOR USER'''


class User(UserMixin, Model):
    # inputs needed to create a user account
    name = CharField(max_length=100)
    email = CharField(unique=True)
    password = CharField(max_length=100)

    # assigning the database to this class
    class Meta:
        database = DATABASE

    # function to get all stocks in watchlist
    def get_flights(self):
        return Flight.select().where(Flight.user == self)

    # method to create user account
    @classmethod
    def create_user(cls, name, email, password):
        try:
            with DATABASE.transaction():
                cls.create(
                    name=name,
                    email=email,
                    password=generate_password_hash(password)
                )
        # expects that an error could occur if user exists
        except IntegrityError:
            raise ValueError("User already exists")


'''MODEL FOR FLIGHTS'''


class Flight(Model):
    # stores the time the user added the stock
    timestamp = DateTimeField(default=datetime.datetime.now)
    # assigns that stock to the user that wanted to add that stock to their watchlist
    user = ForeignKeyField(
        model=User,
        related_name='flight'
    )
    # stores the stock symbol for later use
    flight_number = TextField()
    origin = TextField()
    destination = TextField()
    departure_time = TextField()
    arrival_time = TextField()
    date = TextField()

    # assigns its database and sorts it by the time it was added
    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)


'''INITIALIZE DATABASE'''


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Flight], safe=True)
    DATABASE.close()
