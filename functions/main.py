""" This is main program
    Deploy with `firebase deploy """
import os

import app.register
import app.user
from firebase_admin import credentials, initialize_app
from firebase_functions import https_fn, options

options.set_global_options(region=options.SupportedRegion.ASIA_NORTHEAST1)
cred = credentials.Certificate('./key.json')
initialize_app(cred)

def check_api_key(req: https_fn.Request):
    if os.environ.get('SECRET_NAME') !=  req.headers.get("Authorization"):
        return False
    return True

@https_fn.on_request(
    cors=options.CorsOptions(cors_origins='*', cors_methods=['get']), secrets=["SECRET_NAME"]
)
def hello(_: https_fn.Request) -> https_fn.Response:
    """ hello returns hello_world_from_cloud_function regardless of input """
    return https_fn.Response(f'hello_world_from_cloud_function: {os.environ.get("SECRET_NAME")}')

@https_fn.on_request(
    cors=options.CorsOptions(cors_origins='*', cors_methods=['get', 'post', 'put', 'delete']), secrets=["SECRET_NAME"]
)
def user(req: https_fn.Request) -> https_fn.Response:
    if check_api_key(req) == False:
        return https_fn.Response(status=401, response="Invalid API key")
    if req.method == 'GET':
        return app.user.get_user(req)
    if req.method == 'POST':
        return app.user.create_user(req)
    if req.method == 'PUT':
        return app.user.update_user(req)
    if req.method == 'DELETE':
        return app.user.delete_user(req)
    return https_fn.Response(status=405, response="Not support the request method")

@https_fn.on_request(
    cors=options.CorsOptions(cors_origins='*', cors_methods=['post', 'put']), secrets=["SECRET_NAME"]
)
def auth(req: https_fn.Request) -> https_fn.Response:
    if check_api_key(req) == False:
        return https_fn.Response(status=401, response="Invalid API key")
    if req.method == 'POST':
        return app.register.register_user(req)
    if req.method == 'PUT':
        return app.register.update_user(req)
    return https_fn.Response(status=405, response="Not support the request method")

@https_fn.on_request(
    cors=options.CorsOptions(cors_origins='*', cors_methods=['post']), secrets=["SECRET_NAME"]
)
def login(req: https_fn.Request) -> https_fn.Response:
    if check_api_key(req) == False:
        return https_fn.Response(status=401, response="Invalid API key")
    if req.method == 'POST':
       return app.register.check(req)
    return https_fn.Response(status=405, response="Not support the request method")
