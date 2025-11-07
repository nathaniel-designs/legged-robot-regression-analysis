import pandas as pd
import numpy as np

# Load original CSV
corridor_data = pd.read_csv('corridor/gt_0517_corridor_00.csv')

print(corridor_data.head())

# Time step
dt = 0.1  

# Calculate velocity components (derivative of position)
v_x = np.diff(corridor_data['trans_x']) / dt
v_y = np.diff(corridor_data['trans_y']) / dt
v_z = np.diff(corridor_data['trans_z']) / dt

# Calculate acceleration components (derivative of velocity)
a_x = np.diff(v_x) / dt
a_y = np.diff(v_y) / dt
a_z = np.diff(v_z) / dt

# Calculate compute jerk components (derivative of acceleration)
j_x = np.diff(a_x) / dt
j_y = np.diff(a_y) / dt
j_z = np.diff(a_z) / dt

angular_roll = np.diff(corridor_data['roll']) / dt
angular_pitch = np.diff(corridor_data['pitch']) / dt
angular_yaw = np.diff(corridor_data['yaw']) / dt

# Compute a 3D vector for angular magnitude, create a new DataFrame to store the angular magnitude, then save angular magnitude to a new CSV
angular_v_mag = np.sqrt(np.square(angular_roll[2:]) + np.square(angular_pitch[2:]) + np.square(angular_yaw[2:])) # Eliminate three entries for alignment
angular_vmag_data = pd.DataFrame({'angular_v_mag': angular_v_mag})
angular_vmag_data['Environment'] = 'Corridor'
angular_vmag_data.to_csv('corridor/corridor_angular_vmag_data.csv', index=False)
print(angular_vmag_data.head())

# Compute a 3D vector for jerk magnitude, create a new DataFrame to store the jerk magnitude, then save jerk magnitude to a new CSV
jmag = np.sqrt(np.square(j_x) + np.square(j_y) + np.square(j_z))
jmag_data = pd.DataFrame({'jmag': jmag})
jmag_data['Environment'] = 'Corridor'
jmag_data.to_csv('corridor/corridor_jmag_data.csv', index=False)
print(jmag_data.head())


