from fastapi import FastAPI
from database.models import database as connection, User, Book, Author, Loan, BookAuthor
from security import auth
from application import books

app = FastAPI(
    title="API de servicios bibliotecario",
    description="API de servicios bibliotecario",
    summary="API de servicios bibliotecario",
    version="1.0.0",
)

@app.on_event("startup")
def starup():
    if connection.is_closed():
        connection.connect()
        print('Se conecto a la base de datos')

    connection.create_tables([User, Book, Author, Loan, BookAuthor])

app.include_router(auth.router)
app.include_router(books.router)



