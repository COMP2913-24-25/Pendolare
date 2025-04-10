from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os
import logging
from dotenv import load_dotenv, find_dotenv

# Setup logging
logger = logging.getLogger(__name__)

# Load environment variables
env_path = find_dotenv('../configuration/.env')
load_dotenv(env_path)
environment = os.getenv("ENV", "Production")
use_database = os.getenv("USE_DATABASE", "true").lower() == "true"

# Create session factory and base
Base = declarative_base()
SessionLocal = None
engine = None

# Only initialise database if USE_DATABASE is true
if use_database:
    try:
        # Import here to avoid circular imports
        import json
        import os.path
        
        # Determine config path and handle Docker environments
        if environment == "Testing":
            # In testing mode, always use in-memory SQLite
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
                
                # Check if the file exists, use default connection string if not
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
        logger.info(f"Using database connection type: {connection_string.split('://')[0]}")
        engine = create_engine(connection_string)
        SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
        
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")
        # Fallback to in-memory SQLite for testing
        connection_string = "sqlite:///:memory:"
        engine = create_engine(connection_string)
        SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
else:
    # If database is disabled, use in-memory SQLite
    logger.info("Database usage is disabled. Using in-memory SQLite for test compatibility.")
    engine = create_engine("sqlite:///:memory:")
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Dependency to get DB session
def get_db():
    if SessionLocal is None:
        # Return a mock session if database is not initialised
        from unittest.mock import MagicMock
        mock_session = MagicMock(spec=Session)
        yield mock_session
        return
        
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()