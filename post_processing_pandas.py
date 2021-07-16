import pandas
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

JSBSIM_OUTPUT_FILE_PATH_AVL = "aircraft/c172/result.csv"
JSBSIM_OUTPUT_FILE_PATH_AEROMATIC = "/Users/vianneydubois/Documents/Cours/Supaéro/Stage S4 DCAS/JSBSim/essais/aircraft/cessna172/essai.csv"

Phi_lim = -60

df1 = pandas.read_csv(JSBSIM_OUTPUT_FILE_PATH_AVL, sep=',')
df1['Phi deg'] = np.rad2deg(df1['/fdm/jsbsim/attitude/phi-rad'])
df1['Delta deg'] = np.rad2deg(df1['/fdm/jsbsim/fcs/right-aileron-pos-rad'])

df2 = pandas.read_csv(JSBSIM_OUTPUT_FILE_PATH_AEROMATIC, sep=',')
df2['Phi deg'] = np.rad2deg(df2['/fdm/jsbsim/attitude/phi-rad'])
df2['Delta deg'] = np.rad2deg(df2['/fdm/jsbsim/fcs/right-aileron-pos-rad'])

df1_Phi_lim = df1[df1['Phi deg'] <= Phi_lim]
df2_Phi_lim = df2[df2['Phi deg'] <= Phi_lim]

df1_t_lim = df1_Phi_lim.loc[:, 'Time'].iat[0]
df2_t_lim = df2_Phi_lim.loc[:, 'Time'].iat[0]

print(f'AVL : {df1_t_lim}, AEROMATIC : {df2_t_lim}')

fig, axs = plt.subplots(2, 1)

axs[0].axhline(Phi_lim, color='grey', linestyle='dashed', linewidth=1)
axs[0].axvline(df1_t_lim, color='b', linestyle='dashed', linewidth=1)
#axs[0].axvline(df2_t_lim, color='g', linestyle='dashed', linewidth=1)

axs[0].plot(df1['Time'], df1['Phi deg'], color='b', label='AVL')
#axs[0].plot(df2['Time'], df2['Phi deg'], color='g', label='AeromatiC++')


axs[1].plot(df1['Time'], df1['Delta deg'], color='r')

axs[0].yaxis.set_major_formatter(ticker.FormatStrFormatter('%.f°'))
axs[1].yaxis.set_major_formatter(ticker.FormatStrFormatter('%.f°'))

fig.suptitle('Aileron roll effectiveness simulation - Cessna-like aircraft')
axs[0].grid()
axs[0].set_ylabel("Phi")
axs[0].set_xlabel("Time (s)")
axs[0].legend()
axs[1].grid()
axs[1].set_xlabel("Time (s)")
axs[1].set_ylabel("Aileron position")
plt.tight_layout()
plt.show()

