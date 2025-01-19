from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import time
import threading
import csv
import os

app = Flask(__name__)
socketio = SocketIO(app)

# File paths
SENSOR_1_FILE = 'sensor_data_1.csv'
SENSOR_2_FILE = 'sensor_data_2.csv'

# Function to read data from a CSV file
def read_csv_file(file_path):
    data = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append({
                'timestamp': row['timestamp'],
                'flow': float(row['flow']),
                'pressure': float(row['pressure']),
                'temperature': float(row['temperature'])
            })
    return data

# Load the sensor data from the CSV files
sensor_1_data = read_csv_file(SENSOR_1_FILE)
sensor_2_data = read_csv_file(SENSOR_2_FILE)

# Function to emit data from the CSV files every second
def emit_sensor_data():
    index = 0
    while True:
        if index < len(sensor_1_data):
            data_1 = sensor_1_data[index]
            data_2 = sensor_2_data[index]
            timestamp = data_1['timestamp']
            flow = [data_1['flow'], data_2['flow']]
            pressure = [data_1['pressure'], data_2['pressure']]
            temperature = [data_1['temperature'], data_2['temperature']]

            # Detect leakage
            flow_leakage = flow[0] < 8 or flow[0] > 18 or flow[1] < 8 or flow[1] > 18
            pressure_leakage = pressure[0] < 2 or pressure[0] > 4 or pressure[1] < 2 or pressure[1] > 4

            # Prepare data packet
            data = {
                "timestamp": timestamp,
                "flow": flow,
                "pressure": pressure,
                "temperature": temperature,
                "flow_leakage": flow_leakage,
                "pressure_leakage": pressure_leakage,
            }

            # Emit data to clients
            socketio.emit('sensor_data', data)
            index += 1
            time.sleep(1)  # Emit data every second

# Route for the dashboard
@app.route('/')
def index():
    return render_template('index.html')

# Route for the user interface page
@app.route('/user-interface')
def user_interface():
    return render_template('user_interface.html')

# Route to serve the CSV files
@app.route('/files/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.getcwd(), filename)

# Start emitting data in a background thread
thread = threading.Thread(target=emit_sensor_data, daemon=True)
thread.start()

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
