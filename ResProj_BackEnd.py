import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from DB_Tables import *
from tkinter import messagebox
import re
import requests
from requests.exceptions import ConnectionError

# When this function is called, instead of polling, the backend can send an request to Flask for the JSON files to be 
# loaded again on the webpage.
def updateJsonFiles():
    url = 'http://localhost:5000/notify_update' 
    try:
        response = requests.post(url, timeout=1)
        if response.status_code == 200:
            print("Update was made.")

    except ConnectionError:
        print("Failed to connect to the server. The server may be offline.")
        return 

# Class that is used to create the first window that starts up, the login window
# region Login
class AdminLogin: 
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x250")
        self.root.resizable(False, False)
        self.root.title('Log-In')


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

        self.user_enter_field = ttk.Entry(self.signin, textvariable=self.user_enter)
        self.user_enter_field.pack(fill='x', expand=True)
        self.user_enter_field.focus()

        self.password_label = ttk.Label(self.signin, text="Password:")
        self.password_label.pack(fill='x', expand=True)

        self.password_entry = ttk.Entry(self.signin, textvariable=self.user_pass, show="*")
        self.password_entry.pack(fill='x', expand=True)

        self.login_button = ttk.Button(self.signin, text="Login", command=self.login_attempt)
        self.login_button.pack(fill='x', expand=True, pady=10)

        self.cancel_button = ttk.Button(self.signin, text="Cancel", command=self.root.destroy)
        self.cancel_button.pack(fill='x', expand=True, pady=10)

        self.admin_button = ttk.Button(self.signin, text="Admin Log-In", state='', command=self.admin_logIn)
        self.admin_button.pack(fill='x', expand=True, pady=10)


        self.root.mainloop()

    def login_attempt(self):

        if self.user_enter.get() == '':
            messagebox.showerror("User Name Empty", "Please enter a User Name.")
            return
        elif self.user_pass.get() == '':
            messagebox.showerror("Password  Empty", "Please enter a Password.")
            return
        else:
            
            emp_DAO = Employees_TableDAO('mysqlEmployees')
            emp_ADMIN = emp_DAO.fetch_admins()

            
            for row in emp_ADMIN:
                if self.user_enter.get().strip() == str(row.pin_num) and self.user_pass.get().strip() == str(row.pin_code):
                    messagebox.showinfo("Signed In", "Signed in as " + row.display_name)
                    self.root.destroy()
                    emp_DAO.close()
                    mainWindow(row.display_name)
                    return
                
            messagebox.showerror("Invaild Login", "Invaild User Name and/or Password")
            self.user_pass.set("")

    def admin_logIn(self):
        self.root.destroy()
        mainWindow("ADMIN")
        return
# endregion

# region Main Window
class mainWindow:
    def __init__(self, name):
                
        self.root = tk.Tk()
        self.root.title("Resturant Back-End" + " | Signed in as " + str(name))
        self.root.geometry('1000x750')
        self.root.state('zoomed')
        self.root.iconbitmap('./images/favicon.ico')
        self.current_window = "menu"


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

        
        self.top_frame = tk.Frame(self.root, bg='lightgray', height=75)  
        self.top_frame.pack(side='top', fill='both', expand=False)

        self.menu_image = PhotoImage(file="./images/favicon_64x64.png")
        self.menu_button = tk.Button(self.top_frame, image=self.menu_image, width=75, height=100, text="Menu Setup", compound='top', padx=10, pady=10, font='bold, 12', command= self.menu_Window)
        self.menu_button.pack(padx=10, pady=5, side='left')

        self.employee_image = PhotoImage(file="./images/red_employee_favicon_64x64.png")
        self.employee_button = tk.Button(self.top_frame, image=self.employee_image, width=75, height=100, text="Employees", compound='top', padx=10, pady=10, font='bold, 12', command=self.employee_Window)
        self.employee_button.pack(padx=10, pady=5, side='left')

        self.shift_image = PhotoImage(file="./images/timeMange_64x64.png")
        self.shift_button = tk.Button(self.top_frame, image=self.shift_image, width=75, height=100, text="Time\nManagment", compound='top', padx=10, pady=10, font='bold, 12')
        self.shift_button.pack(padx=10, pady=5, side='left')

        self.left_frame = tk.Frame(self.root, bg='lightgrey', width=400)  
        self.left_frame.pack(side='left', fill='both', expand=False)

        self.right_frame = tk.Frame(self.root, bg='darkgrey') 
        self.right_frame.pack(side='left', fill='both', expand=True)

        Menu_Window(self.root, self.top_frame, self.right_frame, self.left_frame)
        self.root.mainloop()

    def employee_Window(self):
        if self.current_window == "employee":
            return
        else: 
            self.current_window = "employee"
            self.left_frame.destroy()
            self.right_frame.destroy()

        self.left_frame = tk.Frame(self.root, bg='lightgrey', width=400)  
        self.right_frame = tk.Frame(self.root, bg='darkgrey') 

        EmployeeWindow(self.right_frame, self.left_frame, self.top_frame)


    def menu_Window(self):
        if self.current_window == "menu":
            return
        else: 
            self.current_window = "menu"
            self.left_frame.destroy()
            self.right_frame.destroy()
        
        self.left_frame = tk.Frame(self.root, bg='lightgrey', width=400)  
        self.right_frame = tk.Frame(self.root, bg='darkgrey') 

        Menu_Window(self.root, self.top_frame, self.right_frame, self.left_frame)

    def sign_out(self):
        
        self.root.destroy()
        AdminLogin()
# endregion

# region Menu Window
class Menu_Window: 
    def __init__(self, main_Root, main_TopFrame, main_RightFrame, main_LeftFrame):
        self.top_frame = main_TopFrame
        self.root = main_Root
        self.right_frame = main_RightFrame
        self.left_frame = main_LeftFrame

        self.left_frame.pack(side='left', fill='both', expand=False)
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

        self.info_label = tk.Label(self.right_frame, bg='darkgrey', width=75, height=2)
        self.info_label.pack(pady=20)

        self.style=ttk.Style(self.root)
        self.style.configure('Bold.TNotebook.Tab', font=('Helvetica', 12), padding=(10, 2, 10, 2))

        self.notebook = ttk.Notebook(self.right_frame, style='Bold.TNotebook')
        self.notebook.pack(pady=10, padx=10, expand=True, fill='both')
        self.frame3 = ttk.Frame(self.notebook)
        self.frame1 = ttk.Frame(self.notebook)
        self.frame2 = ttk.Frame(self.notebook)

        self.frame3.pack(fill='both', expand=True)
        self.frame1.pack(fill='both', expand=True)
        self.frame2.pack(fill='both', expand=True)

        
        self.notebook.add(self.frame1, text="Menu Details")
        self.notebook.add(self.frame2, text="Menu Section Details")
        self.notebook.add(self.frame3, text="Item Details")

        ###### Frames ######
        
        self.frame_One = FrameOne(self.frame1, self.info_label, self)
        self.frame_Two = FrameTwo(self.frame2, self.info_label, self)
        self.frame_Three = FrameThree(self.frame3, self.info_label, self)

        


    def on_item_selected(self, event):
        self.approve_clear()
        tree = event.widget
        selected_items = tree.selection()

        if selected_items:  
            item = selected_items[0]
            tree_id = re.sub(r'\D', '', item)
            tree_text = tree.item(item, 'text')
            print(f"ID: {tree_id} | Name: {tree_text} | Code: {item[0]}")

            if item[0] == 'M':
                self.notebook.select(0)
                self.frame_One.handle_menu_sel(tree_id)
                
            elif item[0] == 'S':

                self.notebook.select(1)
                self.frame_Two.handle_sec_sel(tree_id)

            elif item[0] == 'I':
                self.notebook.select(2)
                self.frame_Three.handle_item_sel(tree_id)
            
            else:
                print("Error selecting Item")
        

    def build_tree(self):
        self.tree.delete(*self.tree.get_children())
        menu_DAO = Menu_TableDAO('mysqlMenus')
        menu_ALL = menu_DAO.fetch_all_menus()
        for menu_row in menu_ALL:
            self.tree.insert('', tk.END, text=str(menu_row.menu_name), iid='M' + str(menu_row.menu_id), open=False)
        menu_DAO.close()


        menuSec_DAO = MenuSections_TableDAO('mysqlMenus')
        menuSec_ALL = menuSec_DAO.fetch_all_sections()
        for menuSec_row in menuSec_ALL:
            self.tree.insert('', tk.END, text=str(menuSec_row.menu_section_name), iid='S' + str(menuSec_row.menu_section_id), open=False)
            self.tree.move('S' + str(menuSec_row.menu_section_id), 'M' + str(menuSec_row.menu_sec_parent), int(menuSec_row.menu_section_id))
        menuSec_DAO.close()

        
        menuItem_DAO = MenuItems_TableDAO('mysqlMenus')
        menuItem_ALL = menuItem_DAO.fetch_all_items()
        for menuItm_row in menuItem_ALL:
            self.tree.insert('', tk.END, text=str(menuItm_row.menu_item_name), iid='I' + str(menuItm_row.menu_items_id), open=False)

            if menuItm_row.menu_item_parent != 0:
                self.tree.move('I' + str(menuItm_row.menu_items_id),'S' + str(menuItm_row.menu_item_parent), int(menuItm_row.menu_items_id))

            else:
                self.tree.move('I' + str(menuItm_row.menu_items_id),'M' + str(menuItm_row.menu_main), int(menuItm_row.menu_items_id))
        menuItem_DAO.close()

    def approve_clear(self):
        self.frame_One.clear_selection()
        self.frame_Two.clear_selection()
        self.frame_Three.clear_selection()
# endregion

# region Menu Frame
class FrameOne:
    def __init__(self, frame1, info_label, main_window):
        self.info_label = info_label
        self.main_window = main_window

        self.menuName_label = ttk.Label(frame1, text="Menu Name:")
        self.menuName_label.grid(row=0, column=0, padx=11, pady=11)

        self.menuName_entry = ttk.Entry(frame1)
        self.menuName_entry.grid(row=0, column=1, padx=11, pady=11)

        self.menuStrt_label = ttk.Label(frame1, text="Menu Start/End Time:")
        self.menuStrt_label.grid(row=1, column=0, padx=5, pady=5)

        self.menuStrt_levels = ['9am', '10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm', '10pm']
        self.menuStrt_Entry = ttk.Combobox(frame1, values=self.menuStrt_levels, width=10, state='readonly')
        self.menuStrt_Entry.grid(row=1, column=1, padx=5, pady=5)
        self.menuStrt_Entry.bind("<<ComboboxSelected>>", self.check_end_time)

        self.menuEnd_levels = []
        self.menuEnd_Entry = ttk.Combobox(frame1, values=self.menuEnd_levels, width=10, state='readonly')
        self.menuEnd_Entry.grid(row=1, column=2, padx=5, pady=5)
        self.menuEnd_Entry.grid_remove()

        self.menuDays_label = ttk.Label(frame1, text='Menu Days')
        self.menuDays_label.grid(row=2, column=0, padx=5, pady=5)

        self.menuDays_opts = ['Every Day|All', 'Monday|Mon', 'Tuesday|Tues', 'Wednesday|Wed', 'Thursday|Thurs', 'Friday|Fri', 'Saturday|Sat', 'Sunday|Sun']
        self.day_vars = {day.split('|')[0]: tk.BooleanVar() for day in self.menuDays_opts}
        self.everyday_var = tk.BooleanVar()
        self.day_checkbuttons = []


        self.row = 2
        for day_option in self.menuDays_opts:
            day, abbr = day_option.split('|')
            if day == 'Every Day':
                cb = tk.Checkbutton(frame1, text=day, variable=self.everyday_var, command=self.lock_days)
            else:
                cb = tk.Checkbutton(frame1, text=day, variable=self.day_vars[day])
                self.day_checkbuttons.append(cb) 
            cb.grid(row=self.row, column=1, sticky=tk.W)
            self.row += 1

        
        self.checkUpd = 0
        self.submit_button = ttk.Button(frame1, text="Submit", command=self.insert_menu)
        self.submit_button.grid(row=10, column=0, padx=11, pady=11)

        self.clear_button = ttk.Button(frame1, text="Clear", command=self.clear_selection)
        self.clear_button.grid(row=10, column=1, padx=11, pady=11)

        self.delete_button = ttk.Button(frame1, text="Delete", command=self.delete_menu)
        self.delete_button.grid(row=10, column=2, padx=11, pady=11)


    def lock_days(self):
        if self.everyday_var.get():
            for cb, day in zip(self.day_checkbuttons, self.menuDays_opts[1:]):
                day_name = day.split('|')
                self.day_vars[day_name[0]].set(False) 
                cb.config(state=tk.DISABLED)
                
        else:
            for cb in self.day_checkbuttons:
                cb.config(state=tk.NORMAL)


    def check_end_time(self, event = None):
        self.menuEnd_levels = []
        self.menuEnd_Entry.set('')
        
        for time in self.menuStrt_levels[self.menuStrt_levels.index(self.menuStrt_Entry.get()) + 1:]:
            self.menuEnd_levels.append(time)

        self.menuEnd_levels.append('11pm')
        self.menuEnd_Entry['values'] = self.menuEnd_levels
        self.menuEnd_Entry.grid(row=1, column=2, padx=5, pady=5)
    

    def handle_menu_sel(self, tree_id):
        menu_DAO = Menu_TableDAO('mysqlMenus')
        menu_byID = menu_DAO.fetch_menu_by_id(tree_id)
        self.checkUpd = menu_byID.menu_id


        self.menuName_entry.delete(0, tk.END)
        self.menuName_entry.insert(0, menu_byID.menu_name)

        self.menuStrt_Entry.set(menu_byID.menu_start_time)
        self.check_end_time()
        self.menuEnd_Entry.set(menu_byID.menu_end_time)

        for day_var in self.day_vars.values():
            day_var.set(False)
        if self.everyday_var.get():
            self.everyday_var.set(False)
            self.lock_days()
        

        daysplit = menu_byID.menu_days.split(',')
        for item in self.menuDays_opts:
            day, abbr = item.split('|')
            if abbr in daysplit:
                if abbr == 'All':
                    self.everyday_var.set(True)
                    self.lock_days()
                    break
                else:
                    self.day_vars[day].set(True)
        
        self.submit_button.config(text='Update')
        self.info_label.config(text= "Making Changes to: " + f'{menu_byID.menu_name}')
        self.info_label.config(bg='orange', fg='black', font=('Helvetica', 16), width=75, height=2, borderwidth=3, relief="groove")
    
    def clear_selection(self):
        self.menuName_entry.delete(0, tk.END)
        self.menuStrt_Entry.set('')
        self.menuEnd_Entry.set('')

        self.everyday_var.set(False)
        for cb, day in zip(self.day_checkbuttons, self.menuDays_opts[1:]):
                day_name = day.split('|')
                self.day_vars[day_name[0]].set(False) 
                cb.config(state=tk.NORMAL)
        

        self.checkUpd = 0
        self.info_label.config(bg='darkgrey', width=75, height=2, text='', borderwidth=0, relief="flat")
        self.submit_button.config(text="Submit")

        self.menuEnd_Entry.grid_remove()

    def insert_menu(self):
        Menu_DAO = Menu_TableDAO('mysqlMenus')

        menu_name = self.menuName_entry.get()
        menu_start_time = self.menuStrt_Entry.get()
        menu_end_time = self.menuEnd_Entry.get()
        menu_days = ''
        
        if self.everyday_var.get() == True:
            menu_days = 'All'
        else:
            for day in self.menuDays_opts:
                day_name = day.split('|')
                    
                if self.day_vars[day_name[0]].get() == True:
                    if menu_days == '':
                        menu_days += day_name[1]
                    else: 
                        menu_days += "," + day_name[1]
                
        if len(menu_days) == 36:
            menu_days = "All"

        if self.checkUpd == 0: 
            Menu_DAO.insert_menu(menu_name, menu_start_time, menu_end_time, menu_days)
            
        else:
            Menu_DAO.update_menu_by_id(menu_name, menu_start_time, menu_end_time, menu_days, self.checkUpd)

        self.main_window.frame_Three.fill_menu_opts()
        self.main_window.build_tree()
        Menu_DAO.menus_to_json()
        
        self.clear_selection()
        Menu_DAO.close()

    def delete_menu(self):
        Menu_DAO = Menu_TableDAO('mysqlMenus')
        menu_byID = Menu_DAO.fetch_menu_by_id(self.checkUpd)
        
        if messagebox.askyesno("Delete Menu", "Are you sure you want to delete " + menu_byID.menu_name):

            Menu_DAO.delete_menu_by_id(menu_byID.menu_id)

            self.main_window.frame_Three.fill_menu_opts()
            self.main_window.build_tree()
            self.clear_selection()
            Menu_DAO.menus_to_json()
            Menu_DAO.close()
# endregion

# region Meni Section Frame
class FrameTwo:
    def __init__(self, frame2, info_label, main_window):
        self.info_label = info_label
        self.main_window = main_window
        
        self.secName_label = ttk.Label(frame2, text="Section Name:")
        self.secName_label.grid(row=0, column=0, padx=11, pady=11)

        self.secName_entry = ttk.Entry(frame2)
        self.secName_entry.grid(row=0, column=1, padx=11, pady=11)

        self.parMenu_Label = ttk.Label(frame2, text="Parent Menu:")
        self.parMenu_Label.grid(row=1, column=0, padx=11, pady=11)

        self.menuLevels = []
        self.patMenu_entry = ttk.Combobox(frame2, values=self.menuLevels, state='readonly')
        self.patMenu_entry.grid(row=1, column=1, padx=11, pady=11)
        self.fill_menu_opts()

        self.submit_button = ttk.Button(frame2, text="Submit", command=self.insert_section)
        self.submit_button.grid(row=8, column=0, padx=11, pady=11)

        self.clear_button = ttk.Button(frame2, text="Clear", command=self.clear_selection)
        self.clear_button.grid(row=8, column=1, padx=11, pady=11)

        self.delete_button = ttk.Button(frame2, text="Delete", command=self.delete_section)
        self.delete_button.grid(row=8, column=3, padx=11, pady=11)
        self.checkUpd = 0
    


    def fill_menu_opts(self):
        
        self.menuLevels = []
        menu_DAO = Menu_TableDAO('mysqlMenus')
        menu_ALL = menu_DAO.fetch_all_menus()

        for menu in menu_ALL:
            self.menuLevels.append(menu.menu_name)
        
        menu_DAO.close()

        self.patMenu_entry['values'] = self.menuLevels
    
    def handle_sec_sel(self, tree_id):

        menuSec_DAO = MenuSections_TableDAO('mysqlMenus')
        menuSec_byID = menuSec_DAO.fetch_menuSection_by_id(tree_id)

        menu_DAO = Menu_TableDAO('mysqlMenus')
        menu_byID = menu_DAO.fetch_menu_by_id(menuSec_byID.menu_sec_parent)

        self.checkUpd = menuSec_byID.menu_section_id


        self.secName_entry.delete(0, tk.END)
        self.secName_entry.insert(0, menuSec_byID.menu_section_name)

        self.patMenu_entry.set(menu_byID.menu_name)

        self.submit_button.config(text='Update')
        self.info_label.config(text= "Making Changes to: " + f'{menuSec_byID.menu_section_name}')
        self.info_label.config(bg='orange', fg='black', font=('Helvetica', 16), width=75, height=2, borderwidth=3, relief="groove")

        menuSec_DAO.close()
        menu_DAO.close()


    
    def clear_selection(self):
        self.secName_entry.delete(0, tk.END)
        self.patMenu_entry.set('')

        self.checkUpd = 0

        self.info_label.config(bg='darkgrey', width=75, height=2, text='', borderwidth=0, relief="flat")
        self.submit_button.config(text="Submit")
    
    def insert_section(self):
        menuSec_DAO = MenuSections_TableDAO('mysqlMenus')

        menu_DAO = Menu_TableDAO('mysqlMenus')
        menuDAO_byNAME = menu_DAO.fetch_menu_by_name(self.patMenu_entry.get())

        menu_section_name = self.secName_entry.get()
        menu_sec_parent = menuDAO_byNAME.menu_id

        print(self.checkUpd)
        if self.checkUpd == 0: 
            menuSec_DAO.insert_section(menu_section_name, menu_sec_parent)
        
        else:
            menuSecDAO_byID = menuSec_DAO.fetch_menuSection_by_id(self.checkUpd)

            menuItem_DAO = MenuItems_TableDAO('mysqlMenus')
            menuItemDAO_bySEC = menuItem_DAO.fetch_items_by_section(self.checkUpd)
            
            if menuSecDAO_byID.menu_sec_parent == menuDAO_byNAME.menu_id or len(menuItemDAO_bySEC) == 0:
                menuSec_DAO.update_sec_by_id(menu_section_name, menu_sec_parent, self.checkUpd)
            
            else:
                if messagebox.askyesno("Move Section", "WARNING: Updating " + menu_section_name + " will move " + str(len(menuItemDAO_bySEC)) + " item(s).\n"
                                        + "\n\tContinue?"):
                    pass


        self.main_window.build_tree()
        self.clear_selection()

        menuSec_DAO.close()
        menu_DAO.close()


    def delete_section(self):
        pass
# endregion

#region Menu Items Frame
class FrameThree:
    def __init__(self, frame3, info_label, main_window):
        self.info_label = info_label
        self.main_window = main_window

        self.itemName_label = ttk.Label(frame3, text="Item Name:")
        self.itemName_label.grid(row=0, column=0, padx=11, pady=11)

        self.itemName_entry = ttk.Entry(frame3)
        self.itemName_entry.grid(row=0, column=1, padx=11, pady=11)

        self.item_desc_label = ttk.Label(frame3, text="Item Description:")
        self.item_desc_label.grid(row=1, column=0, padx=11, pady=11)

        self.item_desc_entry = tk.Text(frame3, height=5, width=30)
        self.item_desc_entry.grid(row=1, column=1, padx=11, pady=11)
        

        self.itemPrice_label = ttk.Label(frame3, text="Item Price:")
        self.itemPrice_label.grid(row=2, column=0, padx=11, pady=11)

        self.itemPrice_entry = ttk.Entry(frame3)
        self.itemPrice_entry.grid(row=2, column=1, padx=11, pady=11)


        self.itemStock_label = ttk.Label(frame3, text="Item Stock:")
        self.itemStock_label.grid(row=3, column=0, padx=11, pady=11)

        self.item_stockEntry = ttk.Entry(frame3)
        self.item_stockEntry.grid(row=3, column=1, padx=11, pady=11)


        self.itemMenu_Label = ttk.Label(frame3, text="Menu:")
        self.itemMenu_Label.grid(row=5, column=0, padx=11, pady=11)

        self.menuLevels = []
        self.itemMenu_entry = ttk.Combobox(frame3, values=self.menuLevels, state='readonly')
        self.itemMenu_entry.grid(row=5, column=1, padx=11, pady=11)
        self.itemMenu_entry.bind("<<ComboboxSelected>>", self.check_menu_sec)
        self.fill_menu_opts()

        
        self.menu_secLevel_label = ttk.Label(frame3, text="Menu Section:")
        self.menu_secLevel_label.grid(row=6, column=0, padx=11, pady=11)
        self.menu_secLevel_label.grid_remove()

        self.menu_secLevels = []
        self.itemMenuSec_entry = ttk.Combobox(frame3, values=self.menu_secLevels, state='readonly')
        self.itemMenuSec_entry.grid(row=6, column=1, padx=11, pady=11)
        self.itemMenuSec_entry.grid_remove()


        self.submit_button = ttk.Button(frame3, text="Submit", command=self.insert_item)
        self.submit_button.grid(row=8, column=0, padx=11, pady=11)

        self.clear_button = ttk.Button(frame3, text="Clear", command=self.clear_selection)
        self.clear_button.grid(row=8, column=1, padx=11, pady=11)

        self.delete_button = ttk.Button(frame3, text="Delete", command=self.delete_item)
        self.delete_button.grid(row=8, column=3, padx=11, pady=11)
        self.checkUpd = 0


    def handle_item_sel(self, tree_id):
        menuItem_DAO = MenuItems_TableDAO('mysqlMenus')
        menuItem_byID = menuItem_DAO.fetch_item_by_id(tree_id)
        

        self.checkUpd = menuItem_byID.menu_items_id


        self.itemName_entry.delete(0, tk.END)
        self.itemName_entry.insert(0, menuItem_byID.menu_item_name)

        self.item_desc_entry.delete('1.0', tk.END)
        self.item_desc_entry.insert('1.0', menuItem_byID.menu_item_desc)

        self.itemPrice_entry.delete(0, tk.END)
        self.itemPrice_entry.insert(0, menuItem_byID.menu_item_price)

        self.item_stockEntry.delete(0, tk.END)
        self.item_stockEntry.insert(0, menuItem_byID.menu_item_stock)


        menu_DAO = Menu_TableDAO('mysqlMenus')
        menu_byID = menu_DAO.fetch_menu_by_id(menuItem_byID.menu_main)
        self.itemMenu_entry.set(menu_byID.menu_name)

        self.check_menu_sec(None, menuItem_byID.menu_item_parent)

        self.info_label.config(text= "Making Changes to: " + f'{menuItem_byID.menu_item_name}')
        self.info_label.config(bg='orange', fg='black', font=('Helvetica', 16), width=75, height=2, borderwidth=3, relief="groove")

        self.submit_button.config(text="Update")
        menuItem_DAO.close()


    def check_menu_sec(self, event = None, setMen = None):
        self.menu_secLevels = []
        menuSecJ_DAO = MenuSec_Join_Menu_TableDAO('mysqlMenus')
        menuSec_byMID = menuSecJ_DAO.join_menuSections_menuName(self.itemMenu_entry.get())

        if menuSec_byMID != []:
            self.menu_secLevel_label.grid(row=6, column=0, padx=11, pady=11)
            self.itemMenuSec_entry.grid(row=6, column=1, padx=11, pady=11)
            for section in menuSec_byMID:
                self.menu_secLevels.append(section.menu_section_name)
                if setMen == section.menu_section_id:
                    setMen = section.menu_section_name
            
            self.itemMenuSec_entry['values'] = self.menu_secLevels
            if setMen:
                self.itemMenuSec_entry.set(setMen)
        

        else:
            self.itemMenuSec_entry.set('')
            self.menu_secLevel_label.grid_remove()
            self.itemMenuSec_entry.grid_remove()
        
        menuSecJ_DAO.close()


    def fill_menu_opts(self):
        
        self.menuLevels = []
        menu_DAO = Menu_TableDAO('mysqlMenus')
        menu_ALL = menu_DAO.fetch_all_menus()

        for menu in menu_ALL:
            self.menuLevels.append(menu.menu_name)
        
        menu_DAO.close()

        self.itemMenu_entry['values'] = self.menuLevels

    def insert_item(self):
        menuItem_DAO = MenuItems_TableDAO('mysqlMenus')

        menu_DAO = Menu_TableDAO('mysqlMenus')
        menuDAO_byNAME = menu_DAO.fetch_menu_by_name(self.itemMenu_entry.get())

        item_name = self.itemName_entry.get()
        item_desc = self.item_desc_entry.get("1.0", "end-1c")
        item_price = self.itemPrice_entry.get()
        item_stock = self.item_stockEntry.get()
        item_menu = menuDAO_byNAME.menu_id

        if self.itemMenuSec_entry.get() != "":
            menuSection_DAO = MenuSections_TableDAO('mysqlMenus')
            menuSectionDAO_byNAME = menuSection_DAO.fetch_section_by_name(self.itemMenuSec_entry.get())
            item_sec = menuSectionDAO_byNAME.menu_section_id
        else:
            item_sec = 0


        print(self.checkUpd)
        if self.checkUpd == 0: 
            menuItem_DAO.insert_item(item_name, item_desc, item_price, item_stock, item_sec, item_menu)
            
        else:
            menuItem_DAO.update_item_by_id(item_name, item_desc, item_price, item_stock,  item_sec, item_menu, self.checkUpd)

        self.main_window.build_tree()
        menuItem_DAO.menuItems_to_json()
        updateJsonFiles()
        self.clear_selection()
        menuItem_DAO.close()
        menu_DAO.close()


    def clear_selection(self):
        self.itemName_entry.delete(0, tk.END)
        self.item_desc_entry.delete('1.0', tk.END)
        self.itemPrice_entry.delete(0, tk.END)
        self.item_stockEntry.delete(0, tk.END)

        self.itemMenu_entry.set('')
        self.itemMenuSec_entry.set('')

        self.checkUpd = 0
        self.info_label.config(bg='darkgrey', width=75, height=2, text='', borderwidth=0, relief="flat")
        self.submit_button.config(text="Submit")

        self.menu_secLevel_label.grid_remove()
        self.itemMenuSec_entry.grid_remove()

    def delete_item(self):
        menuItem_DAO = MenuItems_TableDAO('mysqlMenus')
        menuItem_byID = menuItem_DAO.fetch_item_by_id(self.checkUpd)
        
        if messagebox.askyesno("Delete Item", "Are you sure you want to delete " + menuItem_byID.menu_item_name):

            menuItem_DAO.delete_item_by_id(menuItem_byID.menu_items_id)

            self.main_window.build_tree()
            self.clear_selection()
            menuItem_DAO.menuItems_to_json()
            menuItem_DAO.close()
            updateJsonFiles()
# endregion


class NewEmployee:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("New Employee")
        self.root.geometry("500x500")

        
        self.root.mainloop()



    

# region Employee Window
class EmployeeWindow:
    def __init__(self, main_RightFrame, main_LeftFrame, main_TopFrame):
        self.left_frame = main_LeftFrame
        self.right_frame = main_RightFrame

        self.left_frame.pack(side='left', fill='both', expand=False)
        self.right_frame.pack(side='left', fill='both', expand=True)
        

        self.tree = ttk.Treeview(self.right_frame, columns=("ID", "FirstName", "LastName", "DisplayName", "PinNum", "PinCode", "AccessLevel", "Role"), show="headings")
        self.tree.heading("ID", text="Database ID")
        self.tree.heading("FirstName", text="First Name")
        self.tree.heading("LastName", text="Last Name")
        self.tree.heading("DisplayName", text="Display Name")
        self.tree.heading("PinNum", text="Pin Number")
        self.tree.heading("PinCode", text="Pin Code")
        self.tree.heading("AccessLevel", text="Access Level")
        self.tree.heading("Role", text="Role")


        self.tree.pack(fill=tk.BOTH, expand=True)

        self.build_tree()
        self.tree.bind("<Double-1>", self.on_item_selected)
        self.updateCheck = -1

        self.emplInsert_label = ttk.Label(self.left_frame, text="Employee", font=('', 24), width=15,anchor='center', background='orange', borderwidth=3, relief='ridge')
        self.emplInsert_label.grid(row=0, column=0, columnspan=2, padx=11, pady=11)



        self.fistName_label = ttk.Label(self.left_frame, text="First Name:")
        self.fistName_label.grid(row=1, column=0, padx=11, pady=11)

        self.firstName_entry = ttk.Entry(self.left_frame)
        self.firstName_entry.grid(row=1, column=1, padx=11, pady=11)


        self.lastName_label = ttk.Label(self.left_frame, text="Last Name:")
        self.lastName_label.grid(row=2, column=0, padx=11, pady=11)

        self.lastName_entry = ttk.Entry(self.left_frame)
        self.lastName_entry.grid(row=2, column=1, padx=11, pady=11)
        

        self.displayName_label = ttk.Label(self.left_frame, text="Display Name:")
        self.displayName_label.grid(row=3, column=0, padx=11, pady=11)

        self.displayName_entry = ttk.Entry(self.left_frame)
        self.displayName_entry.grid(row=3, column=1, padx=11, pady=11)


        self.pinNumber_label = ttk.Label(self.left_frame, text="Pin Number:")
        self.pinNumber_label.grid(row=4, column=0, padx=11, pady=11)

        self.pinNumber_entry = ttk.Entry(self.left_frame)
        self.pinNumber_entry.grid(row=4, column=1, padx=11, pady=11)


        self.pinCode_label = ttk.Label(self.left_frame, text="Pin Code:")
        self.pinCode_label.grid(row=5, column=0, padx=11, pady=11)

        self.pinCode_entry = ttk.Entry(self.left_frame)
        self.pinCode_entry.grid(row=5, column=1, padx=11, pady=11)

        self.accessLevel_label = ttk.Label(self.left_frame, text="Access Level:")
        self.accessLevel_label.grid(row=6, column=0, padx=11, pady=11)

        self.accessLevels = [1, 2, 3, 4, 5]
        self.accessLevel_entry = ttk.Combobox(self.left_frame, values=self.accessLevels, state='readonly')
        self.accessLevel_entry.grid(row=6, column=1, padx=11, pady=11)
        

        self.role_label = ttk.Label(self.left_frame, text="Role:")
        self.role_label.grid(row=7, column=0, padx=11, pady=11)

        self.roles = ['Owner', 'Manager', 'Server', 'Bartender', 'Kitchen', 'Hostess', 'Busser', 'Doorman', 'Barback', 'Maintenance', 'Dishwasher', 'Food-Runner', 'Expeditor']
        self.role_entry = ttk.Combobox(self.left_frame, values=self.roles, state='readonly')
        self.role_entry.grid(row=7, column=1, padx=11, pady=11)
        self.role_entry.set('')


        self.submit_button = ttk.Button(self.left_frame, text="Submit", command=self.submit)
        self.submit_button.grid(row=8, column=0, padx=11, pady=11)

        self.clr_button = ttk.Button(self.left_frame, text="Clear", command=self.clearVals)
        self.clr_button.grid(row=8, column=1, padx=11, pady=11)

        self.del_button = ttk.Button(self.left_frame, text="Delete", command=self.delEmployee)


    def on_item_selected(self, event):
        tree = event.widget
        selected_items = tree.selection()

        if selected_items:  
            item_id = selected_items[0]
            item_values = tree.item(item_id, 'values')
            self.updateCheck = item_values[0]

            self.submit_button.config(text='Update')
            self.del_button.grid(row=9, column=1, padx=11, pady=11)

            employeeDAO = Employees_TableDAO("mysqlEmployees")
            employeeDAO_byID = employeeDAO.fetch_employee_by_Id(item_values[0])
            employeeDAO.close()

            self.firstName_entry.delete(0, tk.END)
            self.firstName_entry.insert(0, employeeDAO_byID.first_name)

            self.lastName_entry.delete(0, tk.END)
            self.lastName_entry.insert(0, employeeDAO_byID.last_name)

            self.displayName_entry.delete(0, tk.END)
            self.displayName_entry.insert(0, employeeDAO_byID.display_name)

            self.pinNumber_entry.delete(0, tk.END)
            self.pinNumber_entry.insert(0, employeeDAO_byID.pin_num)

            self.pinCode_entry.delete(0, tk.END)
            self.pinCode_entry.insert(0, employeeDAO_byID.pin_code)

            self.pinCode_entry.delete(0, tk.END)
            self.pinCode_entry.insert(0, employeeDAO_byID.pin_code)

            self.accessLevel_entry.set(employeeDAO_byID.access_level)

            self.role_entry.set(employeeDAO_byID.role)

            print(item_values)
    
    def submit(self):
        
        employeeDAO = Employees_TableDAO("mysqlEmployees")

        first_name = self.firstName_entry.get()
        last_name = self.lastName_entry.get()
        display_name = self.displayName_entry.get()
        pin_num = self.pinNumber_entry.get()
        pin_code = self.pinCode_entry.get()
        access_level = self.accessLevel_entry.get()
        role = self.role_entry.get()

        if self.updateCheck == -1:
            employeeDAO.insert_employee(first_name, last_name, display_name, pin_num, pin_code, access_level, role)
        else:
            employeeDAO.update_employee_by_id(first_name, last_name, display_name, pin_num, pin_code, access_level, role, self.updateCheck)
        employeeDAO.close()
        self.build_tree()
        self.clearVals()
        updateJsonFiles()
    
    def clearVals(self):
        self.firstName_entry.delete(0, tk.END)

        self.lastName_entry.delete(0, tk.END)

        self.displayName_entry.delete(0, tk.END)

        self.pinNumber_entry.delete(0, tk.END)

        self.pinCode_entry.delete(0, tk.END)

        self.pinCode_entry.delete(0, tk.END)

        self.accessLevel_entry.set('')

        self.role_entry.set('')

        self.updateCheck = -1
        self.submit_button.config(text='Submit')
        self.del_button.grid_remove()

    def delEmployee(self):
        employeeDAO = Employees_TableDAO("mysqlEmployees")
        employeeDAO_byID = employeeDAO.fetch_employee_by_Id(self.updateCheck)
        
        if messagebox.askyesno("Delete Item", "Are you sure you want to delete " + employeeDAO_byID.display_name):

            employeeDAO.delete_employee_by_id(self.updateCheck)
            employeeDAO.close()
            self.clearVals()
            self.build_tree()
            updateJsonFiles()

    def build_tree(self):
        self.tree.delete(*self.tree.get_children())
        employeeDAO = Employees_TableDAO("mysqlEmployees")
        employeeALL_DAO = employeeDAO.fetch_all_employees()
        employeeDAO.close()

        for employee in employeeALL_DAO:
            self.tree.insert("", tk.END, values=(employee.employee_id, employee.first_name, employee.last_name, employee.display_name, employee.pin_num, employee.pin_code, employee.access_level, employee.role))

        
# endregion

if __name__ == "__main__":
    AdminLogin()
