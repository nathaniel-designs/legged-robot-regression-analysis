# Compute a 3D vector for angular magnitude, create a new DataFrame to store the angular magnitude, then save angular magnitude to a new CSV
angular_mag = np.sqrt(np.square(parking_data['roll'][3:]) + np.square(parking_data['pitch'][3:]) + np.square(parking_data['yaw'][3:])) # Eliminate three entries for alignment
angular_mag_data = pd.DataFrame({'angular_mag': angular_mag})
angular_mag_data['Environment'] = 'Parking Lot'
angular_mag_data.to_csv('parking/parking_angular_mag_data.csv', index=False)
print(angular_mag_data.head())