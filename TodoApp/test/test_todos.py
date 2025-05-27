from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from database import Base
from main import app
from routers.todos import get_db, get_current_user
from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.orm import sessionmaker
import pytest
from models import Todos


SQLALCHEMY_DATABASE_URL="sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass= StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()  


def overrde_get_current_user():
    return {'username': 'tyler', 'id': 1, 'user_role': 'admin'}

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = overrde_get_current_user

client = TestClient(app)

#---write test below-----

@pytest.fixture
def test_todo():
    todo = Todos(
        title="learn to code!",
        description="Need to learn everything",
        priority=5,
        complete=False,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection: 
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()



def test_read_all_authenticated(test_todo):
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "complete": False, 
        "title": "learn to code!", 
        "description": "Need to learn everything",
        "id": 1,
        "priority": 5,
        "owner_id": 1,

    }]


#Read on todo test
def test_read_one_authenticated(test_todo):
    response = client.get("/todos/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "complete": False, 
        "title": "learn to code!", 
        "description": "Need to learn everything",
        "id": 1,
        "priority": 5,
        "owner_id": 1,

    }   

#Test if todo does not exist!
def test_read_one_authenticated_not_found():
         response = client.get('/todos/todo/999')
         assert response.status_code == 404
         assert response.json() == {'detail': 'Todo not found!'}



#------test creating a new todo-------
def test_create_todo(test_todo):
     request_data={
          'title': 'New todo!',
          'description': 'New todo description',
          'priority': 5,
          'complete': False,
     }         

     response = client.post('/todos/todo/', json=request_data)
     assert response.status_code == 201
     db = TestingSessionLocal()
     model = db.query(Todos).filter(Todos.id == 2).first()
     assert model.title == request_data.get('title')
     assert model.description == request_data.get('description')
     assert model.priority == request_data.get('priority')
     assert model.complete == request_data.get('complete')


#test update
def test_update_todo(test_todo):
     request_data = {
          'title': 'change the title of the todo.',
          'description': 'Need to learn everyday',
          'priority': 5,
          'complete': False
     }     

     response = client.put('/todos/todo/1', json=request_data)
     assert response.status_code == 204
     db = TestingSessionLocal()
     model = db.query(Todos).filter(Todos.id == 1).first()
     assert model.title == 'change the title of the todo.'



