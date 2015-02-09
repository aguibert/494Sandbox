from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()

association_table = db.Table('association', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(128))
    courses = db.relationship("Course",
                              secondary=association_table,
                              backref="users")
    coursesTeaching = db.relationship('Course', backref='author',
                                      lazy='dynamic')
    name = db.Column(db.String(255))
    permissions = db.Column(db.Integer, default=1)

    def __init__(self, email, password, name, permissions=1):
        self.email = email
        self.password = password
        self.name = name
        self.permissions = permissions
        return

    def get_id(self):
        return str(self.id)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def is_admin(self):
        return True


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    title = db.Column(db.String(255))
    securityCode = db.Column(db.String(6))
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tasks = db.relationship('Task', backref='course', lazy='dynamic')

    def __init__(self, name, title,securityCode = 123456):
        self.securityCode = securityCode
        self.name = name
        self.title = title
        return

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'teacher_name': self.author.name
        }

    def set_students(self, student_file):
        try:
            lines = student_file.read()
            students = lines.split(",")
            for email in students:
                print email
                user = User.query.filter_by(email=email).first()
                if user:
                    if self not in user.courses:
                        user.courses.append(user)
                    else:
                        print "Student already enrolled in course: %s\n" % email
                else:
                    user = User(email, None, None)
                    user.courses.append(self)
                db.session.commit()
        except:
            raise

class Task(db.Model):
    __tablename__='task'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    content = db.Column(db.Text)

    def __init__(self, title):
        self.title = title
        return

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title
        }
