from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models.dbmodels import Manager


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
    submit = SubmitField('Add')


class UpdateEmployeeForm(AddEmployeeForm):
    submit = SubmitField('Update')


class TechnologyFilterForm(FlaskForm):
    main_technology = SelectField(
        'Main technology',
        choices=['Python', 'DevOps', 'Android', 'UI/UX', 'Flutter'],
        validators=[DataRequired()]
    )
    submit = SubmitField('Filter')


class EmployeeSearchForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    submit = SubmitField('Search')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registration')

    def validate_email(self, email: StringField):
        user = Manager.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
