import os
from dotenv import load_dotenv


load_dotenv()

SQLALCHEMY_DB_URL = os.getenv("SQLALCHEMY_DB_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
