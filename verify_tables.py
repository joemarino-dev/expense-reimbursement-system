from sqlalchemy import inspect
from app.database import engine

inspector = inspect(engine)
tables = inspector.get_table_names()

print('Tables in database:')
for table in tables:
	print(f" ✅ {table}")
	columns = inspector.get_columns(table)
	for column in columns: 
		print(f" - {column['name']}, ({column['type']})")
