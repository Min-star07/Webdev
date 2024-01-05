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
