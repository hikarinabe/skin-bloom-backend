""" This is main program
    Deploy with `firebase deploy """
import app.user
from firebase_admin import initialize_app
from firebase_functions import https_fn, options

initialize_app()
options.set_global_options(region=options.SupportedRegion.ASIA_NORTHEAST1)

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
        user_resp = app.user.get_user(req)
        return https_fn.Response(status=200, response=user_resp)
    if req.method == 'POST':
        app.user.create_user(req)
        return https_fn.Response(status=201, response="User created")
    if req.method == 'PUT':
        app.user.update_user(req)
        return https_fn.Response(status=201, response="User updated")
    if req.method == 'DELETE':
        app.user.delete_user(req)
        return https_fn.Response(status=200, response="User deleted")
    return https_fn.Response(status=405, response="Not support the request method")
