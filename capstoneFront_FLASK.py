from flask import Flask, render_template, url_for, request, redirect, jsonify
import json
import os
from DB_Tables import *
from ResProj_BackEnd import AdminLogin
from flask_socketio import SocketIO
import webbrowser

# Need these when using Flask-socketio
# pip install flask-cors
# pip install flask-socketio

# Change the file dir, used to work with the JSON files
os.chdir(os.path.dirname(os.path.realpath(__file__)))
    

# Create app and socket
# From what I understand, the CORS is there to check if it is a different IP
# If we run flask and the socket in local host, the socket is technically open on another IP
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins=['http://127.0.0.1:5000', 'http://localhost:5000'])
app.config["SECRET_KEY"] = "Its a secret?"

# By default, we go right to the capstoneFront
@app.route("/")
def myredirect():
    return redirect(url_for("capstoneFront"))

# route to capstoneFront is capstoneFront.html
@app.route("/capstoneFront")
def capstoneFront():
    return render_template("capstoneFront.html")

# Called to update the JSON files related to the tables
@app.route("/update_tables", methods=["POST"])
def update_tables():
    data = request.json
    print(data)
    json_data = json.dumps({"tables": data}, indent=2)

    with open("./static/data/table_orders.json", "w") as json_file:
        json_file.write(json_data)
    return jsonify({"message": "We did it "})

# Called to update the JSON files related to the menu_items
@app.route("/update_stock", methods=["POST"])
def update_stock():
    data = request.json
    print("id?", data)
    newStock = int(data['stock']) - 1
    MenuItemDAO = MenuItems_TableDAO("mysqlMenus")
    MenuItemDAO.update_item_stock_by_id(newStock, data['item_id'])
    MenuItemDAO.menuItems_to_json()
        
    
    return jsonify({"message": "We did it "})

# OLd not used anymore
# @app.route("/get_menus", methods=["GET"])
# def get_menus():

#     menu_DAO = Menu_TableDAO("mysqlMenus")
#     menu_ALL = menu_DAO.return_menus_json()
#     menu_DAO.close()
#     return menu_ALL

# Check if employee is clocked In or not
@app.route("/check_clock", methods=["POST"])
def check_clock():

    data = request.json

    emp_code = data["empCode"]

    print("Employee Code:", emp_code)

    employee_DAO = Employees_TableDAO("mysqlEmployees")
    employeeBy_PIN = employee_DAO.fetch_employee_by_pin(emp_code)
    employee_DAO.close()

    logEmpl = EmployeesShift_TableDAO("mysqlEmployees")
    recordOpen = logEmpl.fetch_record_by_EMPL_ID(employeeBy_PIN.employee_id)
    logEmpl.close()
    print(recordOpen)

    if recordOpen != None:
        return '1'
    elif recordOpen == None:
        return '0'
    else:
        print("NOT GOOD")



# Clock Employee In or Out
@app.route("/clock_Empl", methods=["POST"])
def clock_Empl():
    data = request.json

    emp_code = data["empCode"]
    timestamp = data["timestamp"]
    close_record = data["clockVal"]

    print(f"Clock: {close_record}")
    print(f"Employee Code: {emp_code}")
    print(f"Timestamp: {timestamp}")

    employee_DAO = Employees_TableDAO("mysqlEmployees")
    employeeBy_PIN = employee_DAO.fetch_employee_by_pin(emp_code)
    employee_DAO.close()

    

    logEmpl = EmployeesShift_TableDAO("mysqlEmployees")
    recordOpen = logEmpl.fetch_record_by_EMPL_ID(employeeBy_PIN.employee_id)

    if close_record == 0:
        logEmpl.employee_clockIN(timestamp, employeeBy_PIN.employee_id)
        logEmpl.close()

        return jsonify({"Contents": "0"})
    
    elif close_record == 1:
        logEmpl.employee_clockOUT(recordOpen.clock_record_id, timestamp)
        recordOpen = logEmpl.fetch_record_by_REC_ID(recordOpen.clock_record_id)
        logEmpl.close()

        return jsonify({"Contents": recordOpen.clock_total})
        
    else:
        return jsonify({"Contents": "-1"})

# This is the socket that is called from the back-end to notify Flask that the JSON files have changed
@app.route('/notify_update', methods=['POST'])
def notify_update():
    print("Received update notification")
    # Emit a WebSocket event to all connected clients
    socketio.emit('JSON_Update', {'message': 'Data has been updated'})
    return jsonify({'message': 'Notification received'}), 200


@app.route("/admin_BackEnd")
def admin_BackEnd():
    AdminLogin()
    return jsonify({"message": "We did it "})
    
if __name__ == "__main__":
    webbrowser.open('http://127.0.0.1:5000')
    socketio.run(app, debug=True) # Turn off debug to stop 2 tabs
