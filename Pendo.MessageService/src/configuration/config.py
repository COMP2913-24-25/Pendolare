from pydantic import BaseModel, Field

class DbConfiguration(BaseModel):
    """
    DbConfiguration class is a configuration object for database connection.
    """
    dbServer: str = "localhost:1433"
    dbDatabase: str = "Pendo.Database"
    dbUsername: str = "SA" 
    dbPassword: str = "reallyStrongPwd123"
    Provider: str = Field(None)
    Host: str = Field(None) 
    Port: int = Field(None)
    Database: str = Field(None)
    Username: str = Field(None)
    Password: str = Field(None)

    def getDbUrl(self) -> str: 
        """
        getDbUrl method returns the database connection string.
        :return: Database connection string.
        """
        # If Provider is set, use the SQLite format
        if self.Provider and self.Provider.lower() == "sqlite":
            return f"sqlite:///{self.Database}"
        
        # Otherwise use the SQL Server format
        return f"mssql+pymssql://{self.dbUsername}:{self.dbPassword}@{self.dbServer}/{self.dbDatabase}"
    
class SendGridConfiguration(BaseModel):
    """
    SendGridConfiguration class is a configuration object for SendGrid.
    """
    apiKey: str
    fromEmail: str
    pendingTemplateId: str
    confirmedTemplateId: str
    cancelledTemplateId: str

class StripeConfiguration(BaseModel):
    """
    StripeConfiguration class is used for the Stripe API keys, wrapped in an object.
    """
    secret: str
    publishable: str