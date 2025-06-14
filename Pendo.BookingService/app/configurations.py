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
    
class PaymentServiceConfiguration(BaseModel):
    """
    PaymentServiceConfiguration class is a configuration object for Payment Service.
    """
    paymentServiceUrl : str
    
class SendGridConfiguration(BaseModel):
    """
    SendGridConfiguration class is a configuration object for SendGrid.
    """
    apiKey : str
    fromEmail : str
    pendingTemplateId : str
    confirmedTemplateId : str
    cancelledTemplateId : str
    arrivalTemplateId : str