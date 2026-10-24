import logging
import os

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

APP_VERSION = "1.0.0"
APP_NAME = os.getenv("APP_NAME", "Каталог русской классики")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    docs_url="/docs",
)

@app.middleware("http")
async def add_json_charset(request: Request, call_next):
    response = await call_next(request)

    if response.headers.get("content-type", "").startswith("application/json"):
        response.headers["content-type"] = "application/json; charset=utf-8"

    return response

class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int


books = [
    Book(
        id=1,
        title="Война и мир",
        author="Лев Толстой",
        year=1869,
    ),
    Book(
        id=2,
        title="Преступление и наказание",
        author="Фёдор Достоевский",
        year=1866,
    ),
    Book(
        id=3,
        title="Евгений Онегин",
        author="Александр Пушкин",
        year=1833,
    ),
    Book(
        id=4,
        title="Мёртвые души",
        author="Николай Гоголь",
        year=1842,
    ),
    Book(
        id=5,
        title="Отцы и дети",
        author="Иван Тургенев",
        year=1862,
    ),
    Book(
        id=6,
        title="Вишнёвый сад",
        author="Антон Чехов",
        year=1904,
    ),
]


@app.on_event("startup")
async def startup_event():
    logger.info("%s, версия %s: приложение запущено", APP_NAME, APP_VERSION)


@app.get("/")
def root():
    return {
        "message": "Добро пожаловать в каталог русской классики!",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/version")
def version():
    return {
        "app": APP_NAME,
        "version": APP_VERSION,
    }


@app.get("/books")
def list_books():
    logger.info("Запрошен полный каталог произведений")
    return {
        "count": len(books),
        "books": [
            book.model_dump(mode="json")
            for book in books
        ],
    }



@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            logger.info("Запрошено произведение с ID %s", book_id)
            return book
            
    logger.warning("Произведение с ID %s не найдено", book_id)
    raise HTTPException(
        status_code=404,
        detail="Произведение не найдено",
    )

@app.get("/books/search/{author}")
def search_books(author: str):
    results = [
        book
        for book in books
        if author.casefold() in book.author.casefold()
    ]

    logger.info(
        "Поиск произведений по автору '%s': найдено %s",
        author,
        len(results),
    )
    return results

