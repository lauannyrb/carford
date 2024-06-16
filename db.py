import os

import bcrypt
from sqlmodel import Session, SQLModel, create_engine

from models import UserModel

sqlite_file_name = 'data/database.sqlite'

if os.path.isfile('testing'):
    sqlite_file_name = 'data/database_test.sqlite'

sqlite_url = f'sqlite:///{sqlite_file_name}'
engine = create_engine(sqlite_url)

if not os.path.isdir('data'):
    os.makedirs('data')

if not os.path.isfile(sqlite_file_name):
    SQLModel.metadata.create_all(engine)
    session = Session(engine)

    password = bcrypt.hashpw(b'admin', bcrypt.gensalt())
    user = UserModel(username='admin', password=password)

    session.add(user)
    session.commit()

    session.close()
