import ROOT

# Open the ROOT file
file = ROOT.TFile.Open("../ROB2/fit_result_ROB_2.root")
if not file or file.IsZombie():
    print("Error: File not found or corrupted.")
    exit()

# Get the histogram from the file
histogram = file.Get("h_charge_ROB02_ch62_sigma_2")
if not histogram:
    print("Error: Histogram not found in the file.")
    exit()

# Get the function from the file
# fit_function = file.Get("Bellamy")
# if not fit_function:
#     print("Error: Fit function not found in the file.")
#     exit()

# Create a canvas to draw the histogram and function
canvas = ROOT.TCanvas("canvas", "Histogram and Fit", 800, 600)

# Draw the histogram
histogram.Draw()

# Draw the fit function on top of the histogram
# fit_function.Draw("same")

# Show the canvas
canvas.SaveAs("test.pdf")
