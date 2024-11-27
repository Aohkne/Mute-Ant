from fastapi import APIRouter, HTTPException, Depends
from app.models.user import UserModel
from app.database import users_collection
from bson import ObjectId
from datetime import datetime
import hashlib

router = APIRouter()

# Helper mã hóa password
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/", response_model=UserModel)
async def create_user(user: UserModel):
    # Kiểm tra email đã tồn tại
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Tạo user mới
    user.hashed_password = hash_password(user.hashed_password)  # Hash password
    user.createdAt = datetime.utcnow().isoformat()
    user.updatedAt = datetime.utcnow().isoformat()

    result = await users_collection.insert_one(user.dict(exclude={"id"}))
    user.id = result.inserted_id
    return user

@router.get("/{user_id}", response_model=UserModel)
async def get_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")

    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserModel)
async def update_user(user_id: str, user: UserModel):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")

    user.updatedAt = datetime.utcnow().isoformat()
    update_result = await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": user.dict(exclude={"id", "createdAt"})},
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return await users_collection.find_one({"_id": ObjectId(user_id)})

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")

    delete_result = await users_collection.delete_one({"_id": ObjectId(user_id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
