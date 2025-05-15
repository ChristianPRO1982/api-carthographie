from fastapi import FastAPI
from app.db import get_connection

app = FastAPI()

@app.get("/data")
def get_data():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM your_table_name LIMIT 100")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
