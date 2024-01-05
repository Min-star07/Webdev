import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import seaborn as sns
plt.style.use("mystyle.txt")

for i in range(8):
    # 
    fig, ax2 = plt.subplots()
    plt.subplots_adjust(right=0.88)
    filename = "/fit_result_ROB_" + str(i) + ".txt"
    df1 = pd.read_csv("../Result_test1"+filename, sep="\t")
    df_sigma0 = df1[df1["Sigma"] == 0]
    df_sigma1 = df1[df1["Sigma"] == 1]
    df_sigma2 = df1[df1["Sigma"] == 2]
    df_sigma3 = df1[df1["Sigma"] == 3]
    df_sigma_1 = df1[df1["Sigma"] == -1]
    df_sigma_2 = df1[df1["Sigma"] == -2]
    df_sigma_3 = df1[df1["Sigma"] == -3]


    df_sigma0.reset_index(inplace=True)
    df_sigma1.reset_index(inplace=True)
    df_sigma2.reset_index(inplace=True)
    df_sigma3.reset_index(inplace=True)
   
    df_sigma_1.reset_index(inplace=True)
    df_sigma_2.reset_index(inplace=True)
    df_sigma_3.reset_index(inplace=True)
    print(df_sigma0)
    print(df_sigma1)
    print(df_sigma2)
    print(df_sigma3)
    print(df_sigma3["Q_{1}"])
    print(df_sigma3["Q_{1}"] - df_sigma0["Q_{1}"])
    
  
    ratio_sigma0 = (df_sigma0["Q_{1}"] - df_sigma3["Q_{1}"])/df_sigma3["Q_{1}"] *100
    ratio_sigma1 = (df_sigma1["Q_{1}"] - df_sigma3["Q_{1}"])/df_sigma3["Q_{1}"] *100
    ratio_sigma2 = (df_sigma2["Q_{1}"] - df_sigma3["Q_{1}"])/df_sigma3["Q_{1}"] *100
    ratio_sigma_1 = (df_sigma_1["Q_{1}"] - df_sigma3["Q_{1}"])/df_sigma3["Q_{1}"] *100
    ratio_sigma_2 = (df_sigma_2["Q_{1}"] - df_sigma3["Q_{1}"])/df_sigma3["Q_{1}"] *100
    ratio_sigma_3 = (df_sigma_3["Q_{1}"] - df_sigma3["Q_{1}"])/df_sigma3["Q_{1}"] *100
    y_max = np.max(ratio_sigma0)
    print(y_max)
    print(ratio_sigma1)
    print(ratio_sigma0)
    y1_mean = 0
    y1_std = 0
    # ax.scatter(df_sigma0["Channel"], df_sigma0["Sigma"] , label ="data 1: mean = %.1f, std = %.1f" %(y1_mean, y1_std))  # Plotting the histogram
    # ax.scatter(df_sigma1["Channel"], df_sigma1["Sigma"] , label ="data 1: mean = %.1f, std = %.1f" %(y1_mean, y1_std))  # Plotting the histogram
    # ax.scatter(df_sigma2["Channel"], df_sigma2["Sigma"] , label ="data 1: mean = %.1f, std = %.1f" %(y1_mean, y1_std))  # Plotting the histogram
    # ax.scatter(df_sigma3["Channel"], df_sigma3["Sigma"] , label ="data 1: mean = %.1f, std = %.1f" %(y1_mean, y1_std))  # Plotting the histogram
    # ax.set_xlabel('Channel')
    # ax.set_xlim(0,63)
    # ax.set_ylim(0, 40)
    # ax.set_ylabel("Q$_{1}$", color='k')
    # ax.tick_params(axis='y', labelcolor='k')
    # # Creating a secondary y-axis
    # ax2 = ax.twinx()
    # ax2 = ax2.axes(xlim=[0,63], ylim =[-20,50], xlabel='Channel', ylabel=r'Relative ratio [%]') #r"$\\frac{{\\chi^2}}{{\\text{{NDF}}}}"
    ax2.scatter(df_sigma0["Channel"], ratio_sigma0 , marker = 'o',  label ="left range : $mean - 0 * \sigma$")  # Plotting the histogram
    ax2.scatter(df_sigma1["Channel"], ratio_sigma1 , marker = '^',  label ="left range : $mean - 1 * \sigma$")  # Plotting the histogram
    ax2.scatter(df_sigma2["Channel"], ratio_sigma2 , marker = '.',  label ="left range : $mean - 2 * \sigma$")  # Plotting the histogram
    ax2.scatter(df_sigma_1["Channel"], ratio_sigma_1 , marker = '+',  label ="left range : $mean - (-1) * \sigma$")  # Plotting the histogram
    ax2.scatter(df_sigma_2["Channel"], ratio_sigma_2 , marker = 'v',  label ="left range : $mean - (-2) * \sigma$")  # Plotting the histogram
    ax2.scatter(df_sigma_3["Channel"], ratio_sigma_3 , marker = 'D',  label ="left range : $mean - (-3)* \sigma$")  # Plotting the histogram
    # ax2.fill_between(x=df1["Channel"], y1=y_min, y2=y_max, color='pink',  interpolate=True, alpha=.2)
    # ax2.tick_params(axis='y', labelcolor='darkgreen')
    plt.title("ROB " + str(i))
    ax2.set_xlabel('Channel')
    ax2.set_xlim(0,63)
    ax2.set_ylim(-30, 50)
    # ax2.tick_params(axis='y', labelcolor='darkgreen')
    ax2.set_ylabel('Relative ratio [%]', color='darkgreen')

    # Displaying legends for both plots
    # lines, labels = ax.get_legend_handles_labels()
    # lines2, labels2 = ax2.get_legend_handles_labels()
    # ax2.legend(lines + lines2, labels + labels2, loc='upper right')
    plt.legend(ncol=2, fontsize=12)
    plt.savefig("sigma_check_ROB_"+str(i)+".pdf")
    plt.show()


    