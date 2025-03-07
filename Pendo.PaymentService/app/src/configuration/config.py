from pydantic import BaseModel

class DbConfiguration(BaseModel):
    """
    DbConfiguration class is a configuration object for database connection.
    """
    dbServer : str
    dbDatabase : str
    dbUsername : str
    dbPassword : str

    def getDbUrl(self) -> str: 
        """
        getDbUrl method returns the database connection string.
        :return: Database connection string.
        """
        return f"mssql+pymssql://{self.dbUsername}:{self.dbPassword}@{self.dbServer}/{self.dbDatabase}"
    
class SendGridConfiguration(BaseModel):
    """
    SendGridConfiguration class is a configuration object for SendGrid.
    """
    apiKey : str
    fromEmail : str
    pendingTemplateId : str
    confirmedTemplateId : str
    cancelledTemplateId : str

class StripeConfiguration(BaseModel):
    """
    StripeConfiguration class is used for the Stripe API keys, wrapped in an object.
    """
    secret: str
    publishable: str 