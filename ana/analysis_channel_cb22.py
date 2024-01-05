import uproot
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

plt.style.use("mystyle.txt")

# for ROB in range(3):
# channellist = [48, 49, 49, 50, 53 ,54 ,55, 56]
for ROB in [15]:
    filepath1 = "Final_Result_test7/ROB_" + str(ROB) + "_final_result.txt"
    df1 = pd.read_csv(filepath1, sep="\t")
    # print(filepath1)

    filepath3 = "Final_Result_test8/ROB_" + str(ROB) + "_final_result.txt"
    df3 = pd.read_csv(filepath3, sep="\t")
    # print(filepath3)



    filename = "fit_result_ROB_" + str(ROB) + ".root"
    path1  = "../Result_test7/"+ filename
    path3  = "../Result_test8/"+ filename

    path4 = "../data/ped_cCB-22_2023-12-18_18_19_hist.root"
    path5 = "../data/ped_cCB-22_2023-12-18_18_20_hist.root"
   
    #Create a PdfPages object to save figures into a PDF file
    pdf_pages = PdfPages('TT_ROB' + str(ROB) +'_waveform.pdf')

    for i in range(64):
        ax = plt.axes(xlim=[0,1250], ylim =[0.1,100000], yscale="log", xlabel='ADC', ylabel=r'count') #r"$\\frac{{\\chi^2}}{{\\text{{NDF}}}}" 
        with uproot.open(path1) as file:
                # print(df1.iloc[i,7])
                sigma = df1.iloc[i,7]
                if i < 10:
                    hist = "h_charge_ROB" +str(ROB)+"_ch0"+str(i)+"_sigma_"+str(sigma)
                else:
                    hist = "h_charge_ROB" +str(ROB)+"_ch"+str(i)+"_sigma_"+str(sigma)
                # histogram = file[hist].to_hist()
                bin_values, bin_edges = file[hist].to_numpy()
                integral = bin_values.sum()
                # Normalize the histogram
                normalized_bin_contents1 = bin_values / integral * 100000
                # plt.hist(bin_edges[:-1], bins=bin_edges, weights=normalized_bin_contents1,histtype ="step", label="data 1")  # Plotting histogram using bin edges and values
                # plt.legend() 
           
        with uproot.open(path3) as file:
                # print(df3.iloc[i,7])
                sigma = df3.iloc[i,7]
                if i < 10:
                    hist = "h_charge_ROB" +str(ROB)+"_ch0"+str(i)+"_sigma_"+str(sigma)
                else:
                    hist = "h_charge_ROB" +str(ROB)+"_ch"+str(i)+"_sigma_"+str(sigma)
                bin_values3, bin_edges3 = file[hist].to_numpy()
                integral3 = bin_values3.sum()
                # Normalize the histogram
                normalized_bin_contents3 = bin_values3 / integral3 * 100000
                # plt.hist(bin_edges3[:-1], bins=bin_edges3, weights=normalized_bin_contents3,histtype ="step",label="data 3-1")  # Plotting histogram using bin edges and values
                # plt.legend() 


        with uproot.open(path4) as file:
                if i < 10:
                    hist = "h_charge_ROB" +str(ROB)+"_ch0"+str(i)
                else:
                    hist = "h_charge_ROB" +str(ROB)+"_ch"+str(i)
                bin_values4, bin_edges4 = file[hist].to_numpy()
                integral4 = bin_values4.sum()
                # Normalize the histogram
                normalized_bin_contents4 = bin_values4 / integral4 * 100000
                # plt.hist(bin_edges3[:-1], bins=bin_edges3, weights=normalized_bin_contents3,histtype ="step",label="data 3-1")  # Plotting histogram using bin edges and values
                # plt.legend() 
        with uproot.open(path5) as file:
                if i < 10:
                    hist = "h_charge_ROB" +str(ROB)+"_ch0"+str(i)
                else:
                    hist = "h_charge_ROB" +str(ROB)+"_ch"+str(i)
                bin_values5, bin_edges5 = file[hist].to_numpy()
                integral5 = bin_values5.sum()
                # Normalize the histogram
                normalized_bin_contents5 = bin_values5 / integral5 * 100000
                # plt.hist(bin_edges3[:-1], bins=bin_edges3, weights=normalized_bin_contents3,histtype ="step",label="data 3-1")  # Plotting histogram using bin edges and values
                # plt.legend() 
       
        plt.hist(bin_edges[:-1], bins=bin_edges,linewidth=2,  weights=normalized_bin_contents1,histtype ="step", label="mode: LED ADC")  # Plotting histogram using bin edges and values
        plt.hist(bin_edges5[:-1], bins=bin_edges5, linewidth=2, weights=normalized_bin_contents5,histtype ="step",label="mode PED ADC")  # Plotting histogram using bin edges and values
        
        plt.hist(bin_edges3[:-1], bins=bin_edges3, linewidth=2, weights=normalized_bin_contents3,histtype ="step",label="mode LED wiki")  # Plotting histogram using bin edges and values
        plt.hist(bin_edges4[:-1], bins=bin_edges,linewidth=2,  weights=normalized_bin_contents4,histtype ="step", label="mode: PED wiki")  # Plotting histogram using bin edges and values
       
        plt.legend() 
        # title = "h_charge_ROB0" +str(ROB)+"_ch0"+str(i)        
        
        histname = hist
        print(ROB , histname)
        plt.title(histname)
        pdf_pages.savefig()  # Save each figure to the PDF file
        plt.close()
    pdf_pages.close()
