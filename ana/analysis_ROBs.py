import uproot
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

plt.style.use("mystyle.txt")

# for ROB in range(3):

for ROB in range(8):
    filepath1 = "Final_Result_test1/ROB_" + str(ROB) + "_final_result.txt"
    df1 = pd.read_csv(filepath1, sep="\t")
    # print(filepath1)

    filepath3 = "Final_Result_test3/ROB_" + str(ROB) + "_final_result.txt"
    df3 = pd.read_csv(filepath3, sep="\t")
    # print(filepath3)

    filepath5 = "Final_Result_test5/ROB_" + str(ROB) + "_final_result.txt"
    df5 = pd.read_csv(filepath5, sep="\t")
    # print(filepath5)

    filepath6 = "Final_Result_test6/ROB_" + str(ROB) + "_final_result.txt"
    df6 = pd.read_csv(filepath6, sep="\t")
    # print(filepath6)

    filename = "fit_result_ROB_" + str(ROB) + ".root"
    path1  = "../Result_test1/"+ filename
    path3  = "../Result_test3/"+ filename
    path5  = "../Result_test5/"+ filename
    path6  = "../Result_test6/"+ filename
    #Create a PdfPages object to save figures into a PDF file
    ax = plt.axes(xlim=[0,250], ylim =[0.1,100000], yscale="log", xlabel='ADC', ylabel=r'count') #r"$\\frac{{\\chi^2}}{{\\text{{NDF}}}}" 
    for i in range(64):
        with uproot.open(path5) as file:
                # print(df5.iloc[i,7])
                sigma = df5.iloc[i,7]
                if i < 10:
                    hist = "h_charge_ROB0" +str(ROB)+"_ch0"+str(i)+"_sigma_"+str(sigma)
                else:
                    hist = "h_charge_ROB0" +str(ROB)+"_ch"+str(i)+"_sigma_"+str(sigma)
                bin_values5, bin_edges5 = file[hist].to_numpy()
                integral5 = bin_values5.sum()
                # Normalize the histogram
                normalized_bin_contents5 = bin_values5 / integral5 * 100000
                plt.hist(bin_edges5[:-1], bins=bin_edges5, weights=normalized_bin_contents5,histtype ="step",label="data 3-2")  # Plotting histogram using bin edges and values
                # plt.legend() 
    title = "h_charge_ROB0" +str(ROB)      
    print(ROB , title)
    plt.title(title)
    plt.savefig("ROB"+str(ROB)+"_all_chanel.pdf")
    plt.close()
