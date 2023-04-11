import os
import boto3
from flask import Flask, request, render_template
from dotenv import load_dotenv

load_dotenv()
consumer_key = os.getenv('ID_SECRET')
consumer_secret = os.getenv('USER_SECRET')


# configurar el cliente de Amazon Rekognition
client = boto3.client('rekognition')

# configurar la aplicación Flask
app = Flask(__name__)

# ruta para mostrar el formulario
@app.route('/')
def index():
    return render_template('form.html')
        

# ruta para procesar la imagen
@app.route('/', methods=['POST'])
def process_image():
    # obtener el archivo de imagen subido por el usuario
    image = request.files['image']

    # convertir la imagen a bytes
    imgbytes = image.read()

    # realizar la detección de objetos en la imagen
    response = client.detect_labels(
        Image={
            'Bytes': imgbytes
        },
        MaxLabels=10
    )
    
    print(response)
    
    # imprimir los resultados de la detección de objetos
    objects = []
    for label in response['Labels']:
        objects.append({'name': label['Name'], 'confidence': label['Confidence']})
        

    # mostrar los resultados en una página web
    return render_template('results.html', objects=objects)

# iniciar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)
