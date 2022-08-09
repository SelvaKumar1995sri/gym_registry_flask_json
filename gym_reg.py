from flask import Flask,request,Response
import json
import copy

app = Flask(__name__)

def check_valid_user(func):
    def wrapper_function(*args, **kwargs):
        print("Start")
        x=open('gym_data.json','r')
        data_obj=json.load(x)
        data_dict = data_obj['gym_registry'][0]['data']['profile_info']['profile_Master']['primary_key']
        if data_dict['user']== request.headers('x-api-key'):
            func(*args,  **kwargs)
        print("End")
    return wrapper_function
        


@check_valid_user
@app.route('/',methods=['Get'])
def view():
    x=open('gym_data.json','r')
    data_obj=json.load(x)
    data_list=data_obj['gym_registry']
    
    return Response(json.dumps(data_list),  mimetype='application/json')


@check_valid_user
@app.route('/add',methods=['POST'])
def add():
    val = request.get_json()   
    x=open("gym_data.json",'r')
    data_obj = json.load(x) 
    data_list = data_obj['gym_registry']
    data_list.append(val)
    with open('gym_data.json','w') as y:
        json.dump(data_obj,y)
    return "Success"

@check_valid_user
@app.route('/update',methods=['put'])
def update():
    val = request.get_json() 
    x=open("gym_data.json",'r')
    data_obj = json.load(x)
    data_list = data_obj['gym_registry']
    val_user = val['data']['profile_info']['profile_Master']['primary_key']['user']
    for i in data_list:
        res=i['data']['profile_info']['profile_Master']['primary_key']['user']
        
        if res == val_user:
            old_coverage=copy.deepcopy(i)
            x=open("gym_data_archive.json",'r')
            old_data_obj = json.load(x)
            old_data_list = old_data_obj['old_gym_registry']
            old_data_list.append(old_coverage)
            index_i=data_list.index(i)
            data_list[index_i]=val
    
    with open('gym_data.json','w') as y:
        json.dump(data_obj,y)
    return "updated Success"

@check_valid_user
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