import pandas as pd
import numpy as np
from pynumdiff.optimize import optimize
from pynumdiff.polynomial_fit import savgoldiff
from scipy.interpolate import interp1d

FR_HIP_XX = 0.000334008405
FR_HIP_YY = 0.000619101213
FR_HIP_ZZ = 0.00040057614
    
FR_THIGH_XX = 0.004431760472
FR_THIGH_YY = 0.004485671726
FR_THIGH_ZZ = 0.000740309489
    
FR_CALF_XX = 0.001088793059
FR_CALF_YY = 0.001100428748
FR_CALF_ZZ = 0.000024787446
    
FL_HIP_XX = 0.000334008405
FL_HIP_YY = 0.000619101213
FL_HIP_ZZ = 0.00040057614
    
FL_THIGH_XX = 0.004431760472
FL_THIGH_YY = 0.004485671726
FL_THIGH_ZZ = 0.000740309489
    
FL_CALF_XX = 0.001088793059
FL_CALF_YY = 0.001100428748
FL_CALF_ZZ = 0.000024787446
    
RR_HIP_XX = 0.000334008405
RR_HIP_YY = 0.000619101213
RR_HIP_ZZ = 0.00040057614
    
RR_THIGH_XX = 0.004431760472
RR_THIGH_YY = 0.004485671726
RR_THIGH_ZZ = 0.000740309489
    
RR_CALF_XX = 0.001088793059
RR_CALF_YY = 0.001100428748
RR_CALF_ZZ = 0.000024787446
    
RL_HIP_XX = 0.000334008405
RL_HIP_YY = 0.000619101213
RL_HIP_ZZ = 0.00040057614
    
RL_THIGH_XX = 0.004431760472
RL_THIGH_YY = 0.004485671726
RL_THIGH_ZZ = 0.000740309489
    
RL_CALF_XX = 0.001088793059
RL_CALF_YY = 0.001100428748
RL_CALF_ZZ = 0.000024787446

def main():
    # Load original CSV
    running_data = pd.read_csv('running/gt_0705_running_00.csv')
    footforce_data = pd.read_csv('running/running_footforce_00.csv')

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
    t_ref = running_data['time'].to_numpy()
    t_init = footforce_pivot['elapsed time'].to_numpy()
    footforces = footforce_pivot['FMAG'].to_numpy()
    dt = np.mean(np.diff(t_ref))
    
    # Shift to start at 0
    t_ref_elapsed = t_ref - t_ref[0]
    
    interpolation_func = interp1d(t_init, footforces, kind='linear', fill_value='extrapolate')
    f_aligned = interpolation_func(t_ref_elapsed)

    params_roll, _ = optimize(savgoldiff, running_data['roll'].to_numpy().astype(float), dt)
    _, drolldt_hat = savgoldiff(running_data['roll'].to_numpy().astype(float), dt, **params_roll)

    params_pitch, _ = optimize(savgoldiff, running_data['pitch'].to_numpy().astype(float), dt)
    _, dpitchdt_hat = savgoldiff(running_data['pitch'].to_numpy().astype(float), dt, **params_pitch)

    params_yaw, _ = optimize(savgoldiff, running_data['yaw'].to_numpy().astype(float), dt)
    _, dyawdt_hat = savgoldiff(running_data['yaw'].to_numpy().astype(float), dt, **params_yaw)
    
    
    # Calculate acceleration components (derivative of velocity)
    params_aroll, _ = optimize(savgoldiff, drolldt_hat, dt)
    _, aroll_hat = savgoldiff(drolldt_hat, dt, **params_aroll)
    
    params_apitch, _ = optimize(savgoldiff, dpitchdt_hat, dt)
    _, apitch_hat = savgoldiff(dpitchdt_hat, dt, **params_apitch)
    
    params_ayaw, _ = optimize(savgoldiff, dyawdt_hat, dt)
    _, ayaw_hat = savgoldiff(dyawdt_hat, dt, **params_ayaw)

    df_accel = pd.DataFrame({
        'alpha_roll': aroll_hat,
        'alpha_pitch': apitch_hat,
        'alpha_yaw': ayaw_hat
    })
    
    df_torque = pd.DataFrame()
    
    df_torque['T_FR_HIP_XX'] = FR_HIP_XX * df_accel['alpha_roll']
    df_torque['T_FR_HIP_YY'] = FR_HIP_YY * df_accel['alpha_pitch']
    df_torque['T_FR_HIP_ZZ'] = FR_HIP_ZZ * df_accel['alpha_yaw']
    
    df_torque['T_FR_THIGH_XX'] = FR_THIGH_XX * df_accel['alpha_roll']
    df_torque['T_FR_THIGH_YY'] = FR_THIGH_YY * df_accel['alpha_pitch']
    df_torque['T_FR_THIGH_ZZ'] = FR_THIGH_ZZ * df_accel['alpha_yaw']
    
    df_torque['T_FR_CALF_XX'] = FR_CALF_XX * df_accel['alpha_roll']
    df_torque['T_FR_CALF_YY'] = FR_CALF_YY * df_accel['alpha_pitch']
    df_torque['T_FR_CALF_ZZ'] = FR_CALF_ZZ * df_accel['alpha_yaw']
    
    df_torque['T_FL_HIP_XX'] = FL_HIP_XX * df_accel['alpha_roll']
    df_torque['T_FL_HIP_YY'] = FL_HIP_YY * df_accel['alpha_pitch']
    df_torque['T_FL_HIP_ZZ'] = FL_HIP_ZZ * df_accel['alpha_yaw']
    
    df_torque['T_FL_THIGH_XX'] = FL_THIGH_XX * df_accel['alpha_roll']
    df_torque['T_FL_THIGH_YY'] = FL_THIGH_YY * df_accel['alpha_pitch']
    df_torque['T_FL_THIGH_ZZ'] = FL_THIGH_ZZ * df_accel['alpha_yaw']
    
    df_torque['T_FL_CALF_XX'] = FL_CALF_XX * df_accel['alpha_roll']
    df_torque['T_FL_CALF_YY'] = FL_CALF_YY * df_accel['alpha_pitch']
    df_torque['T_FL_CALF_ZZ'] = FL_CALF_ZZ * df_accel['alpha_yaw']
    
    df_torque['T_RR_HIP_XX'] = RR_HIP_XX * df_accel['alpha_roll']
    df_torque['T_RR_HIP_YY'] = RR_HIP_YY * df_accel['alpha_pitch']
    df_torque['T_RR_HIP_ZZ'] = RR_HIP_ZZ * df_accel['alpha_yaw']
    
    df_torque['T_RR_THIGH_XX'] = RR_THIGH_XX * df_accel['alpha_roll']
    df_torque['T_RR_THIGH_YY'] = RR_THIGH_YY * df_accel['alpha_pitch']
    df_torque['T_RR_THIGH_ZZ'] = RR_THIGH_ZZ * df_accel['alpha_yaw']
    
    df_torque['T_RR_CALF_XX'] = RR_CALF_XX * df_accel['alpha_roll']
    df_torque['T_RR_CALF_YY'] = RR_CALF_YY * df_accel['alpha_pitch']
    df_torque['T_RR_CALF_ZZ'] = RR_CALF_ZZ * df_accel['alpha_yaw']
    
    df_torque['T_RL_HIP_XX'] = RL_HIP_XX * df_accel['alpha_roll']
    df_torque['T_RL_HIP_YY'] = RL_HIP_YY * df_accel['alpha_pitch']
    df_torque['T_RL_HIP_ZZ'] = RL_HIP_ZZ * df_accel['alpha_yaw']
    
    df_torque['T_RL_THIGH_XX'] = RL_THIGH_XX * df_accel['alpha_roll']
    df_torque['T_RL_THIGH_YY'] = RL_THIGH_YY * df_accel['alpha_pitch']
    df_torque['T_RL_THIGH_ZZ'] = RL_THIGH_ZZ * df_accel['alpha_yaw']
    
    df_torque['T_RL_CALF_XX'] = RL_CALF_XX * df_accel['alpha_roll']
    df_torque['T_RL_CALF_YY'] = RL_CALF_YY * df_accel['alpha_pitch']
    df_torque['T_RL_CALF_ZZ'] = RL_CALF_ZZ * df_accel['alpha_yaw']
    
    df_torque_mags = pd.DataFrame()
    df_torque_mags['T_FR_HIP'] = np.sqrt(np.square(df_torque['T_FR_HIP_XX']) + np.square(df_torque['T_FR_HIP_YY']) + np.square(df_torque['T_FR_HIP_ZZ']))
    df_torque_mags['T_FR_THIGH'] = np.sqrt(np.square(df_torque['T_FR_THIGH_XX']) + np.square(df_torque['T_FR_THIGH_YY']) + np.square(df_torque['T_FR_THIGH_ZZ']))
    df_torque_mags['T_FR_CALF'] = np.sqrt(np.square(df_torque['T_FR_CALF_XX']) + np.square(df_torque['T_FR_CALF_YY']) + np.square(df_torque['T_FR_CALF_ZZ']))

    df_torque_mags['T_FL_HIP'] = np.sqrt(np.square(df_torque['T_FL_HIP_XX']) + np.square(df_torque['T_FL_HIP_YY']) + np.square(df_torque['T_FL_HIP_ZZ']))
    df_torque_mags['T_FL_THIGH'] = np.sqrt(np.square(df_torque['T_FL_THIGH_XX']) + np.square(df_torque['T_FL_THIGH_YY']) + np.square(df_torque['T_FL_THIGH_ZZ']))
    df_torque_mags['T_FL_CALF'] = np.sqrt(np.square(df_torque['T_FL_CALF_XX']) + np.square(df_torque['T_FL_CALF_YY']) + np.square(df_torque['T_FL_CALF_ZZ']))
    
    df_torque_mags['T_RR_HIP'] = np.sqrt(np.square(df_torque['T_RR_HIP_XX']) + np.square(df_torque['T_RR_HIP_YY']) + np.square(df_torque['T_RR_HIP_ZZ']))
    df_torque_mags['T_RR_THIGH'] = np.sqrt(np.square(df_torque['T_RR_THIGH_XX']) + np.square(df_torque['T_RR_THIGH_YY']) + np.square(df_torque['T_RR_THIGH_ZZ']))
    df_torque_mags['T_RR_CALF'] = np.sqrt(np.square(df_torque['T_RR_CALF_XX']) + np.square(df_torque['T_RR_CALF_YY']) + np.square(df_torque['T_RR_CALF_ZZ']))
    
    df_torque_mags['T_RL_HIP'] = np.sqrt(np.square(df_torque['T_RL_HIP_XX']) + np.square(df_torque['T_RL_HIP_YY']) + np.square(df_torque['T_RL_HIP_ZZ']))
    df_torque_mags['T_RL_THIGH'] = np.sqrt(np.square(df_torque['T_RL_THIGH_XX']) + np.square(df_torque['T_RL_THIGH_YY']) + np.square(df_torque['T_RL_THIGH_ZZ']))
    df_torque_mags['T_RL_CALF'] = np.sqrt(np.square(df_torque['T_RL_CALF_XX']) + np.square(df_torque['T_RL_CALF_YY']) + np.square(df_torque['T_RL_CALF_ZZ']))
    
    df_torque_mags['Environment'] = 'Running'
    df_torque_mags.to_csv('running/running_tmag_data.csv', index=False)
    df_torque_mags.head()
    
    params_footforce, _ = optimize(savgoldiff, f_aligned.astype(float), dt)
    _, dfootforcedt_hat = savgoldiff(f_aligned.astype(float), dt, **params_footforce)
    
    dfootforcedt_hat_data = pd.DataFrame({'d_footforce_dt': dfootforcedt_hat})
    dfootforcedt_hat_data['Environment'] = 'Running'
    dfootforcedt_hat_data.to_csv('running/running_dfootforce_dt_data.csv', index=False)
    print(dfootforcedt_hat_data.head())
    
    df_footforce = pd.DataFrame({
        "time": t_ref,        
        "f_aligned": f_aligned
    })
    df_footforce.to_csv('running/running_footforce_data.csv', index=False)
    print(df_footforce.head())
    
if __name__ == "__main__":
    main()