from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
#from .configuration_provider import ConfigurationProvider, Path
from dotenv import load_dotenv
import os
#from .configuration_provider import ConfigurationProvider, Path
'''
load_dotenv()
environment = os.getenv("ENV", "Production")
configPath = f"{Path(__file__).resolve().parent}/appsettings.{environment}.json"
configProvider = ConfigurationProvider(configPath)

engine = create_engine(configProvider.database.getDbUrl())
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# MSSQL Database Configuration
DATABASE_URL = "mssql+pymssql://SA:reallyStrongPwd123@localhost:1433/Pendo.Database"

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the base class for ORM models
Base = declarative_base()

# Create tables
Base.metadata.create_all(bind=engine)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()