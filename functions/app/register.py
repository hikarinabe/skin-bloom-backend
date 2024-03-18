import hashlib
import json
import random
from datetime import datetime

from firebase_admin import firestore
from firebase_functions import https_fn


class LoginResponse:
    def __init__(self, user_id):
        self.user_id = user_id

def format_response(status, response: str):
    return https_fn.Response(status=status, response=json.dumps({'message': response}), content_type='application/json')

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
        return https_fn.Response(status=200, response=json.dumps(LoginResponse(user_id).__dict__), content_type='application/json')

    return format_response(status=500, response="Failed to register user")

# NOTE: password check is done by client side
def update_password(req: https_fn.Request):
    # get user id
    data = json.loads(req.data.decode("utf-8"))
    user_id = data['user_id']

    db = firestore.client()
    doc_ref = db.collection(u'auth').document(user_id)
    user_info = doc_ref.get()
    if user_info.exists == False:
        return format_response(status=404, response="user not found")
    current_password = hashlib.sha256(data['current_password'].encode()).hexdigest()
    if current_password != user_info.to_dict()['password']:
        return format_response(status=400, response="current password is wrong")

    if data['new_password'] != None:
        password = hashlib.sha256(data['new_password'].encode()).hexdigest()
    else:
        return format_response(status=400, response="please specify new password")

    doc_ref.update({
        'email': user_info.to_dict()['email'], 
        'password': password,
        'update_time': datetime.now()
    })
    
    return format_response(status=200, response="password updated")

def check(req: https_fn.Request):
    data = json.loads(req.data.decode("utf-8"))
    email = data['email']

    # get auth information
    db = firestore.client()
    auth_doc = db.collection('auth').where("email", "==", email).get()
    
    for d in auth_doc:
        auth_dict = d.to_dict()
        password = hashlib.sha256(data['password'].encode()).hexdigest()
        if email == auth_dict['email'] and password == auth_dict['password']:
            return https_fn.Response(status=200, response=json.dumps(LoginResponse(d.id).__dict__), content_type='application/json')
            
    return format_response(status=403, response='Fail to login')

