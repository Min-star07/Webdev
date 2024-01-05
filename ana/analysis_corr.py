import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import seaborn as sns


plt.style.use("mystyle.txt")

ROB = 4


def linear(x, k):
    return k * x


df = pd.read_csv(
    "./Final_Result" + "/ROB_" + str(ROB) + "_final_result.txt",
    sep="\t",
    engine="python",
)
print(df)

plt.figure(figsize=(12, 12))
sns.heatmap(
    df.corr(),
    xticklabels=df.corr().columns,
    yticklabels=df.corr().columns,
    cmap="RdBu",
    center=0,
    annot=True,
    annot_kws={"size": 8, "weight": "normal", "color": "#253D24"},
)
plt.title("ROB " + str(ROB))
plt.savefig("./Result" + "/ROB_" + str(ROB) + "_heatmp.pdf")
plt.show()

# ax = plt.axes(xlim=[0,63], ylim =[0,30], xlabel='Channel', ylabel=r'Q$_{1}$') #r"$\\frac{{\\chi^2}}{{\\text{{NDF}}}}"
