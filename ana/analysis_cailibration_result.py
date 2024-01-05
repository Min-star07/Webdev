import uproot
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from scipy.optimize import curve_fit
plt.style.use("mystyle.txt")

# with uproot.open("../test_b2.root") as file:
#     print(file.keys())

events = uproot.open("../DB_fit_MT.root:TB_lin_par") 
print(events.keys())
print(events.values())
print(events.show())
print(events["CH"].array()) 
FEB = events.arrays(["FEB_ID", "CH" , "a1"], library="pd", )#library="np", library="pd"

FEB_list = [9, 4003, 4004, 5002, 5003, 5007, 5009, 5011]
ax = plt.axes(xlim=[0,63], ylim =[20,120], xlabel='Channel', ylabel=r'a1 (slope)') #r"$\\frac{{\\chi^2}}{{\\text{{NDF}}}}"

events2 = uproot.open("../test_b2.root:TB_lin_par") 
print(events2)
FEB_9 = events2.arrays(["FEB_ID", "CH" , "a1"], library="pd", )#library="np", library="pd"
FEB_data1 = FEB_9[FEB_9["FEB_ID"] == 9]
FEB_data1 = FEB_data1.reset_index(drop=True)
# print(FEB_data1)
for i,ifeb in enumerate(FEB_list):
    if ifeb == 9:
        ax.scatter(FEB_data1["CH"], FEB_data1["a1"], label ="FEB : %d" %(ifeb))  # Plotting the histogram
    else:
        FEB_data = FEB[FEB["FEB_ID"] == ifeb]
        # FEB_9.reset_index(inplace=True)
        FEB_data = FEB_data.reset_index(drop=True )
        # print(FEB_data)
        ax.scatter(FEB_data["CH"], FEB_data["a1"], label ="FEB : %d" %(ifeb))  # Plotting the histogram

    # plt.title("ROB "+ str(ROB))
plt.legend(ncol=3,fontsize=12)
plt.savefig("FEB_slope_compare.pdf")
plt.show()


xrange = (0,50)
bins = 500
ax = plt.axes(xlim=[20,100], ylim=[0,10], xlabel=r'slope', ylabel='# of events [/0.1]') #r"$\\frac{{\\chi^2}}{{\\text{{NDF}}}}"
for i,ifeb in enumerate(FEB_list):
    if ifeb == 9:
        ax.hist(FEB_data1["a1"], range=xrange, bins=bins)
    else:
        FEB_data = FEB[FEB["FEB_ID"] == ifeb]
        # FEB_9.reset_index(inplace=True)
        FEB_data = FEB_data.reset_index(drop=True)
        print(FEB_data)
        ax.hist(FEB_data["a1"], range=xrange, bins=bins) #,label ="Q$_{1}$: mean = %.1f, std = %.1f" %(y_mean, y_std)
        # plt.title("ROB "+ str(ROB))
# plt.legend(ncol=3,fontsize=12)
plt.savefig("FEB_slope_hist.pdf")
plt.show()