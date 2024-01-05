import uproot
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from scipy.optimize import curve_fit

plt.style.use("mystyle.txt")


ROB = 15


# Define the double Gaussian function
def gaussian(x, a1, b1, c1):
    return a1 * np.exp(-((x - b1) ** 2) / (2 * c1**2))


df1 = pd.read_csv(
    "Final_Result_test7_2/ROB_" + str(ROB) + "_final_result.txt",
    sep="\t",
    engine="python",
)
print(df1)

df2 = pd.read_csv(
    "Final_Result_test8/ROB_" + str(ROB) + "_final_result.txt",
    sep="\t",
    engine="python",
)
print(df2)


###############################################################################################################
# Generate sample data for a 8x8 grid (replace this with your data)
list1 = list(df1["Q_{1}"])
list2 = list(df2["Q_{1}"])

# Using list comprehension to divide elements
result = [x / y for x, y in zip(list1, list2)]

# Reshape the list into an 8x8 array
array_8x8 = np.array(result).reshape(8, 8)
data = array_8x8
# Create a 8x8 grid plot with colored cells representing values
plt.figure(figsize=(10, 10))
plt.imshow(data, cmap="viridis", interpolation="nearest")
# Add text annotations for each cell
for i in range(8):
    for j in range(8):
        plt.text(j, i, f"{data[i, j]:.1f}", ha="center", va="center", color="white")

# Set colorbar to represent values
plt.colorbar(label=r"Q$_{1}$ value")

# Set labels and title
plt.xlabel("Channel")
plt.ylabel("Channel")
plt.title(r"ROB_" + str(ROB) + "_Q$_{1}$_distribution_Ratio")
plt.savefig("Result/ROB_" + str(ROB) + "_Q1_ratio.pdf")
plt.show()


##################################################################################################################################################
y_mean = np.mean(result)
y_std = np.std(result)
xrange = (0, 40)
bins = 80
# Create a histogram from the data
hist, bin_edges = np.histogram(result, range=xrange, bins=bins, density=False)
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

ax = plt.axes(
    xlim=[0, 30],
    ylim=[0, 15],
    xlabel=r"FADC / Wilkinson ADC ",
    ylabel="# of events [/0.5]",
)  # r"$\\frac{{\\chi^2}}{{\\text{{NDF}}}}"
plt.hist(
    result,
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
plt.savefig("Result/ROB_" + str(ROB) + "_Q1_mean_ratio.pdf")
plt.show()
