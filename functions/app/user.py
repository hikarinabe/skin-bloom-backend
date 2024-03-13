from firebase_functions import https_fn


def get_user(req: https_fn.Request):
    print("get_user")
    return {"user_response": ""}

def create_user(req: https_fn.Request):
    print("create_user")

def delete_user(req: https_fn.Request):
    print("GEdelete_userT")

def update_user(req: https_fn.Request):
    print("update_user")
