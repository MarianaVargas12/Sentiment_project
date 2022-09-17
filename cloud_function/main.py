#Importaciones necesarias
from google.cloud import vision
import firebase_admin
from firebase_admin import firestore
#Inicio de funcion
def main(event, context):
    #variables de nombre de la persona y bucket donde se almacena la imagen
    file_name = event["name"]
    bucket_name = event["bucket"]
    #API del IA
    client = vision.ImageAnnotatorClient()
    # URI de la imagen
    blob_uri = f"gs://{bucket_name}/{file_name}"
    # blob source, como un objeto
    image = vision.Image(source=vision.ImageSource(image_uri=blob_uri))
    response = client.face_detection(image=image)
    #respuesta del sentimiento
    face_annotation = response.face_annotations
    # Toma solo la primera cara
    analist = face_annotation[0]
    #Compara el resultado para cada sentimiento
    #El estado varia de 0 a 5
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
    #Separa todos los estados de la personas
    resp = ''
    if len(answer) == 1:
        resp = answer[0]
    else:
        for person in answer:
            if person != "no se sabe":
                resp += person + ", "
    employee = file_name.split(".")[0]
    print(employee + " esta " + str(resp))
    #app donde se encuenta el bucket
    app_options = {"projectId": "sentimentproject-362601"}
    #Almacena los resultados en la base de datos
    app = firebase_admin.initialize_app(options=app_options)
    database = firestore.client()
    doc = database.collection("employee").document(employee)
    doc.set({
        "name": employee,
        "emotions": resp
    })
    # Elimina el default app
    firebase_admin.delete_app(app)
    return employee + " esta " + str(resp)
