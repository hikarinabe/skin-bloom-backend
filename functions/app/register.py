import hashlib
import json
import random
from datetime import datetime

from firebase_admin import firestore
from firebase_functions import https_fn


class LoginResponse:
    def __init__(self):
        self.result = False

    def set_success(self):
        self.result = True


_AUTO_ID_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
def generate_auto_ID() -> str:
    return "".join(random.choice(_AUTO_ID_CHARS) for _ in range(20))


def register_user(req: https_fn.Request):
    user_id = generate_auto_ID()

    # email
    email = req.form.get('email')

    # hash password    
    password = hashlib.sha256(req.form.get('password')).hexdigest()

    db = firestore.client()
    result = db.collection('auth').document(user_id).set({
        'email': email, 
        'password': password,
        'create_time': datetime.now(),
        'update_time': datetime.now()
    })
    if result:
        return https_fn.Response(status=201, response=user_id)

    return https_fn.Response(status=500, response="Failed to register user")


def check(req: https_fn.Request):
    # get user id
    user_id = req.form.get('user_id')

    # get auth information
    db = firestore.client()
    auth_dict = db.collection('auth').document(user_id).get().to_dict()

    login_response = LoginResponse()

    # email
    if req.form.get('email') != auth_dict['email']:
        return https_fn.Response(status=200, response=json.dumps(login_response))
    
    # hash password    
    password = hashlib.sha256(req.form.get('password')).hexdigest()
    if password != auth_dict['password']:
        return https_fn.Response(status=200, response=json.dumps(login_response))

    return https_fn.Response(status=200, response=json.dumps(login_response.set_success()))

def update_user(req: https_fn.Request):
    # get user id
    user_id = req.form.get('user_id')

    db = firestore.client()
    doc_ref = db.collection(u'auth').document(user_id)
    if doc_ref.get().exists == False:
        return https_fn.Response(status=404, response="user not found")
    
    # email
    email = req.form.get('email')

    # hash password    
    password = hashlib.sha256(req.form.get('password')).hexdigest()

    doc_ref.update({
        'email': email, 
        'password': password,
        'update_time': datetime.now()
    })
    
    return https_fn.Response(status=201, response="User updated")
