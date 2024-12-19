from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('登录')

class VerificationForm(FlaskForm):
    code = StringField('验证码', validators=[DataRequired()])
    submit = SubmitField('验证')

class CourseSubmitForm(FlaskForm):
    name = StringField('课程名称', validators=[DataRequired()])
    teacher = StringField('授课老师', validators=[DataRequired()])
    submit = SubmitField('提交')

class EvaluationForm(FlaskForm):
    recommended = BooleanField('推荐（勾选则推荐）')
    check_in = BooleanField('签到方式（勾选则有签到）')
    test_type = SelectField('考核方式', choices=[('论文','结课论文'),('闭卷考试','闭卷考试'),('开卷考试','开卷考试'),('小组作业','小组作业'),('其他','其他')])
    grade_distribution = SelectField('给分情况', choices=[('高','高'),('一般','一般'),('低','低')])
    workload = SelectField('作业量', choices=[('多','多'),('少','少'),('没有','没有')])
    teaching_quality = SelectField('授课质量', choices=[('非常好','非常好'),('好','好'),('中等','中等'),('差','差'),('非常差','非常差')])
    comment = TextAreaField('匿名评论', validators=[Length(max=500)])
    submit = SubmitField('提交评价')
