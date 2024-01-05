#include <iostream>
#include <TFile.h>
#include <TH1.h>
#include <TF1.h>
#include <TCanvas.h>
#include "Mystyle.h"
#include "Bellamy.h"
using namespace std;

double FitHistogramAfterTMinuit(TString rootfilename, TString histoname, double *par, double fitmin, double fitmax) {

    TFile *file = new TFile(rootfilename);

    if (!file || file->IsZombie()) {
        std::cerr << "Error: Unable to open file " << std::endl;
        return 0;
    }

    // Get the histogram from the ROOT file
    TH1F *histogram = (TH1F*)file->Get(histoname);
    if (!histogram) {
        std::cerr << "Error: Unable to retrieve histogram " << " from file" << std::endl;
        file->Close();
        return 0;
    }

    // Create a Gaussian fit function
    TF1 *fitf = new TF1("fitf", Bellamy, fitmin, fitmax, 8);
    fitf->SetRange(fitmin, fitmax);
    fitf->SetParameters(par[0], par[1], par[2], par[3], par[4], par[5], par[6],par[7]);
    //4.perform the fitting
    fitf->SetNpx(500);
    histogram->Fit("fitf", "R");
    //Get initial chi2, NDF
    double chi2ndf = fitf->GetChisquare() / fitf->GetNDF();
    
    return chi2ndf;
}