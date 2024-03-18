import json
from datetime import datetime

from firebase_admin import firestore
from firebase_functions import https_fn

DEFAULT_BIRTHDAY = datetime(1900, 1, 1, 0, 0, 0)
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

def add_cosmetic_log(req: https_fn.Request):
    data = json.loads(req.data.decode("utf-8"))
    user_id = data['user_id']
    cosmetic_id = data['cosmetic_id']

    db = firestore.client()
    result = db.collection(u'user').document(user_id).collection(u'cosmetic_logs').document(cosmetic_id).set({
        'rate': float(data['rate']) if 'comment' in data else -1,
        'category': int(data['category']) if 'comment' in data else 0,
        'good_tag': data['good_tag'] if 'good_tag' in data else [], 
        'bad_tag': data['bad_tag'] if 'bad_tag' in data else [], 
        'comment': data['comment']  if 'comment' in data else '',
        'create_time': datetime.now(),
        'update_time': datetime.now()
    })
    if result:
        return format_response(status=201, response='Success to create log')
    
    return format_response(status=500, response="Failed to create log")


def get_cosmetic_log(req: https_fn.Request):
    user_id = req.args.to_dict().get('user_id')
    cosmetic_id = req.args.to_dict().get('cosmetic_id')

    db = firestore.client()
    doc = db.collection(u'user').document(user_id).collection(u'cosmetic_logs').document(cosmetic_id).get()    
    if doc.exists == False:
        return format_response(status=404, response="user not found")
    
    # TODO: cosmetic_dataから商品名も持ってくる
    
    log_dict = doc.to_dict()
    resp = {
        'rate': log_dict['rate'],
        'category': log_dict['category'],
        'good_tag': log_dict['good_tag'], 
        'bad_tag': log_dict['bad_tag'],
        'comment': log_dict['comment'],
    } 
    
    return https_fn.Response(status=200, response=json.dumps(resp), content_type='application/json')

def list_cosmetic_log(req: https_fn.Request):
    user_id = req.args.to_dict().get('user_id')

    db = firestore.client()
    log_docs = db.collection(u'user').document(user_id).collection(u'cosmetic_logs').get()

    logs = []
    
    # TODO: cosmetic_dataから商品名も持ってくる    
    for d in log_docs:
        log_dict = d.to_dict()
        one_log = {
            'rate': log_dict['rate'],
            'category': log_dict['category'],
            'good_tag': log_dict['good_tag'], 
            'bad_tag': log_dict['bad_tag'],
            'comment': log_dict['comment'],
        } 
        logs.append(one_log)
    
    return https_fn.Response(status=200, response=json.dumps({"list_cosmetics": logs}), content_type='application/json')

def validate_item(item, data, db_info):
    if (item in data) == False:
        return db_info.to_dict()[item]
    return data[item]

def update_cosmetic_log(req: https_fn.Request):
    data = json.loads(req.data.decode("utf-8"))
    user_id = data['user_id']
    cosmetic_id = data['cosmetic_id']

    db = firestore.client()
    cosmetic_ref = db.collection(u'user').document(user_id).collection(u'cosmetic_logs').document(cosmetic_id)
    cosmetic_info = cosmetic_ref.get()
    if cosmetic_info.exists == False:
        return format_response(status=404, response="log not found")

    cosmetic_ref.update({
        'rate': validate_item('rate', data, cosmetic_info),
        'category': validate_item('category', data, cosmetic_info),
        'good_tag': validate_item('good_tag', data, cosmetic_info), 
        'bad_tag': validate_item('bad_tag', data, cosmetic_info), 
        'comment': validate_item('comment', data, cosmetic_info),
        'update_time': datetime.now()
    })

    return format_response(status=201, response='Success to update log')
    

def delete_cosmetic_log(req: https_fn.Request):
    user_id = req.args.to_dict().get('user_id')
    cosmetic_log_id = req.args.to_dict().get('cosmetic_log_id')

    # ユーザーが存在するか確認
    db = firestore.client()
    user_ref = db.collection(u'user').document(user_id)
    if user_ref.get().exists == False:
        return format_response(status=404, response="user not found")
    
    # ログの削除
    user_ref.collection(u'cosmetic_logs').document(cosmetic_log_id).delete()

    return format_response(status=200, response="CosmeticLog is deleted")