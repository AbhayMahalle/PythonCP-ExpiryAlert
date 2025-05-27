from sqlalchemy import Column, Integer, String, create_engine,Date
from sqlalchemy.orm import declarative_base, sessionmaker
from passlib.context import CryptContext


DATABASE_URL = "sqlite:///users.db"

Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    shop_name = Column(String, nullable=False)


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    batch = Column(String(50), nullable=False)
    expiry_date = Column(Date, nullable=False)
    user_id = Column(Integer, nullable=True)



def hash_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_db():
    Base.metadata.create_all(bind=engine)
