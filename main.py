from typing import Union, List
from fastapi import FastAPI, HTTPException
from models import User, Gender, Roles, UserUpdateRequest
from uuid import UUID, uuid4

app = FastAPI()

# def generate_uuid() -> UUID:
#     return UUID(str(uuid4()))

db: List[User] = [
    User(
        id=uuid4(),
        first_name="John",
        last_name="Doe",
        middle_name="Abel",
        gender=Gender.male,
        roles=[Roles.student]
    ),
    User(
        id=uuid4(),
        first_name="Jane",
        last_name="Daniel",
        middle_name="Coco",
        gender=Gender.female,
        roles=[Roles.admin]
    ) 
]


@app.get("/")
async def read_root(): 
    return {"Hello": "World"}


@app.get("/api/v1/users")
async def fetch_users():
    return db

@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}

@app.delete("/api/v1/users/{user.id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return {"message": f"User {user_id} deleted"}
        raise HTTPException(
            status_code=404,
            detail=f"user with id: {user_id} does not exist"
        )

# @app.put("/api/v1/users/{user.id}")
# async def update_user(user_id: UUID, updated_user: User):
#     for existing_user in db:
#         if existing_user.id == user_id:
#             db.remove(existing_user)
#             db.append(updated_user)
#             return {"message": f"User {user_id} updated"}
#         raise HTTPException(
#             status_code=404,
#             detail=f"User with id: {user_id} does not exist"
#         )
        
@app.put("/api/v1/users/{user.id}")
async def user_update(user_id: UUID, user_update: UserUpdateRequest):
    for user in db:
        if user.id == user_id:
            if user.first_name is not None:
                user.first_name = user_update.first_name
            if user.last_name is not None:
                user.last_name = user_update.last_name
            if user.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user.gender is not  None:
                user.gender = user_update.gender
            if user.roles is not None:
                user.roles = user_update.roles
            return {"message": f"User {user_id} updated"}
        
        raise HTTPException(
            status_code=404,
            detail=f"User with id: {user_id} does not exist"
        )