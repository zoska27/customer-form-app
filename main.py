from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
import re
import psycopg2

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# DB connection
conn = psycopg2.connect(
    dbname="customer_data",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Georgian letter regex (Unicode range for Georgian letters)
GEORGIAN_REGEX = r"^[ა-ჰ]+$"

@app.get("/", response_class=HTMLResponse)
def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/submit")
def submit_data(customer_id: str = Form(...), name: str = Form(...), surname: str = Form(...)):
    # Validate ID length
    if len(customer_id) != 11 or not customer_id.isdigit():
        raise HTTPException(status_code=400, detail="ID must be exactly 11 digits.")

    # Validate name and surname are Georgian
    if not re.fullmatch(GEORGIAN_REGEX, name):
        raise HTTPException(status_code=400, detail="Name must be in Georgian.")
    if not re.fullmatch(GEORGIAN_REGEX, surname):
        raise HTTPException(status_code=400, detail="Surname must be in Georgian.")

    # Insert into DB
    cursor.execute(
        "INSERT INTO submissions (customer_id, name, surname) VALUES (%s, %s, %s)",
        (customer_id, name, surname)
    )
    conn.commit()

    return RedirectResponse("/", status_code=303)
