import json
from datetime import datetime
from zoneinfo import ZoneInfo

from firebase_admin import firestore
from firebase_functions import https_fn
from google.api_core.datetime_helpers import DatetimeWithNanoseconds

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
    format_response(200, "unimplemented")

def get_cosmetic_log(req: https_fn.Request):
    format_response(200, "unimplemented")

def list_cosmetic_log(req: https_fn.Request):
    format_response(200, "unimplemented")

def update_cosmetic_log(req: https_fn.Request):
    format_response(200, "unimplemented")

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