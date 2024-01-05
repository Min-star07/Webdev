import uproot
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from scipy.optimize import curve_fit

plt.style.use("mystyle.txt")

ROB = 7


# Define the double Gaussian function
def gaussian(x, a1, b1, c1):
    return a1 * np.exp(-((x - b1) ** 2) / (2 * c1**2))


list_path = [
    "Final_Result_test1/ROB_" + str(ROB) + "_final_result.txt",
    "Final_Result_test3/ROB_" + str(ROB) + "_final_result.txt",
    "Final_Result_test5/ROB_" + str(ROB) + "_final_result.txt",
    "Final_Result_test6/ROB_" + str(ROB) + "_final_result.txt",
]
dataset = ["data1", "data3-1", "data3-2", "data3-3"]
ax = plt.axes(
    xlim=[4, 40], ylim=[0, 12], xlabel=r"Q$_{1}$", ylabel="# of events [/0.1]"
)  # r"$\\frac{{\\chi^2}}{{\\text{{NDF}}}}"
for i, ipath in enumerate(list_path):
    print(ipath)
    df = pd.read_csv(ipath, sep="\t", engine="python")
    # Find maximum and minimum y-values
    y_max = np.max(df["Q_{1}"])
    y_min = np.min(df["Q_{1}"])
    y_mean = np.mean(df["Q_{1}"])
    y_std = np.std(df["Q_{1}"])

    ##################################################################################################################################################
    xrange = (0, 50)
    bins = 500
    # Create a histogram from the data
    hist, bin_edges = np.histogram(df["Q_{1}"], range=xrange, bins=bins, density=False)
    print(hist)
    print(bin_edges)

    # Get the bin centers
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    # Fit the histogram data to the double Gaussian function
    popt, pcov = curve_fit(gaussian, bin_centers, hist, p0=[40, 12, 4])
    print("Fitted parameters:", popt)
    # Get observed data (bin contents) from the histogram
    observed_data = hist  # Replace this with your actual histogram data
    # Calculate expected values using the fitted model
    expected_data = gaussian(
        bin_centers, 3.74426499, 12.02203955, 0.49898672
    )  # Replace bin_centers with your bin centers

    # Calculate chi-squared
    residuals = observed_data - expected_data
    chi_squared = np.sum(residuals**2)

    # Calculate degrees of freedom
    num_params = 3
    num_bins = len(observed_data)
    ndf = num_bins - num_params

    # Calculate chi-squared per degree of freedom
    chi_squared_ndf = chi_squared / ndf

    print(f"Chi-squared: {chi_squared}")
    print(f"Degrees of freedom: {ndf}")
    print(f"Chi-squared per degree of freedom: {chi_squared_ndf}")

    plt.hist(
        df["Q_{1}"],
        range=xrange,
        bins=bins,
        label="Q$_{1}$: mean = %.1f, std = %.1f" % (y_mean, y_std),
    )
    plt.plot(
        bin_centers,
        gaussian(bin_centers, *popt),
        "r-",
        linewidth=2,
        label=r"fit : $\mu$ = %.1f, $\sigma$ = %.1f" % (popt[1], popt[2]),
    )  # Plotting the fitted curve

    # Add text at a relative position (using relative coordinates)
    # plt.text(0.6, 0.6, 'Relative Text', fontsize=12, color='blue', transform=plt.gca().transAxes)

plt.title("ROB " + str(ROB))
plt.legend()
plt.savefig("ROB_" + str(ROB) + "_Q1_sum.pdf")
plt.show()
ax = plt.axes(
    xlim=[0, 63], ylim=[-40, 40], xlabel=r"channel", ylabel="Ratio [%]"
)  # r"$\\frac{{\\chi^2}}{{\\text{{NDF}}}}"

for i, ipath in enumerate(list_path):
    print(i, ipath)
    df = pd.read_csv(ipath, sep="\t", engine="python")
    # Find maximum and minimum y-values
    y_max = np.max(df["Q_{1}"])
    y_min = np.min(df["Q_{1}"])
    y_mean = np.mean(df["Q_{1}"])
    y_std = np.std(df["Q_{1}"])
    ##################################################################################################################################################
    if i == 0:
        df1 = df["Q_{1}"]
    elif i == 1:
        df3 = df["Q_{1}"]
    elif i == 2:
        df5 = df["Q_{1}"]
    else:
        df6 = df["Q_{1}"]

ratio1 = (df1 - df3) / df3 * 100
ratio5 = (df5 - df3) / df3 * 100
ratio6 = (df6 - df3) / df3 * 100

ax.scatter(df["Channel"], ratio1, color="darkgreen", marker="o", label="data 1")
ax.scatter(df["Channel"], ratio5, color="red", marker="*", label="data 3-2")
ax.scatter(df["Channel"], ratio6, color="blue", marker="v", label="data 3-3")

plt.title("ROB " + str(ROB))
plt.legend()
plt.savefig("Result/ROB_" + str(ROB) + "_Q1_relativevsChannel1.pdf")
plt.show()

ax = plt.axes(
    xlim=[0, 63], ylim=[0, 40], xlabel=r"channel", ylabel="Q$_{1}$"
)  # r"$\\frac{{\\chi^2}}{{\\text{{NDF}}}}"

for i, ipath in enumerate(list_path):
    print(i, ipath)
    df = pd.read_csv(ipath, sep="\t", engine="python")
    # Find maximum and minimum y-values
    y_max = np.max(df["Q_{1}"])
    y_min = np.min(df["Q_{1}"])
    y_mean = np.mean(df["Q_{1}"])
    y_std = np.std(df["Q_{1}"])
    ##################################################################################################################################################
    if i == 0:
        df1 = df["Q_{1}"]
    elif i == 1:
        df3 = df["Q_{1}"]
    elif i == 2:
        df5 = df["Q_{1}"]
    else:
        df6 = df["Q_{1}"]

ratio1 = (df1 - df3) / df3 * 100
ratio5 = (df5 - df3) / df3 * 100
ratio6 = (df6 - df3) / df3 * 100

ax.scatter(df["Channel"], df1, marker="o", label="data 1")
ax.scatter(df["Channel"], df3, marker="*", label="data 3-1")
ax.scatter(df["Channel"], df5, marker="v", label="data 3-2")
ax.scatter(df["Channel"], df5, marker="^", label="data 3-3")

plt.title("ROB " + str(ROB))
plt.legend()
plt.savefig("Result/ROB_" + str(ROB) + "_Q1vsChannel1.pdf")
plt.show()
