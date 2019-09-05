from flask import Flask
from flask import Response
from flask import jsonify
from flask import g
from flask import request
from flask import make_response
import json
import sqlite3
import os

DATABASE = 'database/chinook.db'

app = Flask(__name__, static_folder="json")

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/employees',methods=["GET"])
def employees_list():
    db = get_db()
    data = db.execute('SELECT * FROM employees').fetchall()
    res = []
    for employee in data:
        item = {
            'EmployeeID':employee[0],
            'Firstname':employee[2],
            'Lastname':employee[1],
            'Address':employee[7]
        }
        res.append(item)
    return jsonify({
        'employees': res
    })

@app.route('/employees/<int:id>',methods=["GET"])
def employees_id(id):
    db = get_db()
    data = db.execute('SELECT * FROM EMPLOYEES WHERE EmployeeId='+ str(id)).fetchone()
    
    if not data:
        return jsonify({
            'employee': 'error'
        })
    else:
        employee = {
            'FirstName':data[1],
            'LastName':data[2]
           
        }
        return jsonify({
            'employee': employee
        })

@app.route('/employees',methods=["POST"])
def employees_insert():
    db = get_db()
    
    if request.is_json:
        req = request.get_json()
        fname = req.get('Firstname')
        lname = req.get('Lastname')
        data= db.execute("INSERT INTO EMPLOYEES (FirstName,LastName) VALUES('" + fname+ "','"+lname+"')")
        db.commit()
        if not data:
            return jsonify({'message':'error'})    
        else:        
            return jsonify({'message':'OK'})    

@app.route('/employees/<int:id>',methods=["PUT"])
def employees_update(id):
    db = get_db()
    
    if request.is_json:
        req = request.get_json()
        address = req.get('Address')
        data= db.execute("UPDATE EMPLOYEES set Address = '"+ address +"' where EmployeeId = " + str(id))
        db.commit()
        if not data:
            return jsonify({'message':'error'})    
        else:        
            return jsonify({'message':'OK'})

@app.route('/employees/<int:id>',methods=["DELETE"])
def employees_delete(id):
    db = get_db()   
    data= db.execute("DELETE FROM EMPLOYEES where EmployeeId = " + str(id))
    db.commit()
    if not data:
        return jsonify({'message':'error'})    
    else:        
        return jsonify({'message':'OK'})

@app.route('/', methods=["GET"])
def hello():
    return "Hello World!"

if (__name__ == "__main__"):
	app.run(host='0.0.0.0',port=5000)

