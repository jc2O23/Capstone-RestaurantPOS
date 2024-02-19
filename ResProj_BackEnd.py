import tkinter as tk
from tkinter import ttk
from DB_queries import *
from tkinter import messagebox
import re

class AdminLogin: 
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x250")
        self.root.resizable(False, False)
        self.root.title('Admin Log-In')

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.x = (self.screen_width / 2) - (150)
        self.y = (self.screen_height / 2) - (250)
        self.root.geometry('+%d+%d' % (self.x, self.y))

        self.user_enter = tk.StringVar()
        self.user_pass = tk.StringVar()
       
                   


        self.signin = ttk.Frame(self.root)
        self.signin.pack(padx=10, pady=10, fill='x', expand=True)


        self.user_enter_label = ttk.Label(self.signin, text="User Name:")
        self.user_enter_label.pack(fill='x', expand=True)

        email_entry = ttk.Entry(self.signin, textvariable=self.user_enter)
        email_entry.pack(fill='x', expand=True)
        email_entry.focus()

        self.password_label = ttk.Label(self.signin, text="Password:")
        self.password_label.pack(fill='x', expand=True)

        self.password_entry = ttk.Entry(self.signin, textvariable=self.user_pass, show="*")
        self.password_entry.pack(fill='x', expand=True)

        self.login_button = ttk.Button(self.signin, text="Login", command=self.login_attempt)
        self.login_button.pack(fill='x', expand=True, pady=10)

        self.cancel_button = ttk.Button(self.signin, text="Cancel", command=self.root.destroy)
        self.cancel_button.pack(fill='x', expand=True, pady=10)


        self.root.mainloop()

    def login_attempt(self):

        if self.user_enter.get() == '':
            messagebox.showerror("User Name Empty", "Please enter a User Name.")
            return
        elif self.user_pass.get() == '':
            messagebox.showerror("Password  Empty", "Please enter a Password.")
            return
        else:

            self.query = "SELECT * FROM Employee WHERE access_level = 1"
            self.db = "mysqlEmployees"
            self.connection = create_db_connection(self.db)

            test = fetch_query_results(self.query, self.connection)
            print(test)
            
            for row in test:
                if self.user_enter.get().strip() == str(row[4]) and self.user_pass.get().strip() == str(row[5]):
                    close_out(self.connection)
                    messagebox.showinfo("Signed In", "Signed in as " + str(row[3]))
                    self.root.destroy()
                    mainWindow(str(row[3]))
                    return
                
            messagebox.showerror("Invaild Login", "Invaild User Name and/or Password")
            self.user_pass.set("")

            

            

class mainWindow:
    def __init__(self, name):
        self.root = tk.Tk()
        self.root.title("Resturant Back-End" + " | Signed in as " + str(name))
        self.root.state('zoomed')
        self.root.iconbitmap('./favicon.ico')

        

        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        self.file_menu = tk.Menu(self.menubar, tearoff=False)
        self.empl_menu = tk.Menu(self.menubar, tearoff=False)
        self.itemMenu_menu = tk.Menu(self.menubar, tearoff=False)

        self.file_menu.add_command(label='Sign-Out', command=self.sign_out, font=('', 11))
        self.menubar.add_cascade(label='File', menu=self.file_menu)

        self.menubar.add_cascade(label='Employee', menu=self.empl_menu)
        self.empl_menu.add_command(label='All Employees', command=NewEmployee, font=('', 11))
        self.empl_menu.add_command(label='New Employee', command=NewEmployee, font=('', 11))
        self.empl_menu.add_command(label='Clock-In Status', command=NewEmployee, font=('', 11))

        self.menubar.add_cascade(label='Menus', menu=self.itemMenu_menu)
        self.itemMenu_menu.add_command(label='New', font=('', 11))

        
        

       
        self.left_frame = tk.Frame(self.root, bg='lightgrey', width=400)  
        self.left_frame.pack(side='left', fill='both', expand=False)

        self.right_frame = tk.Frame(self.root, bg='darkgrey') 
        self.right_frame.pack(side='left', fill='both', expand=True)

        self.style = ttk.Style(self.root)
        self.style.configure("Treeview.Heading", font=('Helvetica', 14, 'bold'))
        self.style.configure("Treeview", font=('Helvetica', 12), rowheight = 25)

        self.tree = ttk.Treeview(self.left_frame)
        self.tree.heading('#0', text='---- Menu Data ----', anchor=tk.CENTER)
        
        self.scrollbar = ttk.Scrollbar(self.left_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side='right', fill='y')
        self.tree.pack(side='left', fill='both', expand=True)
        self.tree.column("#0", width=300)  

        self.build_tree()
    
        self.tree.bind("<Double-1>", self.on_item_selected)

        self.info_label = tk.Label(self.right_frame, text="", bg='darkgrey', fg='white', font=('Helvetica', 16))
        self.info_label.pack(pady=20)

        self.notebook = ttk.Notebook(self.right_frame)
        self.notebook.pack(pady=10, padx=10, expand=True, fill='both')
        self.frame1 = ttk.Frame(self.notebook)
        self.frame2 = ttk.Frame(self.notebook)

        self.frame1.pack(fill='both', expand=True)
        self.frame2.pack(fill='both', expand=True)

        self.notebook.add(self.frame1, text="Item Details")
        self.notebook.add(self.frame2, text="Item Modifers")


        self.itemName_label = ttk.Label(self.frame1, text="Item Name:")
        self.itemName_label.grid(row=0, column=0, padx=11, pady=11)

        self.itemName_entry = ttk.Entry(self.frame1)
        self.itemName_entry.grid(row=0, column=1, padx=11, pady=11)

        self.item_desc_label = ttk.Label(self.frame1, text="Item Description:")
        self.item_desc_label.grid(row=1, column=0, padx=11, pady=11)

        self.item_desc_entry = tk.Text(self.frame1, height=5, width=30)
        self.item_desc_entry.grid(row=1, column=1, padx=11, pady=11)
        

        self.itemPrice_label = ttk.Label(self.frame1, text="Item Price:")
        self.itemPrice_label.grid(row=2, column=0, padx=11, pady=11)

        self.itemPrice_entry = ttk.Entry(self.frame1)
        self.itemPrice_entry.grid(row=2, column=1, padx=11, pady=11)


        self.itemStock_label = ttk.Label(self.frame1, text="Item Stock:")
        self.itemStock_label.grid(row=3, column=0, padx=11, pady=11)

        self.item_stockEntry = ttk.Entry(self.frame1)
        self.item_stockEntry.grid(row=3, column=1, padx=11, pady=11)


        self.itemMenu_Label = ttk.Label(self.frame1, text="Menu:")
        self.itemMenu_Label.grid(row=5, column=0, padx=11, pady=11)

        self.menuLevels = []
        self.fill_menu_opts()
        self.itemMenu_entry = ttk.Combobox(self.frame1, values=self.menuLevels, state='readonly')
        self.itemMenu_entry.grid(row=5, column=1, padx=11, pady=11)
        self.itemMenu_entry.bind("<<ComboboxSelected>>", self.check_menu_sec)

        
        self.menu_secLevel_label = ttk.Label(self.frame1, text="Menu Section:")
        self.menu_secLevel_label.grid(row=6, column=0, padx=11, pady=11)
        self.menu_secLevel_label.grid_remove()

        self.menu_secLevels = []
        self.itemMenuSec_entry = ttk.Combobox(self.frame1, values=self.menu_secLevels, state='readonly')
        self.itemMenuSec_entry.grid(row=6, column=1, padx=11, pady=11)
        self.itemMenuSec_entry.grid_remove()


        self.submit_button = ttk.Button(self.frame1, text="Submit", command=self.submit_menu)
        self.submit_button.grid(row=8, column=0, padx=11, pady=11)

        self.clear_button = ttk.Button(self.frame1, text="Clear", command=self.clear_selection)
        self.clear_button.grid(row=8, column=1, padx=11, pady=11)

        self.delete_button = ttk.Button(self.frame1, text="Delete", command=self.delete_item)
        self.delete_button.grid(row=8, column=3, padx=11, pady=11)
        self.checkUpd = 0
        self.root.mainloop()
    
    def check_menu_sec(self, event = None, parent_menu = None):
        self.query = """SELECT menu_section_name FROM menu_sections
            JOIN menu ON menu_sec_parent = menu_id
            WHERE menu_name = %s
            """
        self.db = "mysqlMenus"
        
        self.connection = create_db_connection(self.db)
        self.results = fetch_query_results(self.query, self.connection, (self.itemMenu_entry.get(),))

        print(parent_menu)
        if self.results != []:
            self.menu_secLevels = []
            for row in self.results:
                self.menu_secLevels.append(row[0])
            self.menu_secLevel_label.grid(row=6, column=0, padx=11, pady=11)
            self.itemMenuSec_entry.grid(row=6, column=1, padx=11, pady=11)
            self.itemMenuSec_entry['values'] = self.menu_secLevels
            print(self.menu_secLevels)
            print(parent_menu)
            self.itemMenuSec_entry.set(self.menu_secLevels[parent_menu - 1])
        else:
            self.menu_secLevels = []
            self.itemMenuSec_entry.set('')
            self.menu_secLevel_label.grid_remove()
            self.itemMenuSec_entry.grid_remove()

        close_out(self.connection)

    def fill_menu_opts(self):
        self.query = ("SELECT * FROM menu")
        self.db = "mysqlMenus"
        
        self.connection = create_db_connection(self.db)
        self.menu_opts = fetch_query_results(self.query, self.connection)
        print(self.menu_opts)
        for row in self.menu_opts:
            self.menuLevels.append(row[1])
        close_out(self.connection)

    def on_item_selected(self, event):
        tree = event.widget

        selected_items = tree.selection()

        if selected_items:  

            item = selected_items[0]
            item_id = re.sub(r'\D', '', item)
            item_text = tree.item(item, 'text')
            print(item_id)
            print(item_text)

            self.query = ("SELECT * FROM menu_items WHERE menu_items_id = %s")
            self.db = "mysqlMenus"
            self.connection = create_db_connection(self.db)
            self.item_selected = fetch_query_results(self.query, self.connection, (item_id,))

            print(self.item_selected)

            self.checkUpd = self.item_selected[0][0]


            self.itemName_entry.delete(0, tk.END)
            self.itemName_entry.insert(0, self.item_selected[0][1])

            self.item_desc_entry.delete('1.0', tk.END)
            self.item_desc_entry.insert('1.0', self.item_selected[0][2])

            self.itemPrice_entry.delete(0, tk.END)
            self.itemPrice_entry.insert(0, self.item_selected[0][3])

            self.item_stockEntry.delete(0, tk.END)
            self.item_stockEntry.insert(0, self.item_selected[0][4])

            self.query = ("SELECT * FROM menu WHERE menu_id = %s")
            self.menu_name = fetch_query_results(self.query, self.connection, (self.item_selected[0][6],))
            self.itemMenu_entry.set(self.menu_name[0][1])

            print(self.item_selected[0][5])
            self.check_menu_sec(None,self.item_selected[0][5])

            self.info_label.config(text= "Making Changes to: " + f'{item_text}')
            self.submit_button.config(text="Update")
        
    def submit_menu(self):
        self.db = "mysqlMenus"
        self.connection = create_db_connection(self.db)

        item_name = self.itemName_entry.get()
        item_desc = self.item_desc_entry.get("1.0", "end-1c")
        item_price = self.itemPrice_entry.get()
        item_stock = self.item_stockEntry.get()
        item_menu = self.menuLevels.index(self.itemMenu_entry.get()) + 1
        if(self.itemMenuSec_entry.get() != ""):
            item_sec = self.menu_secLevels.index(self.itemMenuSec_entry.get()) + 1
        else:
            item_sec = 0


        print(self.checkUpd)
        if self.checkUpd == 0: 
            insert_item_query = """
                INSERT INTO menu_items (menu_item_name, menu_item_desc, menu_item_price, menu_item_stock, menu_item_parent, menu_main)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            execute_query(self.connection, insert_item_query, (item_name, item_desc, item_price, item_stock, item_sec, item_menu))
            

        else:
            update_item_query = """
                UPDATE menu_items
                SET menu_item_name = %s, menu_item_desc = %s, menu_item_price = %s, menu_item_stock = %s, menu_item_parent = %s, menu_main = %s
                WHERE menu_items_id = %s
            """
            execute_query(self.connection, update_item_query, (item_name, item_desc, item_price, item_stock, item_sec, item_menu, self.checkUpd))
            
        self.query = "SELECT * FROM menu_items"
        sql_to_json(self.query, self.connection, "menu_items")
        self.tree.delete(*self.tree.get_children())
        self.build_tree()
        self.clear_selection()

    def build_tree(self):
        self.query = "SELECT * FROM Menu"
        self.db = "mysqlMenus"
        self.connection = create_db_connection(self.db)
        self.menu_list = fetch_query_results(self.query, self.connection)
        self.tree_index = 0
        print("I RAN")
        for menu_row in self.menu_list:
            self.tree.insert('', tk.END, text=str(menu_row[1]), iid='M' + str(menu_row[0]), open=False)

            self.query = "SELECT * FROM menu_sections WHERE menu_sec_parent = " + str(menu_row[0])
            self.section_list = fetch_query_results(self.query, self.connection)
            
            

            for sec_row in self.section_list:
                self.tree.insert('', tk.END, text=str(sec_row[1]), iid='S' + str(sec_row[0]), open=False)
                self.tree.move('S' + str(sec_row[0]), 'M' + str(menu_row[0]), int(sec_row[0]))

                self.query = "SELECT * FROM menu_items WHERE menu_item_parent = " + str(sec_row[0])
                self.item_list = fetch_query_results(self.query, self.connection)

                    
                for item_row in self.item_list:
                    self.tree.insert('', tk.END, text=str(item_row[1]), iid= 'I' + str(item_row[0]), open=False)
                    self.tree.move('I' + str(item_row[0]),'S' + str(sec_row[0]), int(item_row[0]))
        
        self.query = "SELECT * FROM menu_items WHERE menu_item_parent = 0" 
        self.item_list = fetch_query_results(self.query, self.connection)

        for item_row in self.item_list:
            self.tree.insert('', tk.END, text=str(item_row[1]), iid= 'I' + str(item_row[0]), open=False)
            self.tree.move('I' + str(item_row[0]),'M' + str(item_row[6]), int(item_row[0]))

        
        close_out(self.connection)

    def clear_selection(self):
        self.itemName_entry.delete(0, tk.END)
        self.item_desc_entry.delete('1.0', tk.END)
        self.itemPrice_entry.delete(0, tk.END)
        self.item_stockEntry.delete(0, tk.END)

        self.itemMenu_entry.set('')
        self.itemMenuSec_entry.set('')

        self.checkUpd = 0
        self.info_label.config(text="")
        self.submit_button.config(text="Submit")

        self.menu_secLevel_label.grid_remove()
        self.itemMenuSec_entry.grid_remove()

    def delete_item(self):
        self.db = "mysqlMenus"
        self.connection = create_db_connection(self.db)

        if messagebox.askyesno("Delete Item", "Are you sure you want to delete " + self.itemName_entry.get()):
            self.delete_item_query = """
                DELETE FROM menu_items
                WHERE menu_items_id = %s
            """

            execute_query(self.connection, self.delete_item_query, (self.checkUpd,))

            self.tree.delete(*self.tree.get_children())
            self.build_tree()
            self.clear_selection()
            self.db = "mysqlMenus"
            self.connection = create_db_connection(self.db)
            self.query = "SELECT * FROM menu_items"
            sql_to_json(self.query, self.connection, "menu_items")
            

    def sign_out(self):
        close_out(self.connection)
        self.root.destroy()
        AdminLogin()
        
class NewEmployee:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("New Employee")
        self.root.geometry("500x500")

        self.fistName_label = ttk.Label(self.root, text="First Name:")
        self.fistName_label.grid(row=0, column=0, padx=11, pady=11)

        self.firstName_entry = ttk.Entry(self.root)
        self.firstName_entry.grid(row=0, column=1, padx=11, pady=11)


        self.lastName_label = ttk.Label(self.root, text="Last Name:")
        self.lastName_label.grid(row=1, column=0, padx=11, pady=11)

        self.lastName_entry = ttk.Entry(self.root)
        self.lastName_entry.grid(row=1, column=1, padx=11, pady=11)
        

        self.displayName_label = ttk.Label(self.root, text="Display Name:")
        self.displayName_label.grid(row=2, column=0, padx=11, pady=11)

        self.displayName_entry = ttk.Entry(self.root)
        self.displayName_entry.grid(row=2, column=1, padx=11, pady=11)


        self.pinNumber_label = ttk.Label(self.root, text="Pin Number:")
        self.pinNumber_label.grid(row=3, column=0, padx=11, pady=11)

        self.pinNumber_entry = ttk.Entry(self.root)
        self.pinNumber_entry.grid(row=3, column=1, padx=11, pady=11)


        self.pinCode_label = ttk.Label(self.root, text="Pin Code:")
        self.pinCode_label.grid(row=4, column=0, padx=11, pady=11)

        self.pinCode_entry = ttk.Entry(self.root)
        self.pinCode_entry.grid(row=4, column=1, padx=11, pady=11)

        self.accessLevel_label = ttk.Label(self.root, text="Access Level:")
        self.accessLevel_label.grid(row=5, column=0, padx=11, pady=11)

        self.accessLevels = [1, 2, 3, 4, 5]
        self.accessLevel_entry = ttk.Combobox(self.root, values=self.accessLevels, state='readonly')
        self.accessLevel_entry.grid(row=5, column=1, padx=11, pady=11)
        self.accessLevel_entry.set(1)

        self.role_label = ttk.Label(self.root, text="Role:")
        self.role_label.grid(row=6, column=0, padx=11, pady=11)

        self.roles = ['Owner', 'Manager', 'Server', 'Bartender', 'Kitchen', 'Hostess']
        self.role_entry = ttk.Entry(self.root)
        self.role_entry.grid(row=6, column=1, padx=11, pady=11)


        self.submit_button = ttk.Button(self.root, text="Submit", command=self.submit)
        self.submit_button.grid(row=7, column=1, padx=11, pady=11)

        
        self.root.mainloop()



    def submit(self):
        self.db = "mysqlEmployees"
        self.connection = create_db_connection(self.db)

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
        execute_query(self.connection, insert_employees_query, (first_name, last_name, display_name, pin_num, pin_code, access_level, role))
        close_out(self.connection)

        



if __name__ == "__main__":
    AdminLogin()
