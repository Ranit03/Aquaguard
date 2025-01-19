import pandas as pd
import numpy as np


# Generate simulated sensor data
time = pd.date_range(start="2025-01-12 00:00", end="2025-01-19 00:00", freq="30T")
data = {
    "Time": time,
    "Flow_Sensor1": np.random.uniform(10, 600, len(time)),
    "Pressure_Sensor1": np.random.uniform(1.0, 6.0, len(time)),
    "Temp_Sensor1": np.random.uniform(4, 50, len(time)),
    "Leak_Sensor1": [0 if np.random.uniform(1.0, 6.0) > 1.5 else 1 for _ in range(len(time))],
    "Flow_Sensor2": np.random.uniform(10, 600, len(time)),
    "Pressure_Sensor2": np.random.uniform(1.0, 6.0, len(time)),
}


# Create a DataFrame
df = pd.DataFrame(data)


# Save DataFrame to a CSV file
df.to_csv('sensor_data.csv', index=False)


print("CSV file 'sensor_data.csv' generated successfully!")
