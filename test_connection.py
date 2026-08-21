from database import engine
from sqlalchemy import text
connection = engine.connect()
print("connection successful")
result = connection.execute(text("SELECT * FROM JOBS WHERE job_id != 3;"))
for row in result:
    print(row)
print('completed all the tasks now closing the connection')
connection.close()
