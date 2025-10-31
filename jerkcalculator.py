import pandas as pd
import numpy as np

# Load original CSV
parking_data = pd.read_csv('gt_0705_parking_00.csv')

# Time step
dt = 0.1  

# Calculate velocity components (derivative of position)
v_x = np.diff(parking_data['trans_x']) / dt
v_y = np.diff(parking_data['trans_y']) / dt
v_z = np.diff(parking_data['trans_z']) / dt

# Calculate acceleration components (derivative of velocity)
a_x = np.diff(v_x) / dt
a_y = np.diff(v_y) / dt
a_z = np.diff(v_z) / dt

# Calculate compute jerk components (derivative of acceleration)
j_x = np.diff(a_x) / dt
j_y = np.diff(a_y) / dt
j_z = np.diff(a_z) / dt

# Compute a 3D vector for jerk magnitude
jmag = np.sqrt(np.square(j_x) + np.square(j_y) + np.square(j_z))

# Create a new DataFrame to store the jerk magnitude
jmag_data = pd.DataFrame({'jmag': jmag})

# Save jerk magnitude to a new CSV
jmag_data.to_csv('jmag_data.csv', index=False)
print(jmag_data.head())

print("Jerk magnitude data saved to 'jmag_data.csv'")
