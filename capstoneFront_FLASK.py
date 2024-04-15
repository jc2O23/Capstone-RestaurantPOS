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


@app.route('/JCcapstoneFront')
def JCcapstoneFront():
    return render_template('JCcapstoneFront.html')


@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.json
    print(data)
    json_data = json.dumps({'tables': data}, indent=2)

    with open('./static/data/table_orders.json', 'w') as json_file:
        json_file.write(json_data)
    return jsonify({'message': "We did it "})


@app.route('/get_menus', methods=['GET'])
def get_menus():

    menu_DAO = Menu_TableDAO('mysqlMenus')
    menu_ALL = menu_DAO.return_menus_json()
    return jsonify(menu_ALL)




if __name__ == "__main__":
    app.run(debug=True)
