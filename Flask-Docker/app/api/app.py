# Import Flask
from flask import Flask, jsonify, request
from utilities import predict_pipeline
from gevent.pywsgi import WSGIServer
import socket
import json
import pyrebase

with open("auth.json") as f:
    config = json.load(f)

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

# test
import cv2
# cap = cv2.VideoCapture("../../../Pose_Similarity_Check_Flask/videos/Workout.mp4")
# cap = "../../../Pose_Similarity_Check_Flask/images/1.jpeg"
# signin = {"pw":"12341234","ID":"cho"}
# storage.child("images/1.jpeg").put(cap)

# test
# path_on_cloud = "temp/1.jpeg"
# fileName = "1.jpeg"
# storage.child(path_on_cloud).download("","IMAGES/temp.jpg")

# test
path_on_cloud = "drj9802@gmail.com/balance/220911/VIDEO_220911_23:58_.mp4"
fileName = "1.jpeg"
storage.child(path_on_cloud).download("","../../tempDB/temp.mp4")

# storage.child("temp/temp.mp4").put("IMAGES/temp.mp4")

# Make Flask
app = Flask(__name__)


# For the "~/predict" command, execute the following function:
@app.route('/predict',methods=['POST','GET'])
def predict():
    # Get data in json format
    data = request.json
    print("Get data:", data)

    # Exception 1 : There is no data
    try:
        sample = data['data']
    except KeyError:
        return jsonify({'error': 'No data sent'})

    # predict the result
    sample = [sample]
    predictions = predict_pipeline(sample)

    # Exception 2 : There is wrong input data
    try:
        result = jsonify(predictions[0])
    except TypeError as e:
        return jsonify({'error': str(e)+'aa'})

    # Return result
    return result


# Run Flask server
if __name__ == "__main__":
    thisIP = socket.gethostbyname(socket.gethostname())
    print("This PC IP:", thisIP)
    # app.run(host=thisIP, debug=True)
    # app.run(host='localhost', debug=True)
    http_server = WSGIServer((thisIP,5000),app)
    http_server.serve_forever()
