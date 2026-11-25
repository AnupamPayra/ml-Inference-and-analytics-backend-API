from sqlmodel import SQLModel, create_engine, Session, dat

DATABASEURL = "sqlite:///database.db"

engine = create_engine(DATABASEURL, echo=True)

def create_table():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
    