import pandas as pd
import numpy as np

# Load original CSV
parking_data = pd.read_csv('gt_0705_parking_00.csv')
print(parking_data.head())

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

# Compute a 3D vector for velocity magnitude (speed), create a new DataFrame to store the speed, then save speed to a new CSV
speed = np.sqrt(np.square(v_x[2:]) + np.square(v_y[2:]) + np.square(v_z[2:]))
speed_data = pd.DataFrame({'speed': speed})
speed_data.to_csv('speed_data.csv', index=False)
print(speed_data.head())

# Compute a 3D vector for angular magnitude, create a new DataFrame to store the angular magnitude, then save angular magnitude to a new CSV
angularmag = np.sqrt(np.square(parking_data['roll'][3:]) + np.square(parking_data['pitch'][3:]) + np.square(parking_data['yaw'][3:]))
angular_data = pd.DataFrame({'angularmag': angularmag})
angular_data.to_csv('angular_data.csv', index=False)
print(angular_data.head())

# Compute a 3D vector for jerk magnitude, create a new DataFrame to store the jerk magnitude, then save jerk magnitude to a new CSV
jmag = np.sqrt(np.square(j_x) + np.square(j_y) + np.square(j_z))
jmag_data = pd.DataFrame({'jmag': jmag})
jmag_data.to_csv('jmag_data.csv', index=False)
print(jmag_data.head())


