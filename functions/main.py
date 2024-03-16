""" This is main program
    Deploy with `firebase deploy """
import app.register
import app.user
from firebase_admin import credentials, initialize_app
from firebase_functions import https_fn, options

options.set_global_options(region=options.SupportedRegion.ASIA_NORTHEAST1)
cred = credentials.Certificate('./key.json')
initialize_app(cred)

@https_fn.on_request(
    cors=options.CorsOptions(cors_origins='*', cors_methods=['get'])
)
def hello(_: https_fn.Request) -> https_fn.Response:
    """ hello returns hello_world_from_cloud_function regardless of input """
    return https_fn.Response('hello_world_from_cloud_function')

@https_fn.on_request(
    cors=options.CorsOptions(cors_origins='*', cors_methods=['get', 'post', 'put', 'delete'])
)
def user(req: https_fn.Request) -> https_fn.Response:
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
    cors=options.CorsOptions(cors_origins='*', cors_methods=['post', 'put'])
)
def auth(req: https_fn.Request) -> https_fn.Response:
    if req.method == 'POST':
        return app.register.register_user(req)
    if req.method == 'PUT':
        return app.register.update_user(req)
    return https_fn.Response(status=405, response="Not support the request method")

@https_fn.on_request(
    cors=options.CorsOptions(cors_origins='*', cors_methods=['post', 'put'])
)
def login(req: https_fn.Request) -> https_fn.Response:
    return app.register.check(req)
