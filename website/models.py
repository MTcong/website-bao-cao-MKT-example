from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import date
from faker import Faker
from werkzeug.security import generate_password_hash
import requests, random


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(150), unique=True)
    phone = db.Column(db.String(20), default="")
    cccd = db.Column(db.String(20), default="")
    password = db.Column(db.String(150))
    address = db.Column(db.String(10000), default="")
    role = db.Column(db.String(10000), default="staff")
    dob = db.Column(db.Date(), default=date(2000, 1, 1))
    stk = db.Column(db.String(20), default="")
    bank_id = db.Column(db.Integer, db.ForeignKey('bank.id'), default=1)
    avatar_url = db.Column(db.String(10000), default='../static/sneat/assets/img/avatars/user.png')
    hour_reports = db.relationship('Hour_report')
    day_reports = db.relationship('Day_report')
    posts = db.relationship('Post')

    def has_role(self, role):
        return self.role == role

    def create_admin():
        admin_user = User(
                name='Vũ Hải Long',
                email='vhlong1706@gmail.com',
                phone='',
                cccd='',
                password=generate_password_hash('vhlong1706@gmail.com'),
                address='',
                role='admin',
                dob=date(2000, 1, 1),
                stk="",
                bank_id=1,
                avatar_url = '../static/sneat/assets/img/avatars/user.png'
            )
        db.session.add(admin_user)
        db.session.commit()

    def create_random_staffs():
        fake = Faker()
        staff = User(
            name=fake.name(),
            email=fake.unique.email(),
            phone=fake.phone_number(),
            cccd=random.randint(100000000000, 999999999999),
            password=generate_password_hash('A@123456'),
            address=fake.address(),
            role='staff',
            dob=fake.date_of_birth(tzinfo=None, minimum_age=20, maximum_age=60),
            stk=str(random.randint(100000, 9999999999999999999)),
            bank_id = random.randint(1, 20),
            avatar_url = '../static/sneat/assets/img/avatars/user.png'
        )
        db.session.add(staff)
        db.session.commit()


class Bank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    code = db.Column(db.String(100), unique=True)
    bin = db.Column(db.String(10))
    shortName = db.Column(db.String(1000), default="")
    logo = db.Column(db.String(1000), default="")
    swift_code = db.Column(db.String(10), default="")
    users = db.relationship('User')

    def create_bank_data():
        try:
            response = requests.get('https://api.vietqr.io/v2/banks')
            if response.status_code==200:
                data = response.json()['data']
                for bank in data:
                    new_bank = Bank(
                        id = bank['id'],
                        name = bank['name'],
                        code = bank['code'],
                        bin = bank['bin'],
                        shortName = bank['shortName'],
                        logo = bank['logo'],
                        swift_code = bank['swift_code']
                    )
                    db.session.add(new_bank)
            db.session.commit()
        except Exception as e:
            print(f"Exception: {e}")


class Hour_report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=1)
    time = db.Column(db.DateTime)
    cost = db.Column(db.Integer, default=0)
    phoneNumber = db.Column(db.Integer, default=0)
    revenue = db.Column(db.Integer, default=0)


class Day_report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=1)
    time = db.Column(db.DateTime)
    newRevenue = db.Column(db.Integer, default=0)
    advanceBudget = db.Column(db.Integer, default=0)
    realBudget = db.Column(db.Integer, default=0)
    phoneNumber = db.Column(db.Integer, default=0)
    mess = db.Column(db.Integer, default=0)
    refund = db.Column(db.Integer, default=0)
    shopeeRevenue = db.Column(db.Integer, default=0)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=1)
    time = db.Column(db.Date, default=date.today())
    link = db.Column(db.String(10000), default="")
    type = db.Column(db.String(1000), default="")
    content = db.Column(db.String(1000), default="")
    budget = db.Column(db.Integer, default=0)
    cpm = db.Column(db.Integer, default=0)
    cpc = db.Column(db.Integer, default=0)
    ctr = db.Column(db.Float, default=0)
    cpa = db.Column(db.Integer, default=0)
    order = db.Column(db.Integer, default=0)
    review = db.Column(db.String(10000), default="")

    def create_random_post():
        fake = Faker()
        for _ in range(5):
            post = Post(
                user_id = random.randint(1, 5),
                time = date.today(),
                link = "https://facebook.com",
                type = 'video',
                content = fake.text(),
                budget = random.randint(100000, 1000000),
                cpm = random.randint(10000, 100000),
                cpc = random.randint(100000, 1000000),
                ctr = 1.02,
                cpa = random.randint(100000, 1000000),
                order = random.randint(1, 3),
                review = fake.text()
            )
            db.session.add(post)
        db.session.commit()


class Target(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    revenue = db.Column(db.Integer, default=0)
    phone = db.Column(db.Integer, default=0)
    budget = db.Column(db.Integer, default=0)

