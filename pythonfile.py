import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="pharmacy_db"
    )


from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from db import get_connection
import datetime

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Patient(BaseModel):
    name: str
    date: str
    priority: int  # 1 is highest, larger number = lower priority

@app.post("/add_patient/")
def add_patient(patient: Patient):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO patients (name, date, priority)
        VALUES (%s, %s, %s)
    """, (patient.name, patient.date, patient.priority))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Patient added"}

@app.get("/patients/{date}")
def get_patients(date: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM patients WHERE date = %s
        ORDER BY priority ASC, id ASC
    """, (date,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

@app.delete("/remove_fifo/{date}")
def remove_fifo(date: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM patients WHERE date = %s
        ORDER BY id ASC LIMIT 1
    """, (date,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Removed first patient (FIFO)"}

@app.delete("/remove_by_name/{name}")
def remove_by_name(name: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE name = %s", (name,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": f"Removed {name}"}

