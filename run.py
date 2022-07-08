from app import create_app, db
from app.models.dbmodels import Manager, Employee, EmployeeData

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'app': app, 'db': db, 'Manager': Manager, 'Employee': Employee, 'EmployeeData': EmployeeData}


if __name__ == '__main__':
    app.run(debug=True)
