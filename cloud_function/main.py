from google.cloud import vision
import firebase_admin
from firebase_admin import firestore

def main(event, context):

    file_name= event["name"]
    bucket_name= event["bucket"]

    client = vision.ImageAnnotatorClient() 

    #URI of the image
    blob_uri = f"gs://{bucket_name}/{file_name}"
    #blob source
    image = vision.Image(source=vision.ImageSource(image_uri=blob_uri))
    response = client.face_detection(image=image)
    faceAnnotation = response.face_annotations
    print("Entro Aqui" + str(faceAnnotation))

    #Get the first face
    analist = faceAnnotation[0]

    if (analist.detection_confidence >= 3) and (analist.detection_confidence <= 5):
        answer = "confident"
    elif (analist.anger_likelihood >= 3) and (analist.anger_likelihood <= 5):
        answer = "angry"
    elif (analist.joy_likelihood >= 3) and (analist.joy_likelihood <= 5):
        answer = "happy"
    elif (analist.sorrow_likelihood >= 3) and (analist.sorrow_likelihood <= 5):
        answer = "sad"
    elif (analist.surprise_likelihood >= 3) and (analist.surprise_likelihood <= 5):
        answer = "surprised"

    employee = file_name.split(".")[0]
    print(employee + " is " + answer)

    app_options = {'projectId': 'proyectosoa-362116'}
    app = firebase_admin.initialize_app(options=app_options)
    db = firestore.client()
    doc = db.collection("employee").document(employee)

    doc.set({
        "name": employee,
        "emotion": answer
    })
    
    # Delete the default app 
    firebase_admin.delete_app(app)

