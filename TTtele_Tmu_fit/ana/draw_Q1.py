import uproot
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from scipy.optimize import curve_fit
plt.style.use("mystyle.txt")



# Define the double Gaussian function
def gaussian(x, a1, b1, c1):
    return a1 * np.exp(-(x - b1)**2 / (2 * c1**2))





df = pd.read_csv("../fit_result_ROB_2_1.txt", sep="\t",engine="python")
print(df)
# print(df["Q_{1}"])
# Find maximum and minimum y-values
y_max = np.max(df["Q_{1}"])
y_min = np.min(df["Q_{1}"])
y_mean = np.mean(df["Q_{1}"])
y_std = np.std(df["Q_{1}"])

ax = plt.axes(xlim=[0,63], ylim =[0,40], xlabel='Channel', ylabel=r'Q$_{1}$') #r"$\\frac{{\\chi^2}}{{\\text{{NDF}}}}"
ax.scatter(df["Channel"], df["Q_{1}"] , marker = 'o', c="darkgreen", label ="Q$_{1}$")  # Plotting the histogram
# Fill between the max and min y-values
# plt.fill_between(df["Channel"], y_min, y_max, color='red', alpha=0.1)
# Fill in area under the curve and the horizontal lines
ax.fill_between(x=df["Channel"], y1=y_min, y2=y_max, color='pink',  interpolate=True, alpha=.2)
plt.text(0.4, 0.7, 'mean = %.2f' %(y_mean),  color='red', transform=plt.gca().transAxes)
plt.text(0.4, 0.6, 'max = %.2f' %(y_max),  color='C0', transform=plt.gca().transAxes)
plt.text(0.4, 0.5, 'min = %.2f' %(y_min),  color='C0', transform=plt.gca().transAxes)
plt.axhline(y=y_min, color='C0', linestyle='--')  # Horizontal line at y_min
plt.axhline(y=y_mean, color='red', linestyle='--')  # Horizontal line at y_max
plt.axhline(y=y_max, color='C0', linestyle='--')  # Horizontal line at y_max
#plt.axvline(x=2, color='green', linestyle='-.', linewidth=2)  # Vertical line at x=2
plt.title("ROB 2")
plt.legend()
plt.savefig("ROB2_2D.pdf")
plt.show()

xrange = (0,50)
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
expected_data = gaussian(bin_centers, 3.74426499, 12.02203955,  0.49898672)  # Replace bin_centers with your bin centers


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

ax = plt.axes(xlim=[4,20], ylim=[0,10], xlabel=r'Q$_{1}$', ylabel='# of events [/0.1]') #r"$\\frac{{\\chi^2}}{{\\text{{NDF}}}}"
plt.hist(df["Q_{1}"], range=xrange, bins=bins,label ="Q$_{1}$: mean = %.2f, std = %.2f" %(y_mean, y_std))
plt.plot(bin_centers, gaussian(bin_centers, *popt), 'r-', linewidth = 2,  label=r"fit : $\mu$ = %.2f, $\sigma$ = %.2f" %(popt[1], popt[2]))  # Plotting the fitted curve

# Add text at a relative position (using relative coordinates)
#plt.text(0.6, 0.6, 'Relative Text', fontsize=12, color='blue', transform=plt.gca().transAxes)

plt.title("ROB 2")
plt.legend()
plt.savefig("ROB2_1D.pdf")
plt.show()

