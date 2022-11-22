# Import Flask
from flask import Flask, jsonify, request
from utilities import predict_pipeline
import socket

# Make Flask
app = Flask(__name__)


# For the "~/predict" command, execute the following function:
@app.post('/predict')
def predct():
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
    app.run(host=thisIP, debug=True)
    # app.run(host='localhost', debug=True)
