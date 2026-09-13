import os
from dotenv import load_dotenv
import pytest
import requests

load_dotenv()

@pytest.fixture(scope="session")
def token():
    token = os.getenv("USER_B_TOKEN")
    return token

@pytest.fixture
def headers(token):
    headers = {
            "Authorization": f"Token {token}"
        }
    return headers

@pytest.fixture
def invalid_headers():
    headers = {
                "Authorization": f"Token 1231231242"
            }
    return headers

@pytest.fixture
def base_url():
    base_url="http://127.0.0.1:8000"
    return base_url

@pytest.fixture
def task(headers, base_url):
    data = {
    "title": "fixture test",
    "description": "test",
    "status": "todo"
    }
    response = requests.post(
        base_url+f"/api/task/", 
        headers=headers,json=data
        )
    task = response.json()

    yield task 

    requests.delete(
        base_url+f"/api/task/{task['id']}/", 
        headers=headers
        )
    
@pytest.fixture
def delete_task(headers, base_url):
    data = {
        "title": "fixture test",
        "description": "test",
        "status": "todo"
    }
    response = requests.post(
        base_url + "/api/task/",
        headers=headers,
        json=data
    )
    delete_task = response.json()
    yield delete_task
    
#==================
#user A scenario
#====================
@pytest.fixture()
def create_user_a(base_url):
    data ={
        "username":"user_a",
        "password":f"{os.getenv('PASS_A')}"
    }
    response = requests.post(
        base_url+"/api/register/",
        json=data
    )
    return response

@pytest.fixture
def user_a_token(base_url, create_user_a):
    data ={
            "username":"user_a",
            "password":f"{os.getenv('PASS_A')}"
        }
    response = requests.post(
        base_url + "/api/token/",
        json=data
    )
    return response.json()['token']

@pytest.fixture
def user_a_headers(user_a_token):
    user_a_headers = {
        "Authorization": f"Token {user_a_token}"
    }
    return user_a_headers

@pytest.fixture
def task_a(base_url, user_a_headers):
    data = {
        "title":"task of User A",
        "description":"test for User A",
        "status":"todo"
    }
    response= requests.post(
        base_url+"/api/task/",
        headers=user_a_headers,
        json=data
        )
    task = response.json()
    
    yield task
    
    response= requests.delete(
        base_url + f"/api/task/{task['id']}/",
        headers=user_a_headers
    )

def test_api_http_patch_invalid_status(headers, base_url, task):
    data = {
        "status":"hello"
    }
    response = requests.patch(
        base_url + f"/api/task/{task['id']}/",
        headers=headers,
        json=data
        )
    response_data=response.json()
    assert response_data["status"] == data["status"]
    assert response.status_code == 400
    

    
