import pandas as pd
import numpy as np
import os


def process_rudder(aircraft_name, delta_psi, t_lim):
    jsbsim_output_file = os.path.join('aircraft', aircraft_name, 'result.csv')

    df1 = pd.read_csv(jsbsim_output_file, sep=',')
    df1['Psi deg'] = np.rad2deg(df1['/fdm/jsbsim/attitude/psi-rad'])
    df1['Delta deg'] = np.rad2deg(df1['/fdm/jsbsim/fcs/rudder-pos-rad'])

    psi_0 = df1['Psi deg'][df1['Time'] > 0.05].iat[0]
    psi_lim = psi_0 + delta_psi

    df1_Phi_lim = df1[df1['Psi deg'] >= psi_lim]

    df1_t_lim = df1_Phi_lim.loc[:, 'Time'].iat[0] - 1  # -1.0 sec because manoeuvre starts at t + 1.0 s
    print(f't_yaw : {df1_t_lim}')

    return df1_t_lim < t_lim


def process_roll(aircraft_name, delta_phi, t_lim):
    jsbsim_output_file = os.path.join('aircraft', aircraft_name, 'result.csv')

    df1 = pd.read_csv(jsbsim_output_file, sep=',')
    df1['Phi deg'] = np.rad2deg(df1['/fdm/jsbsim/attitude/phi-rad'])
    df1['Delta deg'] = np.rad2deg(df1['/fdm/jsbsim/fcs/right-aileron-pos-rad'])

    psi_0 = df1['Phi deg'][df1['Time'] > 0.05].iat[0]
    psi_lim = psi_0 + delta_phi

    df1_Phi_lim = df1[df1['Phi deg'] <= psi_lim]

    df1_t_lim = df1_Phi_lim.loc[:, 'Time'].iat[0] - 1  # -1.0 sec because manoeuvre starts at t + 1.0 s
    print(f't_roll : {df1_t_lim}')

    return df1_t_lim < t_lim
