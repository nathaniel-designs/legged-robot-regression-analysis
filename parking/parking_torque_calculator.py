import pandas as pd
import numpy as np
from pynumdiff.optimize import optimize
from pynumdiff.polynomial_fit import savgoldiff
from scipy.interpolate import interp1d

HIP_XX = 0.000334008405
HIP_YY = 0.000619101213
HIP_ZZ = 0.00040057614
    
THIGH_XX = 0.004431760472
THIGH_YY = 0.004485671726
THIGH_ZZ = 0.000740309489
    
CALF_XX = 0.001088793059
CALF_YY = 0.001100428748
CALF_ZZ = 0.000024787446

def main():
    # Load original CSV
    parking_data = pd.read_csv('parking/gt_0705_parking_00.csv')
    footforce_data = pd.read_csv('parking/parking_footforce_00.csv')

    # Seperate foot force into the 4 feet.
    footforce_data["sensor"] = footforce_data.groupby("elapsed time").cumcount()
    
    footforce_pivot = footforce_data.pivot_table(index="elapsed time", columns="sensor", values="value")
    
    footforce_pivot.columns = ["Foot 1", "Foot 2", "Foot 3", "Foot 4"]
    footforce_pivot = footforce_pivot.reset_index()
    
    force_cols = ["Foot 1", "Foot 2", "Foot 3", "Foot 4"]
    
    footforce_pivot['FMAG'] = np.linalg.norm(footforce_pivot[force_cols].to_numpy(), axis=1)
    
    footforce_pivot = footforce_pivot.sort_values("elapsed time")
    footforce_pivot = footforce_pivot.drop_duplicates("elapsed time")

    # Time step 
    t_ref = parking_data['time'].to_numpy()
    t_init = footforce_pivot['elapsed time'].to_numpy()
    footforces = footforce_pivot['FMAG'].to_numpy()
    dt_motion = np.mean(np.diff(t_ref))
    dt_force = np.mean(np.diff(t_init))
    
    # Shift to start at 0
    t_ref_elapsed = t_ref - t_ref[0]
    t_init = t_init - t_init[0]
    
    interpolation_func = interp1d(t_init, footforces, kind='linear', bounds_error=False, fill_value=np.nan)
    f_aligned = interpolation_func(t_ref_elapsed)

    params_roll, _ = optimize(savgoldiff, parking_data['roll'].to_numpy().astype(float), dt_motion, maxiter = 50)
    _, drolldt_hat = savgoldiff(parking_data['roll'].to_numpy().astype(float), dt_motion, **params_roll)

    params_pitch, _ = optimize(savgoldiff, parking_data['pitch'].to_numpy().astype(float), dt_motion, maxiter = 50)
    _, dpitchdt_hat = savgoldiff(parking_data['pitch'].to_numpy().astype(float), dt_motion, **params_pitch)

    params_yaw, _ = optimize(savgoldiff, parking_data['yaw'].to_numpy().astype(float), dt_motion, maxiter = 50)
    _, dyawdt_hat = savgoldiff(parking_data['yaw'].to_numpy().astype(float), dt_motion, **params_yaw)
    
    
    # Calculate acceleration components (derivative of velocity)
    params_aroll, _ = optimize(savgoldiff, drolldt_hat, dt_motion, maxiter = 50)
    _, aroll_hat = savgoldiff(drolldt_hat, dt_motion, **params_aroll)
    
    params_apitch, _ = optimize(savgoldiff, dpitchdt_hat, dt_motion, maxiter = 50)
    _, apitch_hat = savgoldiff(dpitchdt_hat, dt_motion, **params_apitch)
    
    params_ayaw, _ = optimize(savgoldiff, dyawdt_hat, dt_motion, maxiter = 50)
    _, ayaw_hat = savgoldiff(dyawdt_hat, dt_motion, **params_ayaw)

    df_accel = pd.DataFrame({
        'alpha_roll': aroll_hat,
        'alpha_pitch': apitch_hat,
        'alpha_yaw': ayaw_hat
    })
    
    df_torque = pd.DataFrame()
    
    df_torque['T_HIP_XX'] = HIP_XX * df_accel['alpha_roll']
    df_torque['T_HIP_YY'] = HIP_YY * df_accel['alpha_pitch']
    df_torque['T_HIP_ZZ'] = HIP_ZZ * df_accel['alpha_yaw']
    
    df_torque['T_THIGH_XX'] = THIGH_XX * df_accel['alpha_roll']
    df_torque['T_THIGH_YY'] = THIGH_YY * df_accel['alpha_pitch']
    df_torque['T_THIGH_ZZ'] = THIGH_ZZ * df_accel['alpha_yaw']
    
    df_torque['T_CALF_XX'] = CALF_XX * df_accel['alpha_roll']
    df_torque['T_CALF_YY'] = CALF_YY * df_accel['alpha_pitch']
    df_torque['T_CALF_ZZ'] = CALF_ZZ * df_accel['alpha_yaw']
    
    df_torque_mags = pd.DataFrame()
    df_torque_mags['T_HIP'] = np.sqrt(np.square(df_torque['T_HIP_XX']) + np.square(df_torque['T_HIP_YY']) + np.square(df_torque['T_HIP_ZZ']))
    df_torque_mags['T_THIGH'] = np.sqrt(np.square(df_torque['T_THIGH_XX']) + np.square(df_torque['T_THIGH_YY']) + np.square(df_torque['T_THIGH_ZZ']))
    df_torque_mags['T_CALF'] = np.sqrt(np.square(df_torque['T_CALF_XX']) + np.square(df_torque['T_CALF_YY']) + np.square(df_torque['T_CALF_ZZ']))
    
    df_torque_mags['Environment'] = 'Parking'
    df_torque_mags.to_csv('parking/parking_tmag_data.csv', index=False)
    df_torque_mags.head()
    
    params_footforce, _ = optimize(savgoldiff, f_aligned.astype(float), dt_force)
    _, dfootforcedt_hat = savgoldiff(f_aligned.astype(float), dt_force, **params_footforce)
    
    dfootforcedt_hat_data = pd.DataFrame({'d_footforce_dt': dfootforcedt_hat})
    dfootforcedt_hat_data['Environment'] = 'Parking'
    dfootforcedt_hat_data.to_csv('parking/parking_dfootforce_dt_data.csv', index=False)
    print(dfootforcedt_hat_data.head())
    
    df_torque_mags['total_torque'] = df_torque_mags.drop(
        columns=['Environment']
    ).sum(axis=1)
    
    df_model = pd.DataFrame({
        "time": t_ref, 
        "total_torque": df_torque_mags['total_torque'],
        "footforce": f_aligned,
        "d_footforce_dt": dfootforcedt_hat,
        "environment": "Parking"
    })
    
    df_model.to_csv('parking/parking_model_data.csv', index=False)
    print(df_model.head())

if __name__ == "__main__":
    main()