from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
from datetime import datetime


class CampaignForm(FlaskForm):
    name = StringField('活动名称', validators=[
        DataRequired(message='活动名称不能为空'),
        Length(min=2, max=50, message='活动名称长度必须在2-50个字符之间')
    ])
    description = TextAreaField('活动描述', validators=[
        Optional(),
        Length(max=500, message='描述不能超过500个字符')
    ])
    start_date = DateField('开始日期',
                           format='%Y-%m-%d',
                           validators=[DataRequired(message='请选择开始日期')],
                           default=datetime.now
                           )
    end_date = DateField('结束日期',
                         format='%Y-%m-%d',
                         validators=[DataRequired(message='请选择结束日期')],
                         default=datetime.now
                         )
    status = SelectField('状态', choices=[
        ('未开始', '未开始'),
        ('进行中', '进行中'),
        ('已结束', '已结束')
    ], validators=[DataRequired(message='请选择活动状态')])
    submit = SubmitField('保存活动')

    def validate(self, extra_validators=None):
        # 自定义验证：结束日期必须大于开始日期
        if not super().validate(extra_validators):
            return False

        if self.start_date.data and self.end_date.data:
            if self.end_date.data <= self.start_date.data:
                self.end_date.errors.append('结束日期必须晚于开始日期')
                return False

        return True