# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`
# The Cloud Functions for Firebase SDK to create Cloud Functions and set up triggers.
# The Firebase Admin SDK to access Cloud Firestore.
from firebase_admin import initialize_app
from firebase_functions import https_fn, options

initialize_app()
options.set_global_options(region=options.SupportedRegion.ASIA_NORTHEAST1)

@https_fn.on_request(
        cors=options.CorsOptions(cors_origins="*", cors_methods=["get"])
)
def on_request_example(req: https_fn.Request) -> https_fn.Response:
    return https_fn.Response("Hello world!")

@https_fn.on_request()
def addmessage(req: https_fn.Request) -> https_fn.Response:
    """Take the text parameter passed to this HTTP endpoint and insert it into
    a new document in the messages collection."""
    # Grab the text parameter.
    original = req.args.get("text")
    if original is None:
        return https_fn.Response("No text parameter provided", status=400)

    firestore_client: google.cloud.firestore.Client = firestore.client()

    # Push the new message into Cloud Firestore using the Firebase Admin SDK.
    _, doc_ref = firestore_client.collection("messages").add(
        {"original": original}
    )

    # Send back a message that we've successfully written the message
    return https_fn.Response(f"Message with ID {doc_ref.id} added.")
