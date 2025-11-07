import pandas as pd
import numpy as np

# Load original CSV
indoor_data = pd.read_csv('indoor/gt_0517_indoor_00.csv')

print(indoor_data.head())

# Time step
dt = 0.1  

# Calculate velocity components (derivative of position)
v_x = np.diff(indoor_data['trans_x']) / dt
v_y = np.diff(indoor_data['trans_y']) / dt
v_z = np.diff(indoor_data['trans_z']) / dt

# Calculate acceleration components (derivative of velocity)
a_x = np.diff(v_x) / dt
a_y = np.diff(v_y) / dt
a_z = np.diff(v_z) / dt

# Calculate compute jerk components (derivative of acceleration)
j_x = np.diff(a_x) / dt
j_y = np.diff(a_y) / dt
j_z = np.diff(a_z) / dt

# Compute a 3D vector for angular magnitude, create a new DataFrame to store the angular magnitude, then save angular magnitude to a new CSV
angular_mag = np.sqrt(np.square(indoor_data['roll'][3:]) + np.square(indoor_data['pitch'][3:]) + np.square(indoor_data['yaw'][3:])) # Eliminate three entries for alignment
angular_mag_data = pd.DataFrame({'angular_mag': angular_mag})
angular_mag_data['Environment'] = 'Indoor'
angular_mag_data.to_csv('indoor/indoor_angular_mag_data.csv', index=False)
print(angular_mag_data.head())

# Compute a 3D vector for jerk magnitude, create a new DataFrame to store the jerk magnitude, then save jerk magnitude to a new CSV
jmag = np.sqrt(np.square(j_x) + np.square(j_y) + np.square(j_z))
jmag_data = pd.DataFrame({'jmag': jmag})
jmag_data['Environment'] = 'Indoor'
jmag_data.to_csv('indoor/indoor_jmag_data.csv', index=False)
print(jmag_data.head())