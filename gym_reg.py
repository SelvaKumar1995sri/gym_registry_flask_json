from shutil import ExecError
from flask import Flask,request
import json


app = Flask(__name__)

def my_decorator(func):
    def wrapper_function(*args, **kwargs):
        try:
            print("*"*10)
            x=open('gym_data.json','r')
            data_obj=json.load(x)
            data_list = data_obj['data']['profile_info']['profile_Master']['primary_key']
            if data_list['user']== request.headers('x-api-key'):
                func(*args,  **kwargs)
            print("*"*10)
            return wrapper_function
        except Exception as e:
            print("authontication failed:" +str(e))


@my_decorator
@app.route('/',methods=['Get'])
def view():
    x=open('gym_data.json','r')
    data_obj=json.load(x)
    return data_obj


@my_decorator
@app.route('/add',methods=['POST'])
def add():
    x=open("gym_data.json",'r')
    data_obj = json.load(x) 
    data_list = data_obj['data']["coverage"]
    val = request.get_json() 
    print(val)   
    data_list.append(val)
    with open('gym_data.json','w') as y:
        json.dump(data_obj,y)
    return "Success"

@my_decorator
@app.route('/update',methods=['put'])
def update():
    x=open("gym_data.json",'r')
    data_obj = json.load(x) 
    data_list = data_obj['data']["coverage"]
    val = request.get_json() 
    print(val['no'])
    for i in data_list:
        if i['no'] == val['no'] :
            index_i=data_list.index(i)
            data_list[index_i]=val
    with open('gym_data.json','w') as y:
        json.dump(data_obj,y)
    return "updated Success"

@my_decorator
@app.route('/delete',methods=['put'])
def delete():
    x=open("gym_data.json",'r')
    data_obj = json.load(x) 
    data_list = data_obj['data']["coverage"]
    val = request.get_json()
    for i in data_list:
        if i['id']==val['id']:
            index_i=data_list.index(i)
            del data_list[index_i]
    
    with open('gym_data.json','w') as y:
        json.dump(data_obj,y)
    return "deleted Success"

if __name__ == ('__main__'):
    app.run(debug=True)