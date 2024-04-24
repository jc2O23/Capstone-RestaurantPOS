from mysql.connector import Error
from DB_connection import create_db_connection
import json
import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))


# region Menu Table
class Menu_Table:
    def __init__(self, menu_id, menu_name, menu_start_time, menu_end_time, menu_days):
        self.menu_id = menu_id
        self.menu_name = menu_name
        self.menu_start_time = menu_start_time
        self.menu_end_time = menu_end_time
        self.menu_days = menu_days

class Menu_TableDAO:
    def __init__(self, db):
        self.connection = create_db_connection(db)

    def fetch_all_menus(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Menu")
            return [Menu_Table(*row) for row in cursor.fetchall()]
    
    def fetch_menu_by_id(self, menu_id):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Menu WHERE menu_id = %s", (menu_id,))
            item = cursor.fetchone()
            return Menu_Table(*item)
        
    def fetch_menu_by_name(self, menu_name):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Menu WHERE menu_name = %s", (menu_name,))
            item = cursor.fetchone()
            return Menu_Table(*item)
    
    def menus_to_json(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('SELECT * FROM menu')

                rows = cursor.fetchall()
                
                column_names = [i[0] for i in cursor.description]

                data = [dict(zip(column_names, row)) for row in rows]
                
                # Wrap the data list in a dictionary with the table name as the key
                json_data = json.dumps({'menu': data}, indent=2)
                #json_github(json_data)

                with open('./static/data/menu.json', 'w') as json_file:
                    json_file.write(json_data)
                
                print("MySQL to JSON complete")

        except Error as e:
            print("MySQL to JSON ")
            print(f"Error: {e}")
    
    def return_menus_json(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('SELECT * FROM menu')

                rows = cursor.fetchall()
                
                column_names = [i[0] for i in cursor.description]

                data = [dict(zip(column_names, row)) for row in rows]
                
                # Wrap the data list in a dictionary with the table name as the key
                json_data = json.dumps({'menu': data}, indent=2)
                #json_github(json_data)

                return json_data

        except Error as e:
            print("MySQL to JSON ")
            print(f"Error: {e}")

    def insert_menu(self, menu_name, menu_start_time, menu_end_time, menu_days):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO menu (menu_name, menu_start_time, menu_end_time, menu_days)
                VALUES (%s, %s, %s, %s)
            """, (menu_name, menu_start_time, menu_end_time, menu_days,))
            self.connection.commit()

    def delete_menu_by_id(self, menu_id):
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM menu WHERE menu_id = %s", (menu_id,))
            self.connection.commit()        

    def update_menu_by_id(self, menu_name, menu_start_time, menu_end_time, menu_days, menu_id):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                UPDATE menu
                SET menu_name = %s, menu_start_time = %s, menu_end_time = %s, menu_days = %s
                WHERE menu_id = %s
            """, (menu_name, menu_start_time, menu_end_time, menu_days, menu_id,))
            self.connection.commit()

    def close(self):
        close_connection(self.connection)
## end region

# region Menu Sections Table
class MenuSections_Table:
    def __init__(self, menu_section_id, menu_section_name, menu_sec_parent):
        self.menu_section_id = menu_section_id
        self.menu_section_name = menu_section_name
        self.menu_sec_parent = menu_sec_parent

class MenuSections_TableDAO:
    def __init__(self, db):
        self.connection = create_db_connection(db)

    def fetch_all_sections(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM menu_sections")
            return [MenuSections_Table(*row) for row in cursor.fetchall()]
    
    def fetch_menuSection_by_id(self, menu_section_id):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM menu_sections WHERE menu_section_id = %s", (menu_section_id,))
            item = cursor.fetchone()
            return MenuSections_Table(*item)
        
    def fetch_section_by_name(self, menu_section_name):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM menu_sections WHERE menu_section_name = %s", (menu_section_name,))
            item = cursor.fetchone()
            return MenuSections_Table(*item)
    
    def fetch_section_by_menuId(self, menu_id):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM menu_sections WHERE menu_sec_parent = %s", (menu_id,))
            return [MenuSections_Table(*row) for row in cursor.fetchall()]
    
    def insert_section(self, menu_section_name, menu_sec_parent):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO menu_sections (menu_section_name, menu_sec_parent)
                VALUES (%s, %s)
            """, (menu_section_name, menu_sec_parent,))
            self.connection.commit()
    
    def update_sec_by_id(self, menu_section_name, menu_sec_parent, menu_section_id):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                UPDATE menu_sections
                SET menu_section_name = %s, menu_sec_parent = %s
                WHERE menu_section_id = %s
            """, (menu_section_name, menu_sec_parent, menu_section_id,))
            self.connection.commit()
    


    def menuSections_to_json(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('SELECT * FROM menu_sections')

                rows = cursor.fetchall()
                
                column_names = [i[0] for i in cursor.description]

                data = [dict(zip(column_names, row)) for row in rows]
                
                # Wrap the data list in a dictionary with the table name as the key
                json_data = json.dumps({'menu_sections': data}, indent=2)
                #json_github(json_data)

                with open('./static/data/menu_sections.json', 'w') as json_file:
                    json_file.write(json_data)
                
                print("MySQL to JSON complete")

        except Error as e:
            print("MySQL to JSON ")
            print(f"Error: {e}")
        
    

    def close(self):
        close_connection(self.connection)
# end region

# region Menu/Section Join
class MenuSec_Join_Menu_Table:
    def __init__(self, menu_section_id, menu_section_name, menu_sec_parent, menu_name):
        self.menu_section_id = menu_section_id
        self.menu_section_name = menu_section_name
        self.menu_sec_parent = menu_sec_parent
        self.menu_name = menu_name

class MenuSec_Join_Menu_TableDAO:
    def __init__(self, db):
        self.connection = create_db_connection(db)
    
    def join_menuSections_menuName(self, name):
        with self.connection.cursor() as cursor:
            cursor.execute("""SELECT menu_section_id, menu_section_name, menu_sec_parent, menu.menu_name FROM menu_sections JOIN menu 
            ON menu_sec_parent = menu_id WHERE menu.menu_name = %s
            """, (name,))
            return [MenuSec_Join_Menu_Table(*row) for row in cursor.fetchall()]
            

    
    def close(self):
        close_connection(self.connection)
# end region

# region Menu Items Table
class MenuItems_Table:
    def __init__(self, menu_items_id, menu_item_name, menu_item_desc, menu_item_price, menu_item_stock, menu_item_parent, menu_main):
        self.menu_items_id = menu_items_id
        self.menu_item_name = menu_item_name
        self.menu_item_desc = menu_item_desc
        self.menu_item_price = menu_item_price
        self.menu_item_stock = menu_item_stock
        self.menu_item_parent = menu_item_parent
        self.menu_main = menu_main

class MenuItems_TableDAO:
    def __init__(self, db):
        self.connection = create_db_connection(db)

    def fetch_all_items(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM menu_items")
            return [MenuItems_Table(*row) for row in cursor.fetchall()]
    
    def fetch_items_by_section(self, menu_item_parent):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM menu_items WHERE menu_item_parent = %s", (menu_item_parent,))
            return [MenuItems_Table(*row) for row in cursor.fetchall()]
    
    def fetch_item_by_id(self, menu_items_id):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM menu_items WHERE menu_items_id = %s", (menu_items_id,))
            item = cursor.fetchone()
            return MenuItems_Table(*item)
        
    def delete_item_by_id(self, menu_items_id):
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM menu_items WHERE menu_items_id = %s", (menu_items_id,))
            self.connection.commit()
    
    def insert_item(self, name, desc, price, stock, menu_section, menu_main):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO menu_items (menu_item_name, menu_item_desc, menu_item_price, menu_item_stock, menu_item_parent, menu_main)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, desc, price, stock, menu_section, menu_main,))
            self.connection.commit()

    def update_item_by_id(self, name, desc, price, stock, menu_section, menu_main, item_id):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                UPDATE menu_items
                SET menu_item_name = %s, menu_item_desc = %s, menu_item_price = %s, menu_item_stock = %s, menu_item_parent = %s, menu_main = %s
                WHERE menu_items_id = %s
            """, (name, desc, price, stock, menu_section, menu_main, item_id,))
            self.connection.commit()
    
    def menuItems_to_json(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('SELECT * FROM menu_items')

                rows = cursor.fetchall()
                
                column_names = [i[0] for i in cursor.description]

                data = [dict(zip(column_names, row)) for row in rows]
                
                # Wrap the data list in a dictionary with the table name as the key
                json_data = json.dumps({'menu_items': data}, indent=2)
                #json_github(json_data)

                with open('./static/data/menu_items.json', 'w') as json_file:
                    json_file.write(json_data)
                
                print("MySQL to JSON complete")

        except Error as e:
            print("MySQL to JSON ")
            print(f"Error: {e}")
    
    def close(self):
        close_connection(self.connection)
# end region


# region Employee Table
class Employees_Table:
    def __init__(self, employee_id, first_name, last_name, display_name, pin_num, pin_code, access_level, role):
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.display_name = display_name
        self.pin_num = pin_num
        self.pin_code = pin_code
        self.access_level = access_level
        self.role = role

class Employees_TableDAO:
    def __init__(self, db):
        self.connection = create_db_connection(db)

    def fetch_admins(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Employee WHERE access_level = 1")
            return [Employees_Table(*row) for row in cursor.fetchall()]
    
    def fetch_employee_by_pin(self, pin_num):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Employee WHERE pin_num = %s", (pin_num,))
            item = cursor.fetchone()
            return Employees_Table(*item)
    
    def fetch_all_employees(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Employee")
            return [Employees_Table(*row) for row in cursor.fetchall()]
        
    def insert_employee(self, first_name, last_name, display_name, pin_num, pin_code, access_level, role):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                    INSERT INTO Employee (first_name, last_name, display_name, pin_num, pin_code, access_level, role)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (first_name, last_name, display_name, pin_num, pin_code, access_level, role,))
            self.connection.commit()

    
    def employees_to_json(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('SELECT * FROM Employee')

                rows = cursor.fetchall()
                
                column_names = [i[0] for i in cursor.description]

                data = [dict(zip(column_names, row)) for row in rows]
                
                # Wrap the data list in a dictionary with the table name as the key
                json_data = json.dumps({'Employee': data}, indent=2)
                #json_github(json_data)

                with open('./static/data/employees.json', 'w') as json_file:
                    json_file.write(json_data)
                
                print("MySQL to JSON complete")

        except Error as e:
            print("MySQL to JSON ")
            print(f"Error: {e}")
    
    def close(self):
        close_connection(self.connection)
# end region


# region Employee Shift Table
class EmployeesShift_Table:
    def __init__(self, clock_record_id, clock_In, clock_Out, employee_id, close_Out, clock_total):
        self.clock_record_id = clock_record_id
        self.clock_In = clock_In
        self.clock_Out = clock_Out
        self.employee_id = employee_id
        self.close_Out = close_Out
        self.clock_total = clock_total

class EmployeesShift_TableDAO:
    def __init__(self, db):
        self.connection = create_db_connection(db)


    def fetch_all_records(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM employee_shift")
            return [EmployeesShift_Table(*row) for row in cursor.fetchall()]
        
    def employee_clockIN(self, clock_In, employee_id):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                    INSERT INTO employee_shift (clock_In, employee_id)
                VALUES (%s, %s)
            """, (clock_In, employee_id,))
            self.connection.commit()

    def fetch_record_by_EMPL_ID(self, employee_id):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM employee_shift WHERE employee_id = %s AND close_record = 0", (employee_id,))
            item = cursor.fetchone()
            if item is not None:
                return EmployeesShift_Table(*item)
            else:
                return None
    
    def fetch_record_by_REC_ID(self, clock_record_id):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM employee_shift WHERE clock_record_id = %s", (clock_record_id,))
            item = cursor.fetchone()
            if item is not None:
                return EmployeesShift_Table(*item)
            else:
                return None
            
    def employee_clockOUT(self, clock_record_id, clock_Out):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                    UPDATE employee_shift SET clock_Out = %s, close_record = %s, clock_total = TIMESTAMPDIFF(MINUTE, clock_In, %s) / 60
                           WHERE clock_record_id = %s
            """, (clock_Out, '1', clock_Out, clock_record_id,))
            self.connection.commit()

    def close(self):
        close_connection(self.connection)
# end region



###### Close Connection ######
def close_connection(connection):
    if connection.is_connected():
        try:
            connection.close()
            print("Connection Closed Successful")
        except Error as e:
            print("Close Out ")
            print(f"Error: '{e}'")
            return



# region Main Method
if __name__ == '__main__':
    # test = Menu_TableDAO('mysqlMenus')

    # menus = test.fetch_all_menus()


    # # Now you have a list of Menu objects filled with data from the database
    # for menu in menus:
    #     print(f"Menu ID: {menu.menu_id}, Menu Name: {menu.menu_name}")

    
    # test = Employees_TableDAO('mysqlEmployees')

    # emps = test.fetch_admins()


    # # Now you have a list of Menu objects filled with data from the database
    # for row in emps:
    #     print(f" ID: {row.employee_id}, Name: {row.first_name} {row.last_name}, DIS: {row.display_name}, PIN: {row.pin_num} {row.pin_code} LEVL: {row.access_level} {row.role}")

    # test = MenuItems_TableDAO('mysqlMenus')

    # items = test.fetch_all_items()


    # # Now you have a list of Menu objects filled with data from the database
    # for row in items:
    #     print(row.menu_item_name) 

    # test = MenuItems_TableDAO('mysqlMenus')
    # test.menuItems_to_json()

    # test = MenuSec_Join_Menu_TableDAO('mysqlMenus')
    # test3 = test.join_menuSections_menuName('Dinner Menu')

    # test = Menu_TableDAO("mysqlMenus")
    # test.menus_to_json()

    # test = MenuSections_TableDAO("mysqlMenus")
    # test.menuSections_to_json()

    # test = Employees_TableDAO("mysqlEmployees")
    # test.employees_to_json()
    
    # test = Menu_TableDAO("mysqlMenus")
    # test2 = test.return_menus_json()


    test = EmployeesShift_TableDAO("mysqlEmployees")
    test2 = test.employee_clockOUT('3', "2024-04-18 21:43:34")
    print(test2)

    # test = Employees_TableDAO("mysqlEmployees")
    # test2 = test.fetch_employee_by_pin(101)
    # print(test2)

    # test = MenuItems_TableDAO("mysqlMenus")
    # test2 = test.fetch_item_by_id(10)
    # print(test2)
    pass

# end region