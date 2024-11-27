from bson import ObjectId
from pydantic import BaseModel, EmailStr
from typing import Optional

# Helper để xử lý ObjectId của MongoDB
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# Schema User để thao tác dữ liệu
class UserModel(BaseModel):
    id: Optional[PyObjectId] = None
    username: str
    email: EmailStr
    hashed_password: str
    role: str = "user"  # Mặc định vai trò là "user"
    profile: Optional[dict] = None  # Thông tin hồ sơ (name, avatar, etc.)
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "exampleuser",
                "email": "user@example.com",
                "hashed_password": "hashed_password_here",
                "role": "admin",
                "profile": {
                    "name": "John Doe",
                    "avatar": "https://example.com/avatar.png",
                    "dateOfBirth": "2000-01-01",
                    "address": "123 Example St",
                    "phoneNum": "+1234567890",
                },
                "createdAt": "2024-01-01T00:00:00",
                "updatedAt": "2024-01-02T00:00:00",
            }
        }
