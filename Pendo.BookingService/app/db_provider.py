from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from .configuration_provider import ConfigurationProvider, Path
from dotenv import load_dotenv
import os

load_dotenv()
environment = os.getenv("ENV", "Production")
configPath = f"{Path(__file__).resolve().parent}/appsettings.{environment}.json"
configProvider = ConfigurationProvider(configPath)

engine = create_engine(configProvider.database.getDbUrl())
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()