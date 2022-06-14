from app import app, db
from app.models.dbmodels import Employee, EmployeeData
from flask import render_template, redirect, url_for

'''
Create simple methods for user model (and user_data) :
Create user
Read user (get)
Update user
Delete user
You need to do it both ways - ORM and psycopg2 (raw sql)
'''


@app.route('/')
@app.route('/index')
def main_page():
    employees = db.session.query(Employee).all()
    return render_template('main_page.html', employees=employees)


@app.route('/get_user/<int:employee_id>', methods=['GET', 'POST'])
def get_user(employee_id):
    employee = Employee.query.filter(Employee.id == employee_id).first()
    return render_template('employee_info_page.html', employee=employee)


@app.route('/create_user')
def create_user():
    pass


@app.route('/update_user/<int:employee_id>')
def update_user(employee_id):
    employee = Employee.query.filter(Employee.id == employee_id).first()
    pass


@app.route('/delete_user/<int:employee_id>', methods=['GET', 'POST'])
def delete_user(employee_id):
    Employee.query.filter(Employee.id == employee_id).delete()
    db.session.commit()
    db.session.close()
    return redirect(url_for('main_page'))
