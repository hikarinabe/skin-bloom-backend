import json
import random
from datetime import datetime
from zoneinfo import ZoneInfo

from firebase_admin import firestore
from firebase_functions import https_fn


class UserType:
    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.nick_name = ""
        self.sex = "回答なし"
        self.birthday = datetime(1900, 1, 1)
        

    def __str__(self):
        return f"first_name: {self.first_name}, last_name: {self.last_name}, data:{self.nick_name}, sex:{self.sex}, birthday:{self.birthday}"
    
    def set_first_name(self, request_item):
        if request_item != None:
            self.first_name = request_item
    
    def set_last_name(self, request_item):
        if request_item != None:
            self.last_name = request_item

    def set_nick_name(self, request_item):
        if request_item != None:
            self.nick_name = request_item

    def set_sex(self, request_item):
        if request_item != None:
            self.sex = request_item

    def set_birthday(self, request_item):
        if request_item != None:
            # datetime format: https://docs.python.org/ja/3/library/datetime.html#datetime.datetime.fromisoformat
            birthday =  datetime.fromisoformat(request_item)
            if type(birthday) == datetime:
                self.birthday =  birthday

_AUTO_ID_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
def generate_auto_ID() -> str:
    return "".join(random.choice(_AUTO_ID_CHARS) for _ in range(20))

def set_user_information(req: https_fn.Request) -> UserType:
    user = UserType()
    user.set_first_name(req.form.get('first_name'))
    user.set_last_name(req.form.get('last_name'))
    user.set_nick_name(req.form.get('nick_name'))
    user.set_sex(req.form.get('sex'))
    user.set_birthday(req.form.get('birthday'))
    return user

def timestamp_to_str(time_item) -> str:
    timestamp_str = datetime.fromtimestamp(time_item.timestamp(), ZoneInfo("Asia/Tokyo"))
    return timestamp_str.strftime('%Y-%m-%d-%H:%M:%S.%f')




""" 
    Called by main.py
"""
def get_user(req: https_fn.Request):
    user_id = req.args.to_dict().get('user_id')

    db = firestore.client()
    doc = db.collection(u'user').document(user_id).get()    
    if doc.exists == False:
        return https_fn.Response(status=404, response="user not found")
    
    user_dict = doc.to_dict()

    # json.dumpでエラーが出るので、timestampをstringに直す
    user_dict['birthday'] = timestamp_to_str(user_dict['birthday'])
    user_dict['create_time'] = timestamp_to_str(user_dict['create_time'])
    user_dict['update_time'] = timestamp_to_str(user_dict['update_time'])    

    return https_fn.Response(status=200, response=json.dumps(user_dict), content_type='application/json')

def create_user(req: https_fn.Request):
    db = firestore.client()
    user = set_user_information(req)
    user_id = generate_auto_ID()
    result = db.collection('user').document(user_id).set({
        'first_name': user.first_name, 
        'last_name': user.last_name,
        'nick_name': user.nick_name,
        'sex': user.sex, 
        'birthday': user.birthday,
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
    doc = db.collection(u'user').document(user_id).get()    
    if doc.exists == False:
        return https_fn.Response(status=404, response="user not found")

    # ユーザーの削除
    doc = db.collection(u'user').document(user_id).delete()
    return https_fn.Response(status=200, response="User deleted")
    
def update_user(req: https_fn.Request):
    user_id = req.args.to_dict().get('user_id')

    # ユーザーの存在確認
    db = firestore.client()
    doc_ref = db.collection(u'user').document(user_id)
    if doc_ref.get().exists == False:
        return https_fn.Response(status=404, response="user not found")
    
    # 情報を更新
    user = set_user_information(req)
    doc_ref.update({
        'first_name': user.first_name, 
        'last_name': user.last_name,
        'nick_name': user.nick_name,
        'sex': user.sex, 
        'birthday': user.birthday,
        'update_time': datetime.now()
    })
    
    return https_fn.Response(status=201, response="User updated")
