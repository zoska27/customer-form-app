from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from pathlib import Path
import re

app = FastAPI()
templates = Jinja2Templates(directory="templates")

EXCEL_FILE = "customers.xlsx"
GEORGIAN_REGEX = r"^[ა-ჰ]+$"

@app.get("/", response_class=HTMLResponse)
def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit")
def submit_data(customer_id: str = Form(...), name: str = Form(...), surname: str = Form(...)):
    # Validate ID
    if len(customer_id) != 11 or not customer_id.isdigit():
        raise HTTPException(status_code=400, detail="ID must be exactly 11 digits.")
    # Validate name and surname in Georgian
    if not re.fullmatch(GEORGIAN_REGEX, name):
        raise HTTPException(status_code=400, detail="Name must be in Georgian.")
    if not re.fullmatch(GEORGIAN_REGEX, surname):
        raise HTTPException(status_code=400, detail="Surname must be in Georgian.")

    # Save to Excel
    new_row = pd.DataFrame([[customer_id, name, surname]], columns=["ID", "Name", "Surname"])
    path = Path(EXCEL_FILE)
    if path.exists():
        df = pd.read_excel(path)
        df = pd.concat([df, new_row], ignore_index=True)
    else:
        df = new_row
    df.to_excel(EXCEL_FILE, index=False)
    return RedirectResponse("/", status_code=303)

@app.get("/download/customers.xlsx")
def download_excel():
    return FileResponse(
        path=EXCEL_FILE,
        filename="customers.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
