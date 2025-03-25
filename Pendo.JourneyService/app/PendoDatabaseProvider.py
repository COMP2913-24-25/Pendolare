from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from .configuration.configProvider import ConfigurationProvider, Path
from dotenv import load_dotenv, find_dotenv
import os

env_path = find_dotenv('./configuration/.env')
load_dotenv(env_path)
environment = os.getenv("ENV", "Production")

configPath = f"/code/app/configuration/appsettings.{environment}.json"
configProvider = ConfigurationProvider(configPath)

engine = create_engine(configProvider.database.getDbUrl())
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()