from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Global variable to store alcohol level
alcohol_level = 0

# Route to receive sensor data from NodeMCU
@app.route('/submit-data', methods=['GET'])
def submit_data():
    global alcohol_level
    alcohol_level = request.args.get('alcohol', type=float)
    
    # Emit the new alcohol level to the front-end via WebSocket
    socketio.emit('update_alcohol_level', {'alcohol_level': alcohol_level})
    
    return "Data received successfully"

# Route to serve the interactive web page
@app.route('/')
def index():
    return render_template('index.html')

# WebSocket to push the alcohol level data to the front-end
@socketio.on('connect')
def handle_connect():
    # Send the current alcohol level when the client connects
    emit('update_alcohol_level', {'alcohol_level': alcohol_level})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
