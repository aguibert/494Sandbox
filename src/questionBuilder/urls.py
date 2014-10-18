import views


def setup_urls(app):
    app.add_url_rule('/questionBuilder', view_func=views.QuestionBuilderView.as_view('questionBuilder'))
    app.add_url_rule('/quizBuilder', view_func=views.QuizBuilderView.as_view('quizBuilder'))
