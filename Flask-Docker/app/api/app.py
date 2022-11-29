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

# example (동영상 다운로드)
# path_on_cloud : 동영상이 저장되어있는 위치(영상이름까지 기재)
path_on_cloud = "temp/temp.mp4"
# local_path : local에 동영상을 저장할 위치
local_path = "../../tempDB/temp.mp4"
# 다운로드
storage.child(path_on_cloud).download("",local_path)

# example (동영상 업로드)
# path_on_cloud : 동영상이 저장될 위치(영상이름까지 기재)
path_on_cloud = "temp/temp.mp4"
# local_path : 올릴 동영상이 있는 위치
local_path = "../../tempDB/temp.mp4"
# 업로드
storage.child(path_on_cloud).put(local_path)


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
