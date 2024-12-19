from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_banned = db.Column(db.Boolean, default=False)
    verified = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    teacher = db.Column(db.String(120), nullable=False)
    approved = db.Column(db.Boolean, default=False)

class CourseEvaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    recommended = db.Column(db.Boolean, default=True)
    check_in = db.Column(db.Boolean, default=False)
    test_type = db.Column(db.String(50))
    grade_distribution = db.Column(db.String(20))
    workload = db.Column(db.String(20))
    teaching_quality = db.Column(db.String(20))
    comment = db.Column(db.Text)
    approved = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='evaluations')
    course = db.relationship('Course', backref='evaluations')
