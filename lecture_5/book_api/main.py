from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlitedb.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Base class for SQLAlchemy
Base = declarative_base()

# Factory for creating database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



class Book(Base):
    """
    SQLAlchemy model representing the 'books' table in the database.
    """
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    year = Column(Integer, nullable=True)


Base.metadata.create_all(bind=engine)



def get_db():
    """
    Dependency function to get and close the database session.
    It yields the database session object, which is automatically closed
    by the 'finally' block when the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



class BookBase(BaseModel):
    """
    Base schema for common book attributes.
    """
    title: str
    author: str
    year: Optional[int] = None


class BookCreate(BookBase):
    """
    Schema for incoming data used to create a new book
    """
    pass


class BookResponse(BookBase):
    """
    Schema for outgoing responses, includes the generated ID.
    """
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )



app = FastAPI()



@app.get("/")
def read_root():
    """
    Root endpoint for a welcoming message.
    """
    return {"message": "Welcome to the Book catalog API!"}


@app.post("/books/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    Creates a new book entry in the database.

    Arguments:
        book: The book data validated by the BookCreate schema.
        db: The database session dependency.

    Returns:
        The created book object, with its new ID.
    """
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.get("/books/", response_model=List[BookResponse])
def read_books(db: Session = Depends(get_db)):
    """
    Retrieves a list of all books from the database.

    Arguments:
        db: The database session dependency.

    Returns:
        A list of BookResponse objects.
    """
    return db.query(Book).all()


@app.get("/books/{book_id}", response_model=BookResponse)
def read_book(book_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a single book by its ID.

    Arguments:
        book_id: The ID of the book to retrieve.
        db: The database session dependency.

    Raise:
        HTTPException: 404 Not Found if the book ID does not exist.

    Returns:
        The requested BookResponse object.
    """
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return db_book


@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int, updated_book: BookCreate, db: Session = Depends(get_db)
):
    """
    Updates an existing book entry by ID.

    Arguments:
        book_id: The ID of the book to update.
        updated_book: The new data for the book.
        db: The database session dependency.

    Raises:
        HTTPException: 404 Not Found if the book ID does not exist.

    Returns:
        The updated BookResponse object.
    """
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in updated_book.model_dump(exclude_unset=True).items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Deletes a book entry by its ID.

    Arguments:
        book_id: The ID of the book to delete.
        db: The database session dependency.

    Raise:
        HTTPException: 404 Not Found if the book ID does not exist.
    """
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(db_book)
    db.commit()
    return


@app.get("/books/search/", response_model=List[BookResponse])
def search_books(query: str, db: Session = Depends(get_db)):
    """
    Searches for books by title or author using a partial match (LIKE).

    Arguments:
        query: The search term provided as a query parameter.
        db: The database session dependency.

    Returns:
        A list of matching BookResponse objects.
    """
    search_pattern = f"%{query}%"

    results = db.query(Book).filter(
        (Book.title.like(search_pattern))
        | (Book.author.like(search_pattern))
    ).all()
    return results


