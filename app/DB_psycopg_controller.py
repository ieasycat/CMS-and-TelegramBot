import psycopg2
from psycopg2.extras import RealDictCursor
from config import CONFIG


def get_employees(connection):
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * FROM employee")
        return cursor.fetchall()


def get_employee(connection, employee_id: int):
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * FROM employee JOIN employee_data "
                       "ON employee.id = employee_data.employee_id "
                       f"WHERE employee.id={employee_id}"
                       )
        return cursor.fetchone()


def add_employee(connection, name, last_name, nickname, main_technology, status, cv, additional_data):
    employee = (name, last_name, nickname, main_technology, status)
    employee_data = (cv, additional_data)
    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            query = """INSERT INTO employee (name, last_name, nickname, main_technology, status) 
                                VALUES (%s, %s, %s, %s, %s) 
                                RETURNING id"""
            cursor.execute(query, employee)

            user_id = cursor.fetchone()['id']
            connection.commit()

            query = f"""INSERT INTO employee_data (cv, additional_data, employee_id) VALUES (%s, %s, {user_id})"""
            cursor.execute(query, employee_data)

            connection.commit()
    except Exception:
        connection.rollback()
    finally:
        connection.close()


def delete_employee(connection, employee_id: int):
    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(f"DELETE FROM employee WHERE id={employee_id};")
            connection.commit()
    except Exception:
        connection.rollback()
    finally:
        connection.close()


def main():
    connection = psycopg2.connect(
        host=CONFIG.SQLALCHEMY_DB_HOST,
        user=CONFIG.SQLALCHEMY_DB_USER,
        password=CONFIG.SQLALCHEMY_DB_PASSWORD,
        database=CONFIG.SQLALCHEMY_DATABASE
    )

    print(get_employees(connection))

    # print(get_employee(connection, 1))

    employee = {'name': "SQL111", 'last_name': "Test",
                'nickname': "", 'main_technology': "SQL",
                'status': "Busy", 'cv': "", 'additional_data': ""}

    # add_employee(connection, **employee)

    # delete_employee(connection, 84)


if __name__ == '__main__':
    main()
