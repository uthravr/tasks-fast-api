import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / ".env")

# Database settings
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:1234@localhost:3306/user_management_db"
)

# JWT settings
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "e83a99bf723c34a9080be86a4c281ef546059d09c3bf9ecf2fbb1cf99166a9ba"
)
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
