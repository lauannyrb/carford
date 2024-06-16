from sqlmodel import Field, SQLModel


class OwnerModel(SQLModel, table=True):

    __tablename__ = 'owners'

    id: int | None = Field(default=None, primary_key=True)
    name: str


class CarModel(SQLModel, table=True):

    __tablename__ = 'cars'

    id: int | None = Field(default=None, primary_key=True)
    color: str
    model: str
    owner_id: int = Field(foreign_key='owners.id')


class UserModel(SQLModel, table=True):

    __tablename__ = 'users'

    id: int | None = Field(default=None, primary_key=True)
    username: str
    password: str
