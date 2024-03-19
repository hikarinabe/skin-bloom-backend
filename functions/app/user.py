import json
from datetime import datetime
from zoneinfo import ZoneInfo

from firebase_admin import firestore
from firebase_functions import https_fn
from google.api_core.datetime_helpers import DatetimeWithNanoseconds

DEFAULT_BIRTHDAY = datetime(1900, 1, 1, 0, 0, 0)

def set_str_birthday(time_item: DatetimeWithNanoseconds):
        date_time = datetime(time_item.year, time_item.month, time_item.day,
              time_item.hour, time_item.minute, time_item.second,
              time_item.nanosecond // 1000)
        if type(date_time) == datetime:
            timestamp_str = datetime.fromtimestamp(time_item.timestamp(), ZoneInfo("Asia/Tokyo"))
            return timestamp_str.strftime('%Y-%m-%dT%H:%M:%S')
        return time_item

def set_timestamp_birthday(str_time):
    birthday = DEFAULT_BIRTHDAY
    if str_time != None:
        try:
            # 1900-1-1 0:0:0
            birthday = datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
        except:
            birthday = DEFAULT_BIRTHDAY
    return birthday

def format_response(status, response: str):
    return https_fn.Response(status=status, response=json.dumps({'message': response}), content_type='application/json')


""" 
    Called by main.py
"""
def get_user(req: https_fn.Request):
    user_id = req.args.to_dict().get('user_id')

    db = firestore.client()
    doc = db.collection(u'user').document(user_id).get()    
    if doc.exists == False:
        return format_response(status=404, response="user not found")
    
    auth_doc = db.collection(u'auth').document(user_id).get()    
    if doc.exists == False:
        return format_response(status=404, response="user not found")
    
    user_dict = doc.to_dict()
    resp = {
        "account_name": user_dict['account_name'],
        "sex": user_dict['sex'],
        "birthday": set_str_birthday(user_dict['birthday']),
        "email": auth_doc.to_dict()["email"]
    } 
    
    return https_fn.Response(status=200, response=json.dumps(resp), content_type='application/json')

def create_user(req: https_fn.Request):
    data = json.loads(req.data.decode("utf-8"))
    user_id = data['user_id']
    # ユーザーが存在するか確認
    db = firestore.client()
    doc = db.collection(u'auth').document(user_id).get()    
    if doc.exists == False:
        return format_response(status=404, response="user not found")
    
    # account name の validation
    if ('account_name' in data) == False:
        return format_response(status=400, response="please specify account_name")

    result = db.collection('user').document(user_id).set({
        'account_name': data['account_name'],
        'sex': data['sex']  if 'sex' in data else 'N/A', 
        'birthday': set_timestamp_birthday(data['birthday']), 
        'nayami': data['nayami'] if 'nayami' in data else [], 
        'create_time': datetime.now(),
        'update_time': datetime.now()
    })
    if result:
        return format_response(status=201, response='Success to create user')
    
    return format_response(status=500, response="Failed to create user")

def delete_user(req: https_fn.Request):
    user_id = req.args.to_dict().get('user_id')

    # ユーザーが存在するか確認
    db = firestore.client()
    doc = db.collection(u'auth').document(user_id).get()    
    if doc.exists == False:
        return format_response(status=404, response="user not found")

    # ユーザーの削除
    db.collection(u'auth').document(user_id).delete()
    db.collection(u'user').document(user_id).delete()
    return format_response(status=200, response="User deleted")
    
def validate_item(item, data, db_info):
    if (item in data) == False:
        return db_info.to_dict()[item]
    return data[item]
    
def update_user(req: https_fn.Request):
    data = json.loads(req.data.decode("utf-8"))
    user_id = data['user_id']

    # ユーザーの存在確認
    db = firestore.client()
    user_ref = db.collection(u'user').document(user_id)
    user_info = user_ref.get()
    if user_info.exists == False:
        return format_response(status=404, response="user not found")
    
    # email用
    auth_ref = db.collection(u'auth').document(user_id)
    auth_info = auth_ref.get()
    if auth_info.exists == False:
        return format_response(status=404, response="user not found")
    
    # 情報を更新
    account_name = validate_item('account_name', data, user_info)
    sex = validate_item('sex', data, user_info)
    birthday = set_timestamp_birthday('birthday', data, user_info)
    user_ref.update({
        'account_name': account_name,
        'sex': sex, 
        'birthday': birthday,
        'update_time': datetime.now()
    })

    email = validate_item('email', data, auth_info)
    auth_ref.update({
        "email": email
    })
    
    return format_response(status=200, response="User updated")
