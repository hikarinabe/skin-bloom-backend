import json
from datetime import datetime
from zoneinfo import ZoneInfo

from firebase_admin import firestore
from firebase_functions import https_fn


class UserType:
    def __init__(self):
        self.account_name = ""
        self.sex = "回答なし"
        self.birthday = datetime(1900, 1, 1)
        
    def __str__(self):
        return f"account_name:{self.account_name}, sex:{self.sex}, birthday:{self.birthday}"

    def set_account_name(self, request_item):
        if request_item != None:
            self.account_name = request_item

    def set_sex(self, request_item):
        if request_item != None:
            self.sex = request_item

    def set_birthday(self, request_item):
        if request_item != None:
            # datetime format: https://docs.python.org/ja/3/library/datetime.html#datetime.datetime.fromisoformat
            birthday =  datetime.fromisoformat(request_item)
            if type(birthday) == datetime:
                self.birthday =  birthday
    
    def set_str_birthday(self, time_item):
        if type(time_item) == datetime:
            timestamp_str = datetime.fromtimestamp(time_item.timestamp(), ZoneInfo("Asia/Tokyo"))
            self.birthday = timestamp_str.strftime('%Y-%m-%d-%H:%M:%S.%f')
        else:
            self.birthday = time_item

    def convert_response_to_user_type(user_dict):
        user = UserType()
        user.set_account_name(user_dict['account_name'])
        user.set_sex(user_dict['sex'])
        user.set_str_birthday(user_dict['birthday'])
        return user




""" 
    Called by main.py
"""
def get_user(req: https_fn.Request):
    user_id = req.args.to_dict().get('user_id')

    db = firestore.client()
    doc = db.collection(u'user').document(user_id).get()    
    if doc.exists == False:
        return https_fn.Response(status=404, response="user not found")
    
    user = UserType.convert_response_to_user_type(doc.to_dict())  
    
    return https_fn.Response(status=200, response=json.dumps(user.__dict__), content_type='application/json')

def create_user(req: https_fn.Request):
    db = firestore.client()
    user_id = req.args.to_dict().get('user_id')
    # ユーザーが存在するか確認
    db = firestore.client()
    doc = db.collection(u'auth').document(user_id).get()    
    if doc.exists == False:
        return https_fn.Response(status=404, response="user not found")

    result = db.collection('user').document(user_id).set({
        'account_name': req.form.get('account_name'),
        'sex': req.form.get('sex'), 
        'birthday': req.form.get('birthday'),
        'create_time': datetime.now(),
        'update_time': datetime.now()
    })
    if result:
        return https_fn.Response(status=201, response=user_id)
    
    return https_fn.Response(status=500, response="Failed to create user")

def delete_user(req: https_fn.Request):
    user_id = req.args.to_dict().get('user_id')

    # ユーザーが存在するか確認
    db = firestore.client()
    doc = db.collection(u'auth').document(user_id).get()    
    if doc.exists == False:
        return https_fn.Response(status=404, response="user not found")

    # ユーザーの削除
    db.collection(u'auth').document(user_id).delete()
    db.collection(u'user').document(user_id).delete()
    return https_fn.Response(status=200, response="User deleted")
    
def validate_item(item, req, db_info):
    req_item = req.form.get(item)
    if req_item == None:
        return db_info.to_dict()[item]
    return req_item
    
def update_user(req: https_fn.Request):
    user_id = req.args.to_dict().get('user_id')

    # ユーザーの存在確認
    db = firestore.client()
    user_ref = db.collection(u'user').document(user_id)
    user_info = user_ref.get()
    if user_info.exists == False:
        return https_fn.Response(status=404, response="user not found")
    
    # 情報を更新
    account_name = validate_item('account_name', req, user_info)
    sex = validate_item('sex', req, user_info)
    birthday = validate_item('birthday', req, user_info)

    user_ref.update({
        'account_name': account_name,
        'sex': sex, 
        'birthday': birthday,
        'update_time': datetime.now()
    })
    
    return https_fn.Response(status=200, response="User updated")
