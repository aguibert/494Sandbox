import flask
from flask import redirect
from flask import render_template
from flask import url_for
from flask.views import MethodView
import flask_login
from flask_login import current_user
from flask_login import login_required
import json

from auth import auth
import grading
import models


class ResponseView(MethodView):
    decorators = [login_required]

    def get(self, responseID):
        grader = grading.Grader()
        grader.grade_automatic_questions(responseID)
        grader.grade_supplementary_material(responseID)
        task_response = models.TaskResponse.query.filter_by(id=responseID).first()
        formatted_time = task_response.datetime.strftime("%a %b %d %H:%M:%S")
        response = json.loads(task_response.graded_response)
        supplementary = json.loads(task_response.graded_supplementary)

        return render_template("grading/response.html", response=response,
                               student=task_response.user, task=task_response.task,
                               task_response=task_response, time=formatted_time,
                               supplementary=supplementary,
                               permissions=current_user.permissions)


class ManualGradingView(MethodView):
    decorators = [login_required, auth.permissions_author]

    # TODO come back and verify that the user has permission to do this

    def post(self):
        data = flask.request.get_json()
        response_id = data['response_id'].split('?')[0]
        grader = grading.Grader()
        correctness = grader.grade_manual_question(response_id,
                                                   data['question_id'],
                                                   data['correct'])
        return json.dumps(correctness)


class ManualFeedbackGradingView(MethodView):
    decorators = [login_required, auth.permissions_author]
    # TODO come back and verify that the user has permission to do this

    def post(self):
        data = flask.request.get_json()
        response_id = data['response_id'].split('?')[0]
        grader = grading.Grader()
        grader.grade_manual_question(response_id,
                                     data['question_id'],
                                     data['feedback'],
                                     category="feedback")
        models.db.session.commit()
        return ""


class ManualCriticalGradingView(MethodView):
    decorators = [login_required, auth.permissions_author]
    # TODO come back and verify that the user has permission to do this

    def post(self):
        data = flask.request.get_json()
        response_id = data['response_id'].split('?')[0]
        grader = grading.Grader()
        grader.grade_manual_question(response_id,
                                     data['question_id'],
                                     data['critical'],
                                     category="critical")
        models.db.session.commit()
        return ""