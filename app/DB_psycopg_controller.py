import psycopg2
from psycopg2.extras import RealDictCursor

connection = psycopg2.connect(
    host='localhost',
    user='anton',
    password='1234',
    database='testdb'
)


def get_employees():
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * FROM employee")
        return cursor.fetchall()


def get_employee(employee_id: int):
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * FROM employee JOIN employee_data "
                       "ON employee.id = employee_data.employee_id "
                       f"WHERE employee.id={employee_id}"
                       )
        return cursor.fetchone()


def add_employee(name, last_name, nickname, main_technology, status, cv, additional_data):
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


def delete_employee(employee_id: int):
    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(f"DELETE FROM employee WHERE id={employee_id};")
            connection.commit()
    except Exception:
        connection.rollback()
    finally:
        connection.close()


def main():
    print(get_employees())

    # print(get_employee(1))

    employee = {'name': "SQL111", 'last_name': "Test",
                'nickname': "", 'main_technology': "SQL",
                'status': "Busy", 'cv': "", 'additional_data': ""}

    # add_employee(**employee)

    # delete_employee(84)


if __name__ == '__main__':
    main()
