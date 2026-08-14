from fastapi import FastAPI
from api import books, users, loans

from database.db import create_table


app = FastAPI()
app.include_router(books.router)
app.include_router(users.router)
app.include_router(loans.router)



@app.on_event("startup")
def startup():
    create_table()


@app.get("/")
async def root():
    return {"message": "Hello World"}







