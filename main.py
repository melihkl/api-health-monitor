from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import yaml
import requests
from typing import Optional
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# YAML okuma ve yazma fonksiyonları
def read_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def write_to_yaml(file_path, data):
    with open(file_path, 'w') as file:
        yaml.dump(data, file)


# API health durumunu kontrol eden fonksiyon
def check_health(api):
    method = api.get('method', 'GET').upper()
    url = api['url']
    params = api.get('params', {})
    body = params.get('body', None)
    query = params.get('query', None)

    try:
        if method == 'GET':
            response = requests.get(url, params=query, verify=False)
        elif method == 'POST':
            response = requests.post(url, json=body, verify=False)
        elif method == 'PUT':
            response = requests.put(url, json=body, verify=False)
        elif method == 'DELETE':
            response = requests.delete(url, params=query, verify=False)
        else:
            return f"{api['name']} health: Unsupported method {method}"

        if 200 <= response.status_code < 300:
            return api['name'], response.status_code, "UP"
        else:
            return api['name'], response.status_code, "DOWN"

    except requests.exceptions.RequestException as e:
        return f"{api['name']} health: DOWN (Error: {str(e)})"


# Belirli aralıklarla API health durumunu kontrol eden fonksiyon
def check_apis_health_periodically(yaml_file, output_yaml):
    apis = read_yaml(yaml_file)['apis']

    results = {'apis_health': []}
    for api in apis:
        api_name, status_code, health_status = check_health(api)
        results['apis_health'].append({
            'name': api_name,
            'status_code': status_code,
            'health': health_status
        })

    write_to_yaml(output_yaml, results)


# API formdan alınan veriyi YAML dosyasına kaydeden fonksiyon
def save_to_yaml(api_data, file_path='apis.yaml'):
    try:
        with open(file_path, 'r') as file:
            current_data = yaml.safe_load(file)
    except FileNotFoundError:
        current_data = {"apis": []}

    current_data["apis"].append(api_data)

    with open(file_path, 'w') as file:
        yaml.safe_dump(current_data, file)


# Anasayfa formunu gösteren rota
@app.get("/", response_class=HTMLResponse)
async def form_view(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


# Formdan gelen veriyi işleyip YAML dosyasına kaydeden rota
@app.post("/submit")
async def submit_form(name: str = Form(...), url: str = Form(...), method: str = Form(...),
                      params: Optional[str] = Form(None)):
    try:
        params_dict = json.loads(params) if params else {}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format for params"}

    api_data = {
        "name": name,
        "url": url,
        "method": method,
    }

    if params_dict:
        api_data["params"] = {"body": params_dict}

    save_to_yaml(api_data)

    return {"message": "API data saved successfully!"}


# Health durumunu listeleyen rota
@app.get("/list")
def list(request: Request, yaml_file="apis.yaml", output_yaml_file="api_health_results.yaml"):
    check_apis_health_periodically(yaml_file, output_yaml_file)
    yaml_data = read_yaml(output_yaml_file)
    return templates.TemplateResponse("index.html", {"request": request, "apis_health": yaml_data['apis_health']})