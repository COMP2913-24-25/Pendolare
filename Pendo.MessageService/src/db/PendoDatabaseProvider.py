from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os
import logging
from dotenv import load_dotenv, find_dotenv
import json

# Setup logging
logger = logging.getLogger(__name__)

env_path = find_dotenv('../configuration/.env')
load_dotenv(env_path)

# Create base
Base = declarative_base()

engine = None
SessionLocal = None

def _initialise_database():
    """Initialise the database engine and session factory."""
    global engine, SessionLocal

    # Check environment variables inside the function
    environment = os.getenv("ENV", "Production")
    use_database = os.getenv("USE_DATABASE", "true").lower() == "true"

    if use_database:
        try:
            # Determine config path and handle Docker environments
            if environment == "Testing":
                logger.info("Testing mode detected, using in-memory SQLite database")
                connection_string = "sqlite:///:memory:"
            else:
                # Try to load from config file
                try:
                    from ..configuration.configProvider import ConfigurationProvider
                    
                    configPath = f"/app/src/configuration/appsettings.{environment}.json"
                    # Check for alternate paths if running locally
                    if not os.path.exists(configPath):
                        alternate_paths = [
                            f"src/configuration/appsettings.{environment}.json",
                            f"../src/configuration/appsettings.{environment}.json",
                            f"configuration/appsettings.{environment}.json"
                        ]
                        for path in alternate_paths:
                            if os.path.exists(path):
                                configPath = path
                                break
                    
                    if os.path.exists(configPath):
                        logger.info(f"Loading database config from {configPath}")
                        configProvider = ConfigurationProvider(configPath)
                        connection_string = configProvider.database.getDbUrl()
                    else:
                        # Fallback to environment variables or defaults
                        logger.warning(f"Config file {configPath} not found. Checking for environment variables.")
                        db_server = os.getenv("DB_SERVER", "localhost:1433")
                        db_name = os.getenv("DB_NAME", "Pendo.Database")
                        db_user = os.getenv("DB_USER", "SA")
                        db_password = os.getenv("DB_PASSWORD", "reallyStrongPwd123")
                        connection_string = f"mssql+pymssql://{db_user}:{db_password}@{db_server}/{db_name}"
                except Exception as e:
                    logger.error(f"Error loading configuration: {str(e)}")
                    # Fallback to SQLite for safety
                    connection_string = "sqlite:///:memory:"

            # Create engine with connection string
            logger.info(f"Initialising database connection type: {connection_string.split('://')[0]}")
            engine = create_engine(connection_string)
            SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
            
        except Exception as e:
            logger.error(f"Database initialisation error: {str(e)}")
            # Fallback to in-memory SQLite if initialisation fails
            logger.warning("Falling back to in-memory SQLite due to initialisation error.")
            connection_string = "sqlite:///:memory:"
            engine = create_engine(connection_string)
            SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    else:
        # If database is disabled, use in-memory SQLite
        logger.info("Database usage is disabled. Initialising in-memory SQLite.")
        engine = create_engine("sqlite:///:memory:")
        SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Dependency to get DB session
def get_db():
    """Provides a database session. Initialises the engine and factory if not already done."""
    global engine, SessionLocal

    # Initialise only if engine is not already created
    if engine is None:
        _initialise_database()

    # If SessionLocal is still None after initialisation attempt (e.g., error), handle it
    if SessionLocal is None:
        logger.error("SessionLocal could not be initialised. Returning mock session.")
        from unittest.mock import MagicMock
        mock_session = MagicMock(spec=Session)
        # Configure mock session methods if needed for basic functionality
        mock_session.query.return_value = mock_session
        mock_session.filter.return_value = mock_session
        mock_session.get.return_value = None
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.rollback.return_value = None
        mock_session.close.return_value = None
        yield mock_session
        return
        
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()