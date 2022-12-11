from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create the SQLAlchemy engine
engine = create_engine("mysql://root:secret@10.1.27.156/mydata")

# Define the base class for the SQLAlchemy models
Base = declarative_base()

# Define the User model, which corresponds to the "users" table in the database
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)

# Create the tables in the database (if they don't already exist)
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Define the input and output models for the API
class UserIn(BaseModel):
    name: str

class UserOut(BaseModel):
    id: int
    name: str

# Create the FastAPI app
app = FastAPI()

# Define the API endpoint for retrieving all users
@app.get("/users")
async def get_users():
    # Query the database for all users
    users = session.query(User).all()

    # Convert the query results to a list of dictionaries
    users_dict = [user.__dict__ for user in users]

    # Return the users as a JSON response
    return JSONResponse(content=users_dict)