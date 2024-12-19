from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from .forms import CourseSubmitForm, EvaluationForm
from .models import User, Course, CourseEvaluation
from . import db

course_bp = Blueprint('course', __name__)


@course_bp.route('/')
def index():
    courses = Course.query.filter_by(approved=True).all()
    course_data = []

    for course in courses:
        # 获取所有通过审核的评价
        evaluations = CourseEvaluation.query.filter_by(course_id=course.id, approved=True).all()

        if evaluations:
            # 数据统计
            check_in = "是" if sum(e.check_in for e in evaluations) >= len(evaluations) / 2 else "否"

            # 统计考核方式、给分情况、作业量、授课质量的频率
            from collections import Counter
            test_type = Counter([e.test_type for e in evaluations]).most_common(1)[0][0]
            grade_distribution = Counter([e.grade_distribution for e in evaluations]).most_common(1)[0][0]
            workload = Counter([e.workload for e in evaluations]).most_common(1)[0][0]
            teaching_quality = Counter([e.teaching_quality for e in evaluations]).most_common(1)[0][0]
        else:
            # 如果没有评价，显示默认数据
            check_in = "暂无数据"
            test_type = grade_distribution = workload = teaching_quality = "暂无数据"

        # 将汇总数据添加到课程信息中
        course_data.append({
            'course': course,
            'check_in': check_in,
            'test_type': test_type,
            'grade_distribution': grade_distribution,
            'workload': workload,
            'teaching_quality': teaching_quality
        })

    return render_template('index.html', courses=course_data)

@course_bp.route('/submit_course', methods=['GET','POST'])
def submit_course():
    if 'user_id' not in session:
        flash('请先登录', 'danger')
        return redirect(url_for('user.login'))

    form = CourseSubmitForm()
    if form.validate_on_submit():
        course = Course(name=form.name.data, teacher=form.teacher.data)
        db.session.add(course)
        db.session.commit()
        flash('课程已提交审核', 'success')
        return redirect(url_for('course.index'))
    return render_template('course_submit.html', form=form)

@course_bp.route('/search')
def search():
    q = request.args.get('q', '')
    courses = Course.query.filter(Course.approved == True, Course.name.ilike(f'%{q}%')).all()
    return render_template('course_list.html', courses=courses, q=q)


@course_bp.route('/course/<int:course_id>')
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    if not course.approved:
        flash('该课程尚未审核通过', 'warning')
        return redirect(url_for('course.index'))

    # 获取已审核通过的评价
    evaluations = CourseEvaluation.query.filter_by(course_id=course_id, approved=True).all()

    # 格式化评价数据
    formatted_evaluations = []
    for e in evaluations:
        formatted_evaluations.append({
            'recommended': '推荐' if e.recommended else '不推荐',
            'check_in': '是' if e.check_in else '否',
            'test_type': e.test_type,
            'grade_distribution': e.grade_distribution,
            'workload': e.workload,
            'teaching_quality': e.teaching_quality,
            'comment': e.comment or '无',
            'timestamp': e.timestamp.strftime('%Y-%m-%d %H:%M')
        })

    return render_template('course_detail.html', course=course, evaluations=formatted_evaluations)

@course_bp.route('/course/<int:course_id>/evaluate', methods=['GET','POST'])
def evaluate(course_id):
    if 'user_id' not in session:
        flash('请先登录', 'danger')
        return redirect(url_for('user.login'))

    course = Course.query.get_or_404(course_id)
    if not course.approved:
        flash('该课程尚未审核通过，无法评价', 'danger')
        return redirect(url_for('course.index'))

    form = EvaluationForm()
    if form.validate_on_submit():
        evaluation = CourseEvaluation(
            user_id=session['user_id'],
            course_id=course_id,
            recommended=form.recommended.data,
            check_in=form.check_in.data,
            test_type=form.test_type.data,
            grade_distribution=form.grade_distribution.data,
            workload=form.workload.data,
            teaching_quality=form.teaching_quality.data,
            comment=form.comment.data
        )
        db.session.add(evaluation)
        db.session.commit()
        flash('评价已提交，等待审核', 'success')
        return redirect(url_for('course.course_detail', course_id=course_id))
    return render_template('evaluation_submit.html', form=form, course=course)