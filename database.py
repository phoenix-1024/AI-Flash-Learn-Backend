from sqlalchemy import create_engine, Column, Integer, String, JSON, ForeignKey, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create an SQLite database engine
engine = create_engine('sqlite:///my_database.db')  # "echo=True" enables logging

# Enable foreign key support using a pragma statement
@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# Create a base class for our ORM models
Base = declarative_base()

# Define a model class
class Question(Base):
    __tablename__ = "questions"

    qid = Column(Integer, primary_key=True)
    # setting ondelete cascade to delete all questions if a job is deleted
    doc_id = Column(Integer, ForeignKey(Document.doc_id,ondelete="CASCADE"), nullable = False)
    question = Column(String)
    answer = Column(String)
    para = Column(String)

class Document(Base):
    __tablename__ = "documents"
    doc_id = Column(Integer, primary_key=True)
    doc_name = Column(String)
    status = Column(String)


Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)

# we need to close the db after it is used
def get_db():
    try:
        db = Session()
        yield db
    finally:
        db.close()
