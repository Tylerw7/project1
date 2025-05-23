from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from models import Todos
from database import  SessionLocal
from pydantic import BaseModel, Field
from .auth import get_current_user



router = APIRouter(
    prefix='/admin',
    tags=['admin']
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  

db_dependency = Annotated[Session, Depends(get_db)]  
user_dependency = Annotated[dict, Depends(get_current_user)] #This will be used as a middleware toe verify a user token





#Admin get all users
@router.get('/todo', status_code=status.HTTP_200_OK)
def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication failed')
    return db.query(Todos).all()


#Admin delete any todo
@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(user: user_dependency, db: db_dependency, todo_id: int):

    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='User not authorize')
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Not found')
    
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()