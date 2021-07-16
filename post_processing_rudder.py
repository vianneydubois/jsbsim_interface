import pandas
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

JSBSIM_OUTPUT_FILE_PATH_AVL = "aircraft/c172/result.csv"

delta_psi = 15

df1 = pandas.read_csv(JSBSIM_OUTPUT_FILE_PATH_AVL, sep=',')
df1['Psi deg'] = np.rad2deg(df1['/fdm/jsbsim/attitude/psi-rad'])
df1['Delta deg'] = np.rad2deg(df1['/fdm/jsbsim/fcs/rudder-pos-rad'])

psi_0 = df1['Psi deg'][df1['Time'] > 0.05].iat[0]
psi_lim = psi_0 + delta_psi

df1_Phi_lim = df1[df1['Psi deg'] >= psi_lim]

df1_t_lim = df1_Phi_lim.loc[:, 'Time'].iat[0]
print(f't_lim : {df1_t_lim}')

fig, axs = plt.subplots(2, 1)

axs[0].axhline(psi_lim, color='grey', linestyle='dashed', linewidth=1)
axs[0].axvline(df1_t_lim, color='b', linestyle='dashed', linewidth=1)

axs[0].plot(df1['Time'], df1['Psi deg'], color='b', label='AVL')


axs[1].plot(df1['Time'], df1['Delta deg'], color='r')

axs[0].yaxis.set_major_formatter(ticker.FormatStrFormatter('%.f°'))
axs[1].yaxis.set_major_formatter(ticker.FormatStrFormatter('%.f°'))

fig.suptitle('Aileron roll effectiveness simulation - Cessna-like aircraft')
axs[0].grid()
axs[0].set_ylabel("Psi")
axs[0].set_xlabel("Time (s)")
#axs[0].legend()
axs[1].grid()
axs[1].set_xlabel("Time (s)")
axs[1].set_ylabel("Rudder position")
plt.tight_layout()
plt.show()

