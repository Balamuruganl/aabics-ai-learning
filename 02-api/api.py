from fastapi import FastAPI
from pydantic import BaseModel

#FastAPI is a modern, high-performance Python web framework used primarily for building APIs (Application Programming Interfaces) and backend systems.
app=FastAPI()

#Root endpoint
@app.get("/welcome")
def welcome():
    return {"message": "Welcome to the FastAPI application!"}

#Example Get API with a parameter
@app.get("/user")
def user_profile():
    return {
        "name": "Balamurugan Loganathan",
        "email": "balamurugan.l@gmail.com",
        "LinkedIn": "https://www.linkedin.com/in/balamurugan-loganathan-b1b845297/"
    }

@app.get("/user/{user_id}")
def get_user(user_id: int):
    if user_id <= 0 :
        return {"error": "Invalid user ID. Please provide a positive integer."}
    else:
        return {"user_id": user_id, "name": "User Name", "email": "balamurugan.l@gmail.com"}


class User(BaseModel):
    name: str
    email: str
    age: int

users=[]

@app.post("/users")
def create_user(user: User):
    users.append(user)
    return {"message": "User created successfully", "total_users": len(users)}




