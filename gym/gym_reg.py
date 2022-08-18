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
        if data_dict['user']== request.headers['x-api-key']:
            return func(*args,  **kwargs)
        print("End")
    return wrapper_function
        



@app.route('/',methods=['Get'])
@check_valid_user
def view():
    x=open('gym_data.json','r')
    data_obj=json.load(x)
    data_list=data_obj['gym_registry']
    return {"result": data_list}
    # return Response(json.dumps(data_list),  mimetype='application/json')


@app.route('/add',methods=['POST'])
def add():
    val = get_value(request)
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
            with open('gym_data_archive.json','w') as y:
                json.dump(old_data_obj,y)
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
    data_list = data_obj['gym_registry']
    val = get_value(request)
    for i in data_list:
        if i['user']==val['data']['profile_info']['profile_Master']['primary_key']['user']:
            index_i=data_list.index(i)
            del data_list[index_i]
    
    with open('gym_data.json','w') as y:
        json.dump(data_obj,y)
    return "deleted Success"

def get_value(request):
    return request.get_json()


def tesst1():
    return "deleted Success"

def test2():
    resp = tesst1()
    return resp



if __name__ == ('__main__'):
    app.run(debug=True)