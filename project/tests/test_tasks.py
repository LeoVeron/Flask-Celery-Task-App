from project.server.tasks import create_task
from unittest.mock import patch, call
import json

def test_home(test_app):
    client = test_app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200

@patch("project.server.tasks.create_task.run")
def test_mock_task(mock_run):
    assert create_task.run(1)
    create_task.run.assert_called_once_with(1)

    assert create_task.run(2)
    assert create_task.run.call_count == 2

    assert create_task.run(3)
    assert create_task.run.call_count == 3
    
def test_task_status(test_app):
    client = test_app.test_client()

    resp = client.post(
        "/tasks",
        data=json.dumps({"id": 1}),
        content_type='application/json'
    )
    content = json.loads(resp.data.decode())
    task_id = content["task_id"]
    assert resp.status_code == 202
    assert task_id

    resp = client.get(f"tasks/{task_id}")
    content = json.loads(resp.data.decode())
    assert content == {
            "task_id": task_id,
            "task_status": "PENDING", 
            "match_name": 0,
            "restime": 0,
            "prediction": 0
            }
    assert resp.status_code == 200

    while content["task_status"] == "PENDING":
        resp = client.get(f"tasks/{task_id}")
        content = json.loads(resp.data.decode())
    assert content["task_id"]==task_id
    assert content["task_status"]=="SUCCESS"
    assert content["match_name"]!=0
    assert content["restime"]!=0
    assert content["prediction"]!=0