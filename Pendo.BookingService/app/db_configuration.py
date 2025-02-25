from pydantic import BaseModel

class DbConfiguration(BaseModel):
    dbServer : str = None,
    dbDatabase : str = None,
    dbUsername : str = None,
    dbPassword : str = None,

    def getDbUrl(self) -> str: 
        return f"mssql+pymssql://{self.dbUsername}:{self.dbPassword}@{self.dbServer}/{self.dbDatabase}"