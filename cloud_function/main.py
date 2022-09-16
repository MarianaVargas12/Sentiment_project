from google.cloud import vision
import firebase_admin
from firebase_admin import firestore


def main(event, context):
    file_name = event["name"]
    bucket_name = event["bucket"]

    client = vision.ImageAnnotatorClient()

    # URI of the image
    blob_uri = f"gs://{bucket_name}/{file_name}"
    # blob source
    image = vision.Image(source=vision.ImageSource(image_uri=blob_uri))
    response = client.face_detection(image=image)
    faceAnnotation = response.face_annotations
    print("Entro Aqui" + str(faceAnnotation))

    # Get the first face
    analist = faceAnnotation[0]
    answer = ["no se sabe"]

    if (analist.detection_confidence >= 4) and (analist.detection_confidence <= 5):
        answer += ["confiado"]
    if (analist.anger_likelihood >= 4) and (analist.anger_likelihood <= 5):
        answer += ["enojado"]
    if (analist.joy_likelihood >= 4) and (analist.joy_likelihood <= 5):
        answer += ["feliz"]
    if (analist.sorrow_likelihood >= 4) and (analist.sorrow_likelihood <= 5):
        answer += ["triste"]
    if (analist.surprise_likelihood >= 4) and (analist.surprise_likelihood <= 5):
        answer += ["sorprendido"]

    employee = file_name.split(".")[0]
    resp = ''
    if (len(answer) == 1):
        resp = answer[0]
    else:
        for a in answer:
            if a == "no se sabe":
                a
            else:
                resp += a + ", "

    employee = file_name.split(".")[0]
    print(employee + " esta " + str(resp))

    app_options = {"projectId": "sentimentproject-362601"}
    app = firebase_admin.initialize_app(options=app_options)
    db = firestore.client()
    doc = db.collection("employee").document(employee)

    doc.set({
        "name": employee,
        "emotions": resp
    })

    # Delete the default app
    firebase_admin.delete_app(app)
    return employee + " esta " + str(resp)

