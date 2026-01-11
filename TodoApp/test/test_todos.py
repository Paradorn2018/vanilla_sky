from fastapi import status
from ..models import Todos, Users
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = make_override_get_user

def test_read_all_authenticate(test_todo):
    db, todo, user = test_todo
    response = client.get('/todos')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"title" : "Learn to code!",
                                "description" : "Need to learn everyday!",
                                "complete" : False,
                                "priority" : 5,
                                "owner_id" : todo.owner_id,
                                "id" : todo.id
                                }]


def test_read_one_authenticate(test_todo):
    db, todo, user = test_todo
    response = client.get(f"/todos/todo/{todo.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"title" : "Learn to code!",
                                "description" : "Need to learn everyday!",
                                "complete" : False,
                                "priority" : 5,
                                "owner_id" : todo.owner_id,
                                "id" : todo.id
                                }
    

def test_read_one_authenticated_not_found(test_todo):
    db, todo, user = test_todo
    response = client.get(f"/todos/todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_create_todo(test_todo):
    request_data = {
        'title': 'New Todo',
        'description': 'New todo description',
        'priority': 5,
        'complete': False
    }

    response = client.post('/todos/todo/', json=request_data)
    assert response.status_code == 201

    data = response.json()
    todo_id = data["id"]

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == todo_id).first()

    assert model.title == request_data["title"]
    assert model.description == request_data["description"]
    assert model.priority == request_data["priority"]
    assert model.complete == request_data["complete"]


def test_update_todo(test_todo):
    
    db, todo, user = test_todo
    

    request_data = {
        'title': 'Change the title fo the todo already saved!',
        'description': 'Need to learn everyday!',
        'priority': 5,
        'complete': False
    }
    response = client.put(f"/todos/todo/{todo.id}", json=request_data)

    assert response.status_code == 204

    db.close()
    db = TestingSessionLocal()

    model = db.query(Todos).filter(Todos.id == todo.id).first()
    assert model.title == 'Change the title fo the todo already saved!'


def test_update_todo_not_found(test_todo):
    
    db, todo, user = test_todo
    

    request_data = {
        'title': 'Change the title fo the todo already saved!',
        'description': 'Need to learn everyday!',
        'priority': 5,
        'complete': False
    }
    response = client.put(f"/todos/todo/999", json=request_data)

    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}


def test_delete_todo(test_todo):

    db, todo, user = test_todo

    response = client.delete(f"todos/todo/{todo.id}")
    assert response.status_code == 204
    
    db.close()
    db = TestingSessionLocal()

    model = db.query(Todos).filter(Todos.id == todo.id).first()
    assert model is None


def test_delete_todo_not_found(test_todo):

    db, todo, user = test_todo

    response = client.delete(f"todos/todo/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}


