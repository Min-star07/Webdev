import uproot
import pandas as pd

events1 = uproot.open("../DB_fit_MT.root:TB_lin_par")
print(events1.keys())
print(events1.show())
data1 = events1.arrays(
    ["FEB_ID", "cat_ID", "CH", "a0", "a00", "a1", "a2", "a3", "a4", "a5", "b", "ChiSq"],
    library="pd",
)  # library="np", library="pd"

print(data1)
data1.to_csv("cailibration1.txt", sep="\t")


# events2 = uproot.open("../test_b2.root:TB_lin_par")
# print(events2.keys())
# print(events2.show())
# data2 = events2.arrays(
#     ["FEB_ID", "cat_ID", "CH", "a0", "a00", "a1", "a2", "a3", "a4", "a5", "b", "ChiSq"],
#     library="pd",
# )  # library="np", library="pd"
# data2 = data2[data2["FEB_ID"] != 9]
# print(data2)
# data2.to_csv("cailibration_tt.txt", index=False, sep="\t")

# data = pd.concat([data1,data2])
# data.to_csv("calibration.txt",index=False, sep="\t")
# print(data)
