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
    password = hashlib.sha256(req.form.get('password').encode()).hexdigest()

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

def update_user(req: https_fn.Request):
    # get user id
    user_id = req.args.to_dict().get('user_id')

    db = firestore.client()
    doc_ref = db.collection(u'auth').document(user_id)
    user_info = doc_ref.get()
    if user_info.exists == False:
        return https_fn.Response(status=404, response="user not found")
    
    # email
    email = req.form.get('email')
    if email == None:
        email = user_info.to_dict()['email']

    # hash password
    if req.form.get('password') != None:
        password = hashlib.sha256(req.form.get('password').encode()).hexdigest()
    else:
        password = user_info.to_dict()['password']

    doc_ref.update({
        'email': email, 
        'password': password,
        'update_time': datetime.now()
    })
    
    return https_fn.Response(status=200, response="User updated")

def check(req: https_fn.Request):
    # get user id
    user_id = req.args.to_dict().get('user_id')

    # get auth information
    db = firestore.client()
    auth_doc = db.collection('auth').document(user_id).get()
    if auth_doc.exists == False:
        return https_fn.Response(status=404, response="user not found")
    auth_dict = auth_doc.to_dict()

    login_response = LoginResponse()

    # email
    if req.form.get('email') != auth_dict['email']:
        return https_fn.Response(status=200, response=json.dumps(login_response.__dict__), content_type='application/json')
    
    # hash password    
    password = hashlib.sha256(req.form.get('password').encode()).hexdigest()
    if password != auth_dict['password']:
        return https_fn.Response(status=200, response=json.dumps(login_response.__dict__), content_type='application/json')

    login_response.set_success()
    return https_fn.Response(status=200, response=json.dumps(login_response.__dict__), content_type='application/json')
