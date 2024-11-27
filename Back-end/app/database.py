from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Load biến môi trường từ .env
load_dotenv()

# Lấy URI từ file .env
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")  # URI mặc định
DATABASE_NAME = os.getenv("DATABASE_NAME", "test_database")  # Tên DB

# Tạo client MongoDB
client = AsyncIOMotorClient(MONGO_URI)
database = client[DATABASE_NAME]
users_collection = database.get_collection("users")  # Collection tên "users"
