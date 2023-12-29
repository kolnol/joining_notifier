from sqlalchemy import create_engine

## Replace this connection string with your own
connection_string = 'sqlite:///example.db'

engine = create_engine(connection_string)
