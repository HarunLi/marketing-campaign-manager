# 在 app 目录下创建 forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired

class CampaignForm(FlaskForm):
    name = StringField('活动名称', validators=[DataRequired()])
    description = TextAreaField('活动描述')
    start_date = DateField('开始日期', format='%Y-%m-%d')
    end_date = DateField('结束日期', format='%Y-%m-%d')
    status = SelectField('状态', choices=[
        ('未开始', '未开始'), 
        ('进行中', '进行中'), 
        ('已结束', '已结束')
    ])
    submit = SubmitField('创建活动')