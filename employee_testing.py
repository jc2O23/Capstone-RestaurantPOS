import tkinter as tk
from tkinter import ttk
from DB_queries import *
from tkinter.font import Font



class NewEmployee:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("New Employee")
        self.root.geometry("500x500")

        self.fistName_label = ttk.Label(self.root, text="First Name:")
        self.fistName_label.grid(row=0, column=0, padx=10, pady=10)

        self.firstName_entry = ttk.Entry(self.root)
        self.firstName_entry.grid(row=0, column=1, padx=10, pady=10)


        self.lastName_label = ttk.Label(self.root, text="Last Name:")
        self.lastName_label.grid(row=1, column=0, padx=10, pady=10)

        self.lastName_entry = ttk.Entry(self.root)
        self.lastName_entry.grid(row=1, column=1, padx=10, pady=10)
        

        self.displayName_label = ttk.Label(self.root, text="Display Name:")
        self.displayName_label.grid(row=2, column=0, padx=10, pady=10)

        self.displayName_entry = ttk.Entry(self.root)
        self.displayName_entry.grid(row=2, column=1, padx=10, pady=10)


        self.pinNumber_label = ttk.Label(self.root, text="Pin Number:")
        self.pinNumber_label.grid(row=3, column=0, padx=10, pady=10)

        self.pinNumber_entry = ttk.Entry(self.root)
        self.pinNumber_entry.grid(row=3, column=1, padx=10, pady=10)


        self.pinCode_label = ttk.Label(self.root, text="Pin Code:")
        self.pinCode_label.grid(row=4, column=0, padx=10, pady=10)

        self.pinCode_entry = ttk.Entry(self.root)
        self.pinCode_entry.grid(row=4, column=1, padx=10, pady=10)

        self.accessLevel_label = ttk.Label(self.root, text="Access Level:")
        self.accessLevel_label.grid(row=5, column=0, padx=10, pady=10)

        self.accessLevels = [1, 2, 3, 4, 5]
        self.accessLevel_entry = ttk.Combobox(self.root, values=self.accessLevels, state='readonly')
        self.accessLevel_entry.grid(row=5, column=1, padx=10, pady=10)
        self.accessLevel_entry.set(1)

        self.role_label = ttk.Label(self.root, text="Role:")
        self.role_label.grid(row=6, column=0, padx=10, pady=10)

        self.roles = ['Owner', 'Manager', 'Server', 'Bartender', 'Kitchen', 'Hostess']
        self.role_entry = ttk.Entry(self.root)
        self.role_entry.grid(row=6, column=1, padx=10, pady=10)


        self.submit_button = ttk.Button(self.root, text="Submit", command=self.submit)
        self.submit_button.grid(row=7, column=1, padx=10, pady=10)

        self.root.mainloop()

    def submit(self):
        db = "mysqlEmployees"
        connection = create_db_connection(db)

        first_name = self.firstName_entry.get()
        last_name = self.lastName_entry.get()
        display_name = self.displayName_entry.get()
        pin_num = self.pinNumber_entry.get()
        pin_code = self.pinCode_entry.get()
        access_level = self.accessLevel_entry.get()
        role = self.role_entry.get()

        insert_employees_query = """
        INSERT INTO Employee (first_name, last_name, display_name, pin_num, pin_code, access_level, role)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        execute_query(connection, insert_employees_query, (first_name, last_name, display_name, pin_num, pin_code, access_level, role))

class EmployeeLogIN:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Log In")
        self.root.geometry("500x500")
        self.buttonStyle = ttk.Style()
        self.buttonStyle.configure('my.TButton', font=('Helvetica', 24))
        self.entryFont = Font(family="Helvetica", size=24)

        for row_index in range(5):
            self.root.grid_rowconfigure(row_index, weight=1)
            self.root.grid_columnconfigure(row_index, weight=1)

        # Create and place the LogINEntry in the center cell (2, 2)
        self.LogINEntry = ttk.Entry(self.root, font=self.entryFont, state='readonly', justify='center')
        self.LogINEntry.grid(row=0, column=2, sticky='nesw')  # Center cell of 5x5 grid

        self.button = ttk.Button(self.root, text='1', style='my.TButton', command=lambda : self.insertNumber(1))
        self.button.grid(row=1, column=1, sticky='nesw')
        self.button = ttk.Button(self.root, text='2', style='my.TButton', command=lambda : self.insertNumber(2))
        self.button.grid(row=1, column=2, sticky='nesw')
        self.button = ttk.Button(self.root, text='3', style='my.TButton', command=lambda : self.insertNumber(3))
        self.button.grid(row=1, column=3, sticky='nesw')
        self.button = ttk.Button(self.root, text='4', style='my.TButton', command=lambda : self.insertNumber(4))
        self.button.grid(row=2, column=1, sticky='nesw')
        self.button = ttk.Button(self.root, text='5', style='my.TButton', command=lambda : self.insertNumber(5))
        self.button.grid(row=2, column=2, sticky='nesw')
        self.button = ttk.Button(self.root, text='6', style='my.TButton', command=lambda : self.insertNumber(6))
        self.button.grid(row=2, column=3, sticky='nesw')
        self.button = ttk.Button(self.root, text='7', style='my.TButton', command=lambda : self.insertNumber(7))
        self.button.grid(row=3, column=1, sticky='nesw')
        self.button = ttk.Button(self.root, text='8', style='my.TButton', command=lambda : self.insertNumber(8))
        self.button.grid(row=3, column=2, sticky='nesw')
        self.button = ttk.Button(self.root, text='9', style='my.TButton', command=lambda : self.insertNumber(9))
        self.button.grid(row=3, column=3, sticky='nesw')
        self.button = ttk.Button(self.root, text='0', style='my.TButton', command=lambda : self.insertNumber(0))
        self.button.grid(row=4, column=2, sticky='nesw')

        self.root.mainloop()

    def insertNumber(self, number):
        print(number)
        self.LogINEntry.config(state='normal')
        self.LogINEntry.insert(3 ,str(number))
        self.LogINEntry.config(state='readonly')
        


if __name__ == "__main__":
    NewEmployee()
    EmployeeLogIN()