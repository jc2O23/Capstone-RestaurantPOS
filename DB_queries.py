from mysql.connector import Error, MySQLConnection
from DB_connection import read_db_config
import json
from git_hub import json_github


def create_database(query, connection):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Database created successfully")
    except Error as err:
        print("DB Creation ")
        print(f"Error: '{err}'")

    finally:
        cursor.close()
        connection.close()


def create_db_connection(db):
    db_config = read_db_config(db)

    try:
        print("Attempting Connection to Database...")
        connection = MySQLConnection(**db_config)
        if connection.is_connected():
            print("Connection established")
        else:
            print("Connection failed")

    except Error as err:
        print("Connection failed ")
        print(f"Error: '{err}'")
        quit()

    return connection

def execute_query(connection, query, params = None):
    cursor = connection.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        connection.commit()
        print("Query successful")
    except Error as err:
        print("Execute Query ")
        print(f"Error: '{err}'")



# connection = create_db_connection("localhost", "root", "CSC481_DevGrp7", "Employees")
# execute_query(connection, create_employees_table)




def new_query(query, connection):
    try:
        
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        print('Total Row(s):', cursor.rowcount)
        for row in rows:
            print(row)


    except Error as e:
        print("New Query ")
        print(f"Error: '{e}'")

    finally:
        cursor.close()
        connection.close()

def fetch_query_results(query, connection, params=None):
    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return rows  
    except Error as e:
        print("Fetch All ")
        print(f"Error: '{e}'")
        return None 
    
def sql_to_json(query, connection, table_name): 
    try:
        cursor = connection.cursor()

        cursor.execute(query)
        
        rows = cursor.fetchall()
        
        column_names = [i[0] for i in cursor.description]

        data = [dict(zip(column_names, row)) for row in rows]
        
        # Wrap the data list in a dictionary with the table name as the key
        json_data = json.dumps({table_name: data}, indent=2)
        #json_github(json_data)

        with open('menu.json', 'w') as json_file:
            json_file.write(json_data)
        
        print("MySQL to JSON complete")

    except Error as e:
        print("MySQL to JSON ")
        print(f"Error: {e}")
    

def close_out(connection):
    try:
        cursor = connection.cursor()
        cursor.close()
        connection.close()
        print("Connection Closed Successful")
    except Error as e:
        print("Close Out ")
        print(f"Error: '{e}'")
        return
        


if __name__ == '__main__':
    
    query = "SELECT * FROM Employee WHERE access_level = 1"
    db = "mysqlEmployees"
    connection = create_db_connection(db)

    new_query(query, connection)




    # query = "CREATE DATABASE Menus"


    # query = "CREATE DATABASE Employees"
    # db = "mysqlServer"
    # connection = create_db_connection(db)
    # create_database(query, connection)


    # db = "mysqlEmployees"
    # connection = create_db_connection(db)
    # create_employees_table = """
    #     CREATE TABLE Employee (
    #         employee_id INT AUTO_INCREMENT PRIMARY KEY,
    #         first_name VARCHAR(40) NOT NULL,
    #         last_name VARCHAR(40) NOT NULL,
    #         display_name VARCHAR(40) NOT NULL,
    #         pin_num INT NOT NULL,
    #         pin_code INT NOT NULL,
    #         access_level INT NOT NULL,
    #         role VARCHAR(20) NOT NULL,
    #         CHECK (pin_num BETWEEN 1 AND 999),
    #         CHECK (pin_code BETWEEN 1 AND 9999),
    #         CHECK (access_level BETWEEN 1 AND 5)
    #     );
    #     """
    # execute_query(connection, create_employees_table)
    
    # insert_employees_query = """
    #     INSERT INTO Employee (first_name, last_name, display_name, pin_num, pin_code, access_level, role)
    #     VALUES
    #         ('John', 'Campbell', 'John C.', 116, 1116, 5, 'Owner'),
    #         ('Liam', 'McFadden', 'Liam F.', 190, 1190, 5, 'Owner'),
    #         ('Daniel', 'Sahm', 'Dan S.', 202, 2202, 5, 'Owner')
    #     """
    # execute_query(connection, insert_employees_query)

    query = "SELECT * FROM Employee"

    db = "mysqlEmployees"
    connection = create_db_connection(db)
    # test = fetch_query_results(query, connection)
    # # test1 = " "
    # # test1=test1.join(test)



    # print(test)
    # with open('data.json', 'w') as f:
    #     f.write(str(test))
    
    # test = json.loads(test)

    # with open('data.json', 'w') as f:
    #     f.write(test)


    query = "SELECT * FROM menu_items"

    db = "mysqlMenus"
    connection = create_db_connection(db)
    sql_to_json(query, connection, "menu_items")
    close_out(connection)







    


    



    



