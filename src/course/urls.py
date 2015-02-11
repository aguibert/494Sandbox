import views


def setup_urls(app):
    app.add_url_rule('/course/create', view_func=views.CreateView.as_view('create_course'))
    app.add_url_rule('/course/view/<courseID>', view_func=views.CourseMasterView.as_view('view_course'))
    app.add_url_rule('/home/coursetasklist/<courseID>', view_func=views.CourseTaskListView.as_view('course_task_list'))
