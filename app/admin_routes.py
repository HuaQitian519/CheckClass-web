from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import User, Course, CourseEvaluation
from . import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
def check_admin():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('user.login'))

@admin_bp.route('/')
def dashboard():
    pending_courses = Course.query.filter_by(approved=False).count()
    pending_evals = CourseEvaluation.query.filter_by(approved=False).count()
    return render_template('admin_dashboard.html', pending_courses=pending_courses, pending_evals=pending_evals)

@admin_bp.route('/review_courses')
def review_courses():
    courses = Course.query.filter_by(approved=False).all()
    return render_template('admin_course_review.html', courses=courses)

@admin_bp.route('/approve_course/<int:course_id>')
def approve_course(course_id):
    course = Course.query.get_or_404(course_id)
    course.approved = True
    db.session.commit()
    flash('课程已审核通过', 'success')
    return redirect(url_for('admin.review_courses'))

@admin_bp.route('/review_evaluations')
def review_evaluations():
    evals = CourseEvaluation.query.filter_by(approved=False).all()
    return render_template('admin_evaluation_review.html', evaluations=evals)

@admin_bp.route('/approve_evaluation/<int:eval_id>')
def approve_evaluation(eval_id):
    evaluation = CourseEvaluation.query.get_or_404(eval_id)
    evaluation.approved = True
    db.session.commit()
    flash('评价已审核通过', 'success')
    return redirect(url_for('admin.review_evaluations'))

@admin_bp.route('/view_evaluation_user/<int:eval_id>')
def view_evaluation_user(eval_id):
    evaluation = CourseEvaluation.query.get_or_404(eval_id)
    user = User.query.get(evaluation.user_id)
    return f'发布者邮箱: {user.email}'

@admin_bp.route('/users')
def manage_users():
    users = User.query.all()
    return render_template('admin_user_management.html', users=users)

@admin_bp.route('/ban_user/<int:user_id>')
def ban_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_banned = True
    db.session.commit()
    flash('用户已封禁', 'success')
    return redirect(url_for('admin.manage_users'))