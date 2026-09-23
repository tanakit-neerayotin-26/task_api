import requests
from datetime import datetime
import pytest

#=========================
# Health
#=========================
def test_status():
    response = requests.get("http://127.0.0.1:8000/health/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
  
#=================
#Task GET
#================
def test_api_http_get_token_check_all(headers, base_url, task):
    response = requests.get(base_url + "/api/task/", headers=headers)
    data = response.json()
    required_keys = ["id", 
                     "title", 
                     "description",
                     "status", 
                     "priority",
                     "created_at", 
                     "updated_at"
    ]
    assert isinstance(data, list) #check the respond data is it a list or not
    assert len(data) > 0 #check if it not data[] = empty
                     
    for task in data:  #loop the task in data(list of json/dict), task is now json individual
        assert "status" in task
        status = task["status"]
        assert status in ["todo", "in_progress","done"] 

        assert isinstance(task["id"], int)

        assert "title" in task
        title = task["title"]
        assert isinstance(title,str)
        assert title.strip() != ""
        
        assert isinstance(task["description"], str)

        assert "priority" in task
        priority = task["priority"]
        assert isinstance(priority, str)
        assert priority in ["low","medium","high"]

        assert "created_at" in task
        created_at = task["created_at"]
        try:
            datetime.fromisoformat(created_at)
        except ValueError:
            assert False
        assert "updated_at" in task

        updated_at = task["updated_at"]
        try:
            datetime.fromisoformat(updated_at)
        except ValueError:
            assert False

        for key in required_keys: #loop key in required_keys then each key is "id", ...
           assert key in task # check key in task(individual json) if key("id",..) in task or not

#=================
#Task POST
#=================
def test_api_http_post_valid_status(headers, base_url):
    data = {
        "title" : "post api",
        "description" : "this is post test",
        "status": "in_progress"
    }
    respond = requests.post(base_url + "/api/task/", headers=headers, json=data)
    respond_data = respond.json()
    assert respond.status_code == 201 

    assert isinstance(respond_data["id"], int)
    assert respond_data["id"] > 0

    assert "status" in respond_data
    assert isinstance(respond_data["status"], str)
    assert respond_data["status"] in ["todo","in_progress","done"]

    assert "priority" in respond_data
    assert isinstance(respond_data["priority"], str)
    assert respond_data["priority"] in ["low", "medium", "high"]

    assert "created_at" in respond_data
    assert isinstance(respond_data["created_at"], str)
    assert datetime.fromisoformat(respond_data["created_at"])

    assert "updated_at" in respond_data
    assert isinstance(respond_data["updated_at"], str)
    assert datetime.fromisoformat(respond_data["updated_at"]) 
    
    
    for key in data:
        assert respond_data[key] == data[key]

def test_api_http_post_invalid_status(headers, base_url):
    data = {
            "title" : "post api",
            "description" : "this is post test",
            "status": "hello"
        }
    respond = requests.post(base_url + "/api/task/", headers=headers, json=data)
    respond_data = respond.json()
    assert respond.status_code == 400
    assert "status" in respond_data
    assert isinstance(respond_data["status"], list)
    assert len(respond_data["status"]) > 0
    assert isinstance(respond_data["status"][0], str)

#=========================
#CRUD test
#=========================

def test_get_task(headers, base_url, task):
    respond = requests.get(
        base_url + f"/api/task/{task['id']}/", 
        headers=headers
    )
    assert respond.status_code == 200

    data = respond.json()
    assert data['id'] == task['id']
    assert data["title"] == task["title"]
    assert data["description"] == task["description"]
    assert data["status"] == task["status"]

def test_update_task(headers, base_url, task):
    data = {
        "title":"update title"
    }
    response = requests.patch(
        base_url+f"/api/task/{task['id']}/",
        headers=headers,
        json=data
        )
    assert response.status_code==200

    updated_data = response.json()
    assert updated_data['title'] == data['title']

    response = requests.get(
        base_url+f"/api/task/{task['id']}/",
        headers=headers
    )

    assert response.status_code == 200

    actual_data = response.json()
    assert actual_data['title'] == data['title'] 

def test_delete_task(headers, base_url, delete_task):
        response = requests.delete(
            base_url + f"/api/task/{delete_task['id']}/",
            headers=headers
            )
        assert response.status_code == 204

        response = requests.get(
            base_url + f"/api/task/{delete_task['id']}/",
            headers=headers
        )
        assert response.status_code == 404

#=========================================
# Authentication
#=========================================

def test_api_http_get_data_no_token(base_url):
    response = requests.get(base_url + "/api/task/")
    assert response.status_code == 401

def test_api_http_post_unauthorized(base_url):
    data = {
        "title": "fixture test",
        "description": "test",
        "status": "todo"
    }
    response = requests.post(
        base_url + "/api/task/",
        json=data
    )
    assert response.status_code == 401

def test_api_http_patch_unauthorized(base_url, task):
    data = {
            "title": "fixture test",
            "description": "test",
            "status": "todo"
        }
    response = requests.patch(
        base_url + f"/api/task/{task['id']}/",
        json=data)
    
    assert response.status_code == 401

def test_api_http_delete_unauthorized(base_url, delete_task):
    response = requests.delete(
        base_url + f"/api/task/{delete_task['id']}/"
        )
    assert response.status_code == 401

def test_api_http_get_invalid_token(base_url, invalid_headers):
    response = requests.get(
        base_url + "/api/task/",
        headers=invalid_headers
        )
    assert response.status_code == 401

def test_api_http_post_invalid_token(base_url, invalid_headers):
    data = {
        "title": "fixture test",
        "description": "test",
        "status": "todo"
    }
    response = requests.post(
        base_url + "/api/task/",
        headers=invalid_headers,
        json=data
        )
    assert response.status_code == 401

def test_api_http_patch_invalid_token(base_url, invalid_headers, task):
    data = {
        "title": " update title",
    }
    response = requests.patch(
        base_url + f"/api/task/{task['id']}/",
        headers=invalid_headers,
        json=data
        )
    assert response.status_code == 401

def test_api_http_delete_invalid_token(base_url, invalid_headers, task):
    response = requests.delete(
        base_url + f"/api/task/{task['id']}/",
        headers=invalid_headers,
        )
    assert response.status_code == 401

#============================
#Authentication and OwnerShip
#=============================

def test_user_b_get_user_a(headers, task_a, base_url):
    response = requests.get(
        base_url + f"/api/task/{task_a['id']}/", 
        headers=headers
        )
    assert response.status_code == 404

def test_user_b_patch_user_a(headers, task_a, base_url):
    data = {
        "title": "Update user B",
    }
    response = requests.patch(
        base_url + f"/api/task/{task_a['id']}/", 
        headers=headers,
        json=data
        )
    assert response.status_code == 404

def test_user_b_delete_user_a(headers, task_a, base_url):
    response = requests.delete(
        base_url + f"/api/task/{task_a['id']}/", 
        headers=headers,
        )
    assert response.status_code == 404

#==========
#Validation
#===========

def test_api_http_post_missing_title(headers, base_url):
    data = {
        "description": "missing title",
        "status": "todo"
    }
    response = requests.post(
        base_url + f"/api/task/", 
        headers=headers,
        json=data
        )
    response_data = response.json()
    assert "title" in response_data
    assert response.status_code == 400

def test_api_http_post_invalid_priority(headers, base_url):
    data = {
         "title": "invalid priority",
         "description": "test",
         "status": "todo",
         "priority": "super_high"
        }
    response = requests.post(
            base_url + f"/api/task/", 
            headers=headers,
            json=data
            )
    response_data = response.json()
    assert "priority" in response_data
    assert response.status_code == 400

def test_api_http_post_empty_title(headers, base_url):
    data = {
       "title": "",
        "description": "test",
        "status": "todo",     
        }
    response = requests.post(
            base_url + f"/api/task/", 
            headers=headers,
            json=data
            )
    response_data = response.json()
    assert "title" in response_data
    assert response.status_code == 400

def test_api_http_post_whitespace_title(headers, base_url):
    data = {
       "title": "     ",
        "description": "test",
        "status": "todo",     
        }
    response = requests.post(
            base_url + f"/api/task/", 
            headers=headers,
            json=data
            )
    response_data = response.json()
    assert "title" in response_data
    assert response.status_code == 400
    
    
def test_api_http_post_missing_status(headers, base_url):
    data = {
       "title": "missing status",
        "description": "test"
        }
    response = requests.post(
            base_url + f"/api/task/", 
            headers=headers,
            json=data
            )
    response_data = response.json()
    try:
        assert response_data["status"] == "todo"
        assert response.status_code == 201
    finally:
        if 'id' in response_data and response.status_code == 400:
            requests.delete(
            base_url + f"/api/task/{response_data['id']}/",
            headers=headers)

def test_api_http_post_missing_priority(headers, base_url):
    data = {
       "title": "missing priority",
        "description": "test"
        }
    response = requests.post(
            base_url + f"/api/task/", 
            headers=headers,
            json=data
            )
    response_data = response.json()
    try:
        assert response_data["priority"] == "medium"
        assert response.status_code == 201
    finally:
            requests.delete(
            base_url + f"/api/task/{response_data['id']}/",
            headers=headers)

def test_api_http_patch_invalid_status(headers, base_url, task):
    data = {
        "status":"hello"
    }
    response = requests.patch(
        base_url + f"/api/task/{task['id']}/",
        headers=headers,
        json=data
        )
    response_data = response.json()
    assert "status" in response_data
    assert response.status_code == 400

@pytest.mark.parametrize("status",[
    "hello",
    "working",
    "finished"
])
def test_api_http_patch_invalid_status(headers, base_url, task, status):
    data = {
        "status":status
    }
    response = requests.patch(
        base_url + f"/api/task/{task['id']}/",
        headers=headers,
        json=data
        )
    response_data = response.json()
    assert "status" in response_data
    assert response.status_code == 400

@pytest.mark.parametrize("priority",[
    "super_high",
    "urgent",
    "123"
])
def test_api_http_patch_invalid_priority(headers, base_url, task, priority):
    data = {
        "priority":priority
    }
    response = requests.patch(
        base_url + f"/api/task/{task['id']}/",
        headers=headers,
        json=data
        )
    response_data = response.json()
    assert "priority" in response_data
    assert response.status_code == 400

def divide(a,b):
    return a/b
def test_divde_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10,0)

items = ["a", "b", "c"]
def get_item(items, index):
    return items[index]

def test_invalid_index():
    with pytest.raises(IndexError):
        get_item(items,10)