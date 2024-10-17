import requests


def check_health(api):
    method = api.get('method', 'GET').upper()  # Varsayılan GET
    url = api['url']

    params = api.get('params', {})
    if isinstance(params, str):
        params = {}

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
            return {"name": api['name'], "status_code": "Unsupported", "health": "Unsupported method"}

        if 200 <= response.status_code < 300:
            return {"name": api['name'], "status_code": response.status_code, "health": "UP"}
        else:
            return {"name": api['name'], "status_code": response.status_code, "health": "DOWN"}

    except requests.exceptions.RequestException as e:
        return {"name": api['name'], "status_code": "Error", "health": f"DOWN (Error: {str(e)})"}
