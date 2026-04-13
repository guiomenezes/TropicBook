from fastapi import FastAPI
from app.routers import guests, rooms, reservations, payments, reports
from app.routers import auth
from app import models
from app.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='TropicBook_API')

app.include_router(guests.router)
app.include_router(rooms.router)
app.include_router(reservations.router)
app.include_router(payments.router)
app.include_router(reports.router)
app.include_router(auth.router)

@app.get('/')
def home():
    return {'message': 'Hostel API Funcionando.'}