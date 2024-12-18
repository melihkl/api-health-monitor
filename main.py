import json
from typing import Optional

from fastapi import FastAPI, Form, Request, Depends, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.staticfiles import StaticFiles

from app import crud, services, schemas
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
                      params: Optional[str] = Form(None),
                      cookie: Optional[str] = Form(None),
                      db: Session = Depends(get_db)):
    api_data = {"name": name, "url": url, "method": method, "params": params, "cookie": cookie}
    crud.create_api(db=db, api_data=api_data)
    return {"message": "API data saved successfully!"}

# JSON File ile API Ekleme


@app.post("/fileSubmit/")
async def submit_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    try:
        json_data = json.loads(content.decode('utf-8'))
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Geçersiz json")

    for api in json_data.get("apis", []):
        api_data = {
            "name": api["name"],
            "url": api["url"],
            "method": api["method"],
            "params": api.get("params"),
            "cookie": api.get("cookie")
        }
        print(api_data)
        crud.create_api(db=db, api_data=api_data)

    return {"message": "File saved successfully!"}


@app.post("/api/add/")
def add_new_api(api: schemas.APICreate, db: Session = Depends(get_db)):
    try:
        new_api = crud.create_api(db=db, api_data=api.dict())
        return new_api
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occured: {str(e)}")


# API Health Check Listeleme
@app.get("/list")
def list_apis(request: Request, db: Session = Depends(get_db)):
    apis = crud.get_apis(db)
    return templates.TemplateResponse("index.html", {"request": request, "apis_health": apis})


@app.get("/openList")
def open_list(request: Request, db: Session = Depends(get_db)):
    apis = crud.get_apis(db)
    health_results = [services.check_health(api.__dict__) for api in apis]
    return templates.TemplateResponse("index.html", {"request": request, "apis_health": health_results})
