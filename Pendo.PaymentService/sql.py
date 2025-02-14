import io
import sys
from sqlalchemy import create_engine, MetaData
from sqlacodegen.codegen import CodeGenerator

def generate_model(host, user, password, database, outfile = None):
    engine = create_engine(f'mssql+pymssql://{user}:{password}@{host}/{database}')
    metadata = MetaData(bind=engine)
    metadata.reflect()
    outfile = io.open(outfile, 'w', encoding='utf-8') if outfile else sys.stdout
    generator = CodeGenerator(metadata)
    generator.schema = 'payment'
    generator.render(outfile)

generate_model("localhost:1433", "SA", "reallyStrongPwd123", "Pendo.Database", outfile='test.py')