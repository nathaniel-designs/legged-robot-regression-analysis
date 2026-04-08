import pandas as pd
import numpy as np
from pynumdiff.optimize import optimize
from pynumdiff.polynomial_fit import savgoldiff
import rosbag_pandas as rspd

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
    corridor_data = pd.read_csv('corridor/gt_0517_corridor_00.csv')

    print(corridor_data.head())

    # Time step
    dt = 0.1  

    params_roll, _ = optimize(savgoldiff, corridor_data['roll'].to_numpy().astype(float), dt)
    _, drolldt_hat = savgoldiff(corridor_data['roll'].to_numpy().astype(float), dt, **params_roll)

    params_pitch, _ = optimize(savgoldiff, corridor_data['pitch'].to_numpy().astype(float), dt)
    _, dpitchdt_hat = savgoldiff(corridor_data['pitch'].to_numpy().astype(float), dt, **params_pitch)

    params_yaw, _ = optimize(savgoldiff, corridor_data['yaw'].to_numpy().astype(float), dt)
    _, dyawdt_hat = savgoldiff(corridor_data['yaw'].to_numpy().astype(float), dt, **params_yaw)
    
    
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
    df_torque_mags['T_FL_THIGH'] = np.sqrt(np.square(df_torque['T_FL_THIGH_XX']) + np.square(df_torque['T_FL_THIGH_YY']) + np.square(df_torque['T_FL_HIP_ZZ']))
    df_torque_mags['T_FL_CALF'] = np.sqrt(np.square(df_torque['T_FL_CALF_XX']) + np.square(df_torque['T_FL_CALF_YY']) + np.square(df_torque['T_FL_CALF_ZZ']))
    
    df_torque_mags['T_RR_HIP'] = np.sqrt(np.square(df_torque['T_RR_HIP_XX']) + np.square(df_torque['T_RR_HIP_YY']) + np.square(df_torque['T_RR_HIP_ZZ']))
    df_torque_mags['T_RR_THIGH'] = np.sqrt(np.square(df_torque['T_RR_THIGH_XX']) + np.square(df_torque['T_RR_THIGH_YY']) + np.square(df_torque['T_RR_HIP_ZZ']))
    df_torque_mags['T_RR_CALF'] = np.sqrt(np.square(df_torque['T_RR_CALF_XX']) + np.square(df_torque['T_RR_CALF_YY']) + np.square(df_torque['T_RR_CALF_ZZ']))
    
    df_torque_mags['T_RL_HIP'] = np.sqrt(np.square(df_torque['T_RL_HIP_XX']) + np.square(df_torque['T_RL_HIP_YY']) + np.square(df_torque['T_RL_HIP_ZZ']))
    df_torque_mags['T_RL_THIGH'] = np.sqrt(np.square(df_torque['T_RL_THIGH_XX']) + np.square(df_torque['T_RL_THIGH_YY']) + np.square(df_torque['T_RL_HIP_ZZ']))
    df_torque_mags['T_RL_CALF'] = np.sqrt(np.square(df_torque['T_RL_CALF_XX']) + np.square(df_torque['T_RL_CALF_YY']) + np.square(df_torque['T_RL_CALF_ZZ']))
    
    df_torque_mags['Environment'] = 'Corridor'
    df_torque_mags.to_csv('corridor/corridor_tmag_data.csv', index=False)
    df_torque_mags.head()
    
    corridor_bag = rspd.bag_to_dataframe('bags/corridor.bag') 
    corridor_bag.head()

if __name__ == "__main__":
    main()