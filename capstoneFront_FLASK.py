from flask import Flask, render_template, url_for, request, redirect, jsonify
import json
import os
from DB_Tables import *

os.chdir(os.path.dirname(os.path.realpath(__file__)))

app = Flask(__name__)

app.config["SECRET_KEY"] = "Its a secret?"


@app.route("/")
def myredirect():
    return redirect(url_for("JCcapstoneFront"))


@app.route("/JCcapstoneFront")
def JCcapstoneFront():
    return render_template("JCcapstoneFront.html")


@app.route("/add_data", methods=["POST"])
def add_data():
    data = request.json
    print(data)
    json_data = json.dumps({"tables": data}, indent=2)

    with open("./static/data/table_orders.json", "w") as json_file:
        json_file.write(json_data)
    return jsonify({"message": "We did it "})


@app.route("/get_menus", methods=["GET"])
def get_menus():

    menu_DAO = Menu_TableDAO("mysqlMenus")
    menu_ALL = menu_DAO.return_menus_json()
    menu_DAO.close()
    return menu_ALL

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

    


if __name__ == "__main__":
    app.run(debug=True)
