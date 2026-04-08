    # Calculate compute jerk components (3rd derivative of position)
    jx_hat = savgol_filter(running_data['trans_x'].to_numpy().astype(float), window_length=5, polyorder=2, delta=dt, deriv=3)
    jy_hat = savgol_filter(running_data['trans_y'].to_numpy().astype(float), window_length=5, polyorder=2, delta=dt, deriv=3)
    jz_hat = savgol_filter(running_data['trans_z'].to_numpy().astype(float), window_length=5, polyorder=2, delta=dt, deriv=3)

    # Calculate angular velocity components
    drolldt_hat = savgol_filter(running_data['roll'].to_numpy().astype(float), window_length=5, polyorder=2, delta=dt, deriv=1)
    dpitchdt_hat = savgol_filter(running_data['pitch'].to_numpy().astype(float), window_length=5, polyorder=2, delta=dt, deriv=1)
    dyawdt_hat = savgol_filter(running_data['yaw'].to_numpy().astype(float), window_length=5, polyorder=2, delta=dt, deriv=1)