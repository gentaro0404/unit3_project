import sqlite3
from secure_password import hash_password, check_password

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from models import Users, Base

def create_base():
    engine = create_engine('sqlite:///vocab_app.db')
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    my_session = session()
    print(Base.metadata.tables.keys())
    print(engine.connect())
    return None
class database_handler:
    def __init__(self,dbname):
        self.session = None
        engine = create_engine(f"sqlite:///{dbname}")
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close(self):
        self.session.close()

    def insert_user(self, email, username, password):
        if not self.session.query(Users).filter_by(email=email).first():
            new_user = Users(email=email, username=username, password=password)
            self.session.add(new_user)
            self.session.commit()
            print("User registered")
        else:
            print("User already exists")

    def check_user(self, email):
        try:
            user = self.session.query(Users).filter_by(email=email).one()
            return True
        except NoResultFound:
            return False
    def login_check(self, username, password):
        user = self.session.query(Users).filter_by(username=username).first()
        if not user:
            return False

        if check_password(password, user.password):
            return True
        else:
            return False

create_base()
test = database_handler("vocab_app.db")
print(test.check_user("haha@haha.com"))


