from fastapi import FastAPI
import sqlite3

app = FastAPI()

DB_PATH = "students.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/students/gpafrom/{start_gpa}")
def students_by_gpa(start_gpa: float):
    """Returns number and names of students whose GPA >= start_gpa."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM Students WHERE gpa >= ?", (start_gpa,))
    rows = cur.fetchall()
    conn.close()
    names = [row["name"] for row in rows]
    return {"number": len(names), "names": names}


@app.get("/students/startyear/{year}")
def students_by_start_year(year: int):
    """Returns number and names of students whose start year == year."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM Students WHERE start_year = ?", (year,))
    rows = cur.fetchall()
    conn.close()
    names = [row["name"] for row in rows]
    return {"start_year": year, "number": len(names), "names": names}


@app.get("/students/yearrange/")
def students_by_year_range(from_year: int, to_year: int):
    """Returns number and names of students whose start year is between from_year and to_year (inclusive)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT name FROM Students WHERE start_year >= ? AND start_year <= ?",
        (from_year, to_year),
    )
    rows = cur.fetchall()
    conn.close()
    names = [row["name"] for row in rows]
    return {"number": len(names), "names": names}
