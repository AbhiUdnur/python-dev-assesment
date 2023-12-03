# importing required libraries/packages

from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from io import BytesIO # used for converting binary data into pandas framework friendly format
import pandas as pd
import sqlite3
import time    # used for delaying time  so that we ca return back to //return templates.TemplateResponse("index.html", {"request": request})// after the pop of success.

app = FastAPI()

# connects to HTML/jinja templates
templates = Jinja2Templates(directory="templates")   

# Connect to SQLite database
conn = sqlite3.connect("data.db")

# create data table if not have the one
conn.execute("""CREATE TABLE IF NOT EXISTS data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT,
    Age TEXT
)""")

# connection for executing SQL queries.
cursor = conn.cursor()

# create a base/home page
@app.get("/", response_class=HTMLResponse)

async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# all process post the upload of csv
@app.post("/upload_csv")

async def upload_csv(request: Request, csv_file: UploadFile = File(...)):

    # Read CSV data into a Pandas DataFrame
    csv_data = await csv_file.read()
    df = pd.read_csv(BytesIO(csv_data))

    # Save CSV data to SQLite database
    df.to_sql("data", conn, if_exists="append", index=False)

    time.sleep(2)   # delay for lating success msg popup to appear 

    return templates.TemplateResponse("index.html", {"request": request})

# all process post requesting to acess data
@app.get("/visualize_data", response_class=HTMLResponse)
async def visualize_data(request: Request):

    cursor.execute("""SELECT * FROM data""")
    results = cursor.fetchall()
    # print(results)
    return templates.TemplateResponse("visualize_data.html", {"request": request,"results": results})


