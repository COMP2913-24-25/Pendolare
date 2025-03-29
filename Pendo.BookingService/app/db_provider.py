from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from .configuration_provider import ConfigurationProvider, Path
from dotenv import load_dotenv
import os

load_dotenv()
environment = os.getenv("ENV", "Production")
configPath = f"{Path(__file__).resolve().parent}/appsettings.{environment}.json"
configProvider = ConfigurationProvider(configPath)

# value -1 means no limit - see https://docs.sqlalchemy.org/en/20/errors.html#error-3o7r
engine = create_engine(configProvider.database.getDbUrl(), pool_size=20, max_overflow=-1)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()