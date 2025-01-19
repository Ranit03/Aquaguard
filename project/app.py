from flask import Flask, render_template
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

app = Flask(__name__)

@app.route('/')
def home():
    # Load the CSV file
    df = pd.read_csv('sensor_data.csv')

    flow_high_threshold = 300
    flow_low_threshold = 50
    pressure_leak_threshold = 1.5
    pressure_drop_threshold = 0.5
    temp_low_threshold = 4
    temp_high_threshold = 50

    # Features and target variable for the model
    df["Flow_Status"] = df["Flow_Sensor1"].apply(
        lambda x: "High Usage" if x > flow_high_threshold else ("Low Usage" if x < flow_low_threshold else "Normal")
    )
    df["Pressure_Status"] = df["Pressure_Sensor1"].apply(
        lambda x: "Leak Detected" if x < pressure_leak_threshold else "Normal"
    )
    df["Temp_Status"] = df["Temp_Sensor1"].apply(
        lambda x: "Too Low" if x < temp_low_threshold else ("Too High" if x > temp_high_threshold else "Optimal")
    )

    # Calculate pressure drop for leak detection
    df["Pressure_Drop"] = df["Pressure_Sensor1"].diff().abs()

    # Calculate flow difference between two sensors (Sensor1 - Sensor2) for leak detection
    df["Flow_Difference"] = (df["Flow_Sensor1"] - df["Flow_Sensor2"]).abs()

    # Prepare data for machine learning model (Features and labels)
    df['Leak'] = (df['Pressure_Drop'] > pressure_drop_threshold).astype(int)
    df['Peak_Hour'] = df['Flow_Difference'].apply(
        lambda x: 1 if (x > flow_high_threshold) else 0
    )

    features = ['Flow_Sensor1', 'Flow_Sensor2', 'Pressure_Sensor1', 'Pressure_Sensor2', 'Temp_Sensor1']
    X = df[features]
    y_peak = df['Peak_Hour']
    y_leak = df['Leak']

    # Split the dataset for training and testing
    X_train, X_test, y_train_peak, y_test_peak, y_train_leak, y_test_leak = train_test_split(X, y_peak, y_leak, test_size=0.2, random_state=42)

    # Initialize models
    peak_model = RandomForestClassifier(n_estimators=100, random_state=42)
    leak_model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Train the models
    peak_model.fit(X_train, y_train_peak)
    leak_model.fit(X_train, y_train_leak)

    # Predictions
    y_pred_peak = peak_model.predict(X_test)
    y_pred_leak = leak_model.predict(X_test)

    # Calculate accuracy
    peak_hour_accuracy = accuracy_score(y_test_peak, y_pred_peak) * 100
    leak_detection_accuracy = accuracy_score(y_test_leak, y_pred_leak) * 100

    # Predictions and Recommendations
    df["Predicted_Peak_Hour"] = peak_model.predict(X[features])
    df["Predicted_Leak"] = leak_model.predict(X[features])

    # Recommendations for Peak Hours
    peak_hour_recommendations = df[df["Predicted_Peak_Hour"] == 1]
    peak_hour_ranges = []

    if not peak_hour_recommendations.empty:
        peak_hour_ranges = sorted(peak_hour_recommendations.groupby("Time")["Flow_Difference"].mean().sort_values(ascending=False).head(3).index)

    # Maintenance Recommendations
    maintenance_recommendations = []
    if df["Flow_Status"].str.contains("High Usage|Low Usage").any():
        maintenance_recommendations.append("- Investigate flow anomalies and optimize water usage.")
    if df["Pressure_Status"].str.contains("Leak Detected").any():
        maintenance_recommendations.append("- Check high-risk areas for leaks and repair as needed.")
    if df["Temp_Status"].str.contains("Too High|Too Low").any():
        maintenance_recommendations.append("- Adjust temperature settings to prevent pipe damage.")

    return render_template(
        'index.html', 
        peak_hour_accuracy=peak_hour_accuracy,
        leak_detection_accuracy=leak_detection_accuracy,
        maintenance_recommendations=maintenance_recommendations,
        peak_hour_ranges=peak_hour_ranges,
        peak_hour_recommendations=peak_hour_recommendations
    )

if __name__ == '__main__':
    app.run(debug=True)
