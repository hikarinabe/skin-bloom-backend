import json

from firebase_admin import firestore
from firebase_functions import https_fn


def get_user(req: https_fn.Request):
    user_id = req.args.to_dict().get('user_id')

    db = firestore.client()
    doc = db.collection(u'user').document(user_id).get()
    if doc.exists == False:
        return https_fn.Response(status=404, response="user not found")
    resp = doc.to_dict()

    return https_fn.Response(status=200, response=json.dumps(resp), content_type='application/json')

def create_user(req: https_fn.Request):
    print("create_user")

def delete_user(req: https_fn.Request):
    print("GEdelete_userT")

def update_user(req: https_fn.Request):
    return https_fn.Response(status=201, response="User updated")
