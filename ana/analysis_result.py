import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import seaborn as sns
plt.style.use("mystyle.txt")
with open("Final_Result_test6/check_channel_result.txt", "w") as f:
    for i in range(8):
        list_channel = []
        filename = "Final_Result_test6/ROB_" + str(i) + "_final_result.txt"
        print(filename)
        df = pd.read_csv(filename, sep="\t")
        print(df["flag_chi2"])
        count_channel = (df["flag_chi2"] == 1).sum()
        list_channel = df[df["flag_chi2"] == 1]["Channel"].tolist()
        print(f"=====================This is ROB {i}=====================================", file=f)
        print(f"{count_channel}", file=f)
        print(f"{list_channel}", file=f)