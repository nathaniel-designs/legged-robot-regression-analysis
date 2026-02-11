import pandas as pd
import numpy as np
from pynumdiff.optimize import optimize
from pynumdiff.polynomial_fit import savgoldiff

def main():
    # Load original CSV
    parking_data = pd.read_csv('parking/gt_0705_parking_00.csv')

    print(parking_data.head())

    # Time step
    dt = 0.1  

    # Calculate velocity components (derivative of position)
    params_vx, val_vx = optimize(savgoldiff, parking_data['trans_x'].to_numpy().astype(float), dt)
    x_hat, dxdt_hat = savgoldiff(parking_data['trans_x'].to_numpy().astype(float), dt, **params_vx)

    params_vy, val_vy = optimize(savgoldiff, parking_data['trans_y'].to_numpy().astype(float), dt)
    y_hat, dydt_hat = savgoldiff(parking_data['trans_y'].to_numpy().astype(float), dt, **params_vy)

    params_vz, val_vz = optimize(savgoldiff, parking_data['trans_z'].to_numpy().astype(float), dt)
    z_hat, dzdt_hat = savgoldiff(parking_data['trans_z'].to_numpy().astype(float), dt, **params_vz)

    # Calculate acceleration components (derivative of velocity)
    params_ax, _ = optimize(savgoldiff, dxdt_hat, dt)
    _, ax_hat = savgoldiff(dxdt_hat, dt, **params_ax)

    params_ay, _ = optimize(savgoldiff, dydt_hat, dt)
    _, ay_hat = savgoldiff(dydt_hat, dt, **params_ay)

    params_az, _ = optimize(savgoldiff, dzdt_hat, dt)
    _, az_hat = savgoldiff(dzdt_hat, dt, **params_az)

    # Calculate compute jerk components (derivative of acceleration)
    params_jx, _ = optimize(savgoldiff, ax_hat, dt)
    _, jx_hat = savgoldiff(ax_hat, dt, **params_jx)

    params_jy, _ = optimize(savgoldiff, ay_hat, dt)
    _, jy_hat = savgoldiff(ay_hat, dt, **params_jy)

    params_jz, _ = optimize(savgoldiff, az_hat, dt)
    _, jz_hat = savgoldiff(az_hat, dt, **params_jz)

    params_roll, val_roll = optimize(savgoldiff, parking_data['roll'].to_numpy().astype(float), dt)
    roll_hat, drolldt_hat = savgoldiff(parking_data['roll'].to_numpy().astype(float), dt, **params_roll)

    params_pitch, val_pitch = optimize(savgoldiff, parking_data['pitch'].to_numpy().astype(float), dt)
    pitch_hat, dpitchdt_hat = savgoldiff(parking_data['pitch'].to_numpy().astype(float), dt, **params_pitch)

    params_yaw, val_yaw = optimize(savgoldiff, parking_data['yaw'].to_numpy().astype(float), dt)
    yaw_hat, dyawdt_hat = savgoldiff(parking_data['yaw'].to_numpy().astype(float), dt, **params_yaw)

    # Compute a 3D vector for angular magnitude, create a new DataFrame to store the angular magnitude, then save angular magnitude to a new CSV
    angular_vel_mag = np.sqrt(np.square(drolldt_hat) + np.square(dpitchdt_hat) + np.square(dyawdt_hat)) # Eliminate three entries for alignment
    angular_vel_mag_data = pd.DataFrame({'angular_vel_mag': angular_vel_mag})
    angular_vel_mag_data['Environment'] = 'Parking Lot'
    angular_vel_mag_data.to_csv('parking/parking_angular_vel_mag_data.csv', index=False)
    print(angular_vel_mag_data.head())

    # Compute a 3D vector for jerk magnitude, create a new DataFrame to store the jerk magnitude, then save jerk magnitude to a new CSV
    jmag = np.sqrt(np.square(jx_hat) + np.square(jy_hat) + np.square(jz_hat))
    jmag_data = pd.DataFrame({'jmag': jmag})
    jmag_data['Environment'] = 'Parking Lot'
    jmag_data.to_csv('parking/parking_jmag_data.csv', index=False)
    print(jmag_data.head())

if __name__ == "__main__":
    main()
