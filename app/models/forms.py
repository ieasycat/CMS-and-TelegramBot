from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class AddEmployeeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    main_technology = SelectField(
        'Main technology',
        choices=['Python', 'DevOps', 'Android', 'UI/UX', 'Flutter'],
        validators=[DataRequired()]
    )
    status = SelectField('Status', choices=['Free', 'Busy'], validators=[DataRequired()])
    cv = TextAreaField('CV')
    additional_data = TextAreaField('Additional data')


class TechnologyFilter(FlaskForm):
    main_technology = SelectField(
        'Main technology',
        choices=['Python', 'DevOps', 'Android', 'UI/UX', 'Flutter'],
        validators=[DataRequired()]
    )


class EmployeeSearch(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
