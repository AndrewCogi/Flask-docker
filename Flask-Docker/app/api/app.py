# Import Libraries
from gevent import monkey
monkey.patch_all()

from flask import Flask, jsonify, request
from utilities import predict_pipeline
from gevent.pywsgi import WSGIServer
import cv2
import socket
import json
import pyrebase

with open("auth.json") as f:
    config = json.load(f)

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()



# example (동영상 다운로드)
# path_on_cloud : 동영상이 저장되어있는 위치(영상이름까지 기재)
# path_on_cloud = "bjy123bjy@gmail.com/exercise/unselected/221202/VIDEO_221202_13:30_.mp4"
# path_on_cloud2 = "temp/celebrity.mp4"
# local_path : local에 동영상을 저장할 위치
# local_path = "tempDB/video/bjy123bjy.mp4"
# local_path2 = "tempDB/image/celebrity.mp4"
# 다운로드
# storage.child(path_on_cloud).download("",local_path)
# storage.child(path_on_cloud2).download("",local_path2)

# example (동영상 업로드)
# path_on_cloud : 동영상이 저장될 위치(영상이름까지 기재)
# path_on_cloud = "temp/temp.mp4"
# local_path : 올릴 동영상이 있는 위치
# local_path = "tempDB/video/temp.mp4"
# 업로드
# storage.child(path_on_cloud).put(local_path)



# Make Flask
app = Flask(__name__)

# command : <none>
@app.route('/',methods=['GET','POST'])
def hello():
    return jsonify("Hello Client!")

# command : download
@app.route('/download',methods=['POST'])
def download():
    # Get data in json format
    data = request.json
    print("Get data:", data)

    # download temp.mp4
    if data['fileName'] == 'temp':
        path_on_cloud = "temp/video/temp.mp4"
        local_path = "tempDB/video/temp.mp4"
        storage.child(path_on_cloud).download("",local_path)

    # download celebrity.mp4
    elif data['fileName'] == 'celebrity':
        path_on_cloud = "temp/image/celebrity.mp4"
        local_path = "tempDB/image/celebrity.mp4"
        storage.child(path_on_cloud).download("",local_path)

    return jsonify("Download Complete")

# command : upload
@app.route('/upload',methods=['POST'])
def upload():
    # Get data in json format
    data = request.json
    print("Get data (upload):", data)

    # upload temp.mp4
    if data['fileName'] == 'temp':
        path_on_cloud = "temp/video/temp.mp4"
        local_path = "tempDB/video/temp.mp4"
        storage.child(path_on_cloud).put(local_path)

    # upload celebrity.mp4
    elif data['fileName'] == 'celebrity':
        path_on_cloud = "temp/image/celebrity.mp4"
        local_path = "tempDB/image/celebrity.mp4"
        storage.child(path_on_cloud).put(local_path)

    return jsonify("Upload Complete")



# For the "~/predict" command, execute the following function:
@app.route('/predict',methods=['POST','GET'])
def predict():
    # Get data in json format
    data = request.json
    print("Get data (predict):", data)

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
