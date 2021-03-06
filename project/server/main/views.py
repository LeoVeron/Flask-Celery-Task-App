# project/server/main/views.py


from flask import render_template, Blueprint, jsonify, request
from project.server.tasks import create_task
from celery.result import AsyncResult
from project.server import db
from project.database import Matche

main_blueprint = Blueprint("main", __name__,)


@main_blueprint.route("/", methods=["GET"])
def home():
    return render_template("main/home.html", matches=Matche.query.all())

@main_blueprint.route("/tasks", methods=["POST"])
def run_task():
    content = request.json
    match_id = content["id"]
    task = create_task.delay(int(match_id))
    return jsonify({"task_id": task.id}), 202
    # return jsonify({"match_name": task.match_name, "restime": task.restime, "prediction": task.prediction}), 202


@main_blueprint.route("/tasks/<task_id>", methods=["GET"])
def get_status(task_id):
    task_result = AsyncResult(task_id)
    res = task_result.result
    if res :
        result = {
            "task_id": task_id,
            "task_status": task_result.status,
            "match_name": res[0],
            "restime": res[1],
            "prediction": res[2]
        }
    else:
        result = {
            "task_id": task_id,
            "task_status": task_result.status,
            "match_name": 0,
            "restime": 0,
            "prediction": 0
        }
    return jsonify(result), 200
