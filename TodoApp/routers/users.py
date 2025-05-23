from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from models import Todos, Users
from database import  SessionLocal
from pydantic import BaseModel, Field
from .auth import get_current_user
from passlib.context import CryptContext



router = APIRouter(
    prefix='/user',
    tags=['user']
)


#Pydantics model
class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

#Pydantics model to change phone number
class PhoneChange(BaseModel):
    new_phone_number: str    



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  

db_dependency = Annotated[Session, Depends(get_db)]  
user_dependency = Annotated[dict, Depends(get_current_user)] #This will be used as a middleware toe verify a user token
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')




#Get user profile
@router.get('/profile', status_code=status.HTTP_200_OK)
def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed.')
    return db.query(Users).filter(Users.id == user.get('id')).first()


#This endpoint will allow then to change there password
@router.put('/change-password', status_code=status.HTTP_204_NO_CONTENT)
def change_password(user: user_dependency, db: db_dependency, reset_request: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed.')
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not bcrypt_context.verify(reset_request.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Password incorrect.')
    
    user_model.hashed_password = bcrypt_context.hash(reset_request.new_password)
    db.add(user_model)
    db.commit()


#Endpoint to allow a user to change there phone number
@router.put('/phone-change', status_code=status.HTTP_200_OK)
def update_phone_number(user: user_dependency, db: db_dependency, new_phone: PhoneChange):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed.')
    
    user_phone_number = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_phone_number is None:
        raise HTTPException(status_code=401, detail='User not found.')
    
    #update phone number
    user_phone_number.phone_number = new_phone.new_phone_number
    db.add(user_phone_number)
    db.commit()