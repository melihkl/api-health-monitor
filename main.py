from typing import Optional

from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.staticfiles import StaticFiles

from app import crud, services
from app.db import Base, engine, get_db

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Veritabanı oluşturulması
Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")


# Ana sayfa
@app.get("/", response_class=HTMLResponse)
async def form_view(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


# API Ekleme
@app.post("/submit")
async def submit_form(name: str = Form(...), url: str = Form(...), method: str = Form(...),
                      params: Optional[str] = Form(None), db: Session = Depends(get_db)):
    api_data = {"name": name, "url": url, "method": method, "params": params}
    crud.create_api(db=db, api_data=api_data)
    return {"message": "API data saved successfully!"}


# API Health Check Listeleme
@app.get("/list")
def list_apis(request: Request, db: Session = Depends(get_db)):
    apis = crud.get_apis(db)
    health_results = [services.check_health(api.__dict__) for api in apis]
    return templates.TemplateResponse("index.html", {"request": request, "apis_health": health_results})