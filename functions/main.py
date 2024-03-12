""" This is main program
    Deploy with `firebase deploy """
from firebase_admin import initialize_app
from firebase_functions import https_fn, options

initialize_app()
options.set_global_options(region=options.SupportedRegion.ASIA_NORTHEAST1)

@https_fn.on_request(
    cors=options.CorsOptions(cors_origins="*", cors_methods=["get"])
)
def hello(_: https_fn.Request) -> https_fn.Response:
    """ hello returns hello_world_from_cloud_function regardless of input """
    return https_fn.Response("hello_world_from_cloud_function")
