from fastapi import FastAPI, Request
import models
from database import engine
from routers import auth, todos, admin, users
from fastapi.templating import Jinja2Templates
from pathlib import Path


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


BASE_DIR = Path(__file__).resolve().parent 
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get('/')
def test(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


#Health check
@app.get('/healthy')
def health_check():
    return {'status': 'Healthy'}



app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
