import auth

import flask
from flask import redirect
from flask import render_template
from flask import url_for
from flask.views import MethodView
import flask_login
from flask_login import current_user
from flask_login import login_required


class LoginView(MethodView):

    def get(self):
        if current_user is not None and current_user.is_authenticated():
            return redirect(url_for('home'))
        return render_template("login.html", failure=False)

    def post(self):
        email = flask.request.form.get('email')
        pw = flask.request.form.get('password')
        auth.login(email, pw)
        if current_user.is_authenticated():
            next_url = flask.request.args.get('next', url_for("home"))
            return redirect(next_url, code=302)
        return render_template("login.html", failure=True)


class LogoutView(MethodView):

    def get(self):
        flask_login.logout_user()
        return redirect(url_for("login"))