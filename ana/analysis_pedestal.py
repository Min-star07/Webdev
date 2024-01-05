import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import seaborn as sns
plt.style.use("mystyle.txt")

# # Create a 3x3 grid of plots
# fig, axs = plt.subplots(3, 3, figsize=(10, 10))

# # Flatten the 3x3 array of axes to iterate over them
# axs = axs.flatten()

# Plot on each axis
# for i, ax in enumerate(axs):
# Thus we have to give more margin:

for i in range(8):
    # if i == 8:
    #     break
    fig, ax = plt.subplots()
    plt.subplots_adjust(right=0.88)
    filename = "/ROB_" + str(i) + "_final_result.txt"
    df1 = pd.read_csv("./Final_Result_test1"+filename, sep="\t")
    print(df1)
    # df2 = pd.read_csv("./Final_Result_test2"+filename, sep="\t")
    # print(df2)
    df3 = pd.read_csv("./Final_Result_test3"+filename, sep="\t")
    print(df3)
    reletive_ratio = (df1["ped_mean"] - df3["ped_mean"])/df3["ped_mean"]*100
    y_max = np.max(reletive_ratio)
    print(y_max)
    print("===================================================")
    y_min = np.min(reletive_ratio)
    y_mean = np.mean(reletive_ratio)
    y_std = np.std(reletive_ratio)
    y1_mean = np.mean(df1["ped_mean"])
    y1_std = np.std(df1["ped_mean"])
    y3_mean = np.mean(df3["ped_mean"])
    y3_std = np.std(df3["ped_mean"])
    # ax = ax.axes(xlim=[0,63], ylim =[-20,50], xlabel='Channel', ylabel=r'Pedestal mean [ADC]') #r"$\\frac{{\\chi^2}}{{\\text{{NDF}}}}"
    ax.scatter(df1["Channel"], df1["ped_mean"] , marker = 'o', c="blue", label ="data 1: mean = %.1f, std = %.1f" %(y1_mean, y1_std))  # Plotting the histogram
    # ax.scatter(df2["Channel"], df2["ped_mean"] , marker = 'o', c="blue", label ="data 2")  # Plotting the histogram
    ax.scatter(df3["Channel"], df3["ped_mean"] , marker = 'o', c="red", label ="data 3: mean = %.1f, std = %.1f" %(y3_mean, y3_std))  # Plotting the histogram
    ax.set_xlabel('Channel')
    ax.set_xlim(0,63)
    ax.set_ylim(-10, 60)
    ax.set_ylabel('Pedestal mean [ADC]', color='k')
    ax.tick_params(axis='y', labelcolor='k')
    # Creating a secondary y-axis
    ax2 = ax.twinx()
    # ax2 = ax2.axes(xlim=[0,63], ylim =[-20,50], xlabel='Channel', ylabel=r'Relative ratio [%]') #r"$\\frac{{\\chi^2}}{{\\text{{NDF}}}}"
    ax2.scatter(df3["Channel"], reletive_ratio , marker = '+', c="darkgreen", label ="Relative ratio : mean = %.1f, std = %.1f" %(y_mean, y_std) )  # Plotting the histogram
    ax2.fill_between(x=df1["Channel"], y1=y_min, y2=y_max, color='pink',  interpolate=True, alpha=.2)
    ax2.tick_params(axis='y', labelcolor='darkgreen')
    plt.title("ROB " + str(i))
    ax2.set_xlabel('Channel')
    ax2.set_xlim(0,63)
    ax2.set_ylim(-10, 60)
    ax2.tick_params(axis='y', labelcolor='darkgreen')
    ax2.set_ylabel('Relative ratio [%]', color='darkgreen')

    # Displaying legends for both plots
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper right')

    plt.savefig("pedestal_check"+str(i)+".pdf")
    plt.show()



