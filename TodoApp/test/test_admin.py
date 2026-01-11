from .utils import *
from ..routers.admin import get_current_user, get_db
from fastapi import status
from ..models import Todos

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = make_override_get_user

def test_admin_read_all_authenticated(test_todo):

    db, todo, user = test_todo

    response = client.get('/admin/todo')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"title" : "Learn to code!",
                                "description" : "Need to learn everyday!",
                                "complete" : False,
                                "priority" : 5,
                                "owner_id" : todo.owner_id,
                                "id" : todo.id
                                }]
    

def test_delete_admin_todo(test_todo):
    db, todo, user = test_todo
    response = client.delete(f'/admin/todo/{todo.id}')
    assert response.status_code == 204

    db.close()
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == todo.id).first()
    assert model is None


def test_delete_admin_todo_not_found(test_todo):
    db, todo, user = test_todo
    response = client.delete(f'/admin/todo/9999')
    assert response.status_code == 404

    db.close()
    db = TestingSessionLocal()
    assert response.json() == {'detail': 'Todo not found.'}