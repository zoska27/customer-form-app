from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from pathlib import Path

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit")
def submit_data(customer_id: str = Form(...), name: str = Form(...), surname: str = Form(...)):
    df = pd.DataFrame([[customer_id, name, surname]], columns=["ID", "Name", "Surname"])
    file_path = Path("customers.xlsx")

    if file_path.exists():
        old_df = pd.read_excel(file_path)
        df = pd.concat([old_df, df], ignore_index=True)

    df.to_excel(file_path, index=False)
    return RedirectResponse("/", status_code=303)
