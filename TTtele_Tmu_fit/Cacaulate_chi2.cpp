#include <iostream>
#include <TFile.h>
#include <TH1.h>
#include <TF1.h>
#include <TCanvas.h>
#include "Mystyle.h"
#include "Bellamy.h"
using namespace std;


double Cacaulatechi2(TString rootfilename, TString histoname, double min_x, double max_x, double *par_fit){
     // Open the ROOT file containing the histogram
    TString filename_LED = rootfilename;
    TString histname = histoname;
    TFile *file = new TFile(filename_LED, "READ");
    vector <double> vec_x;
    vector <double> vec_observed;
    vector <double> vec_expected;
    // Check if the file is opened successfully
    if (!file || file->IsZombie()) {
        std::cerr << "Error: Unable to open file!!!!!!!!!!!!!!!" << std::endl;
        return 0;
    }
    TH1F *histogram = (TH1F*)file->Get(histname);
     // Check if the histogram is retrieved successfully
    if (!histogram) {
        std::cerr << "Error: Unable to retrieve histogram!!!!!!!!!!!!!!!!!" << std::endl;
        file->Close();
        return 0 ;
    }
    //double parameters[8] = {66081,	29.9573,	10.4655,	0.0121268,	8.83317,	0.0409415,	0.0783083,	1.11371}; //05
    //double parameters[8] = {66081,	30.1453,	10.0695,	0.0485093,	9.56545,	0.0403632,	0.0152064,	1.05111};
    double parameters[8] ={par_fit[0], par_fit[1], par_fit[2], par_fit[3], par_fit[4], par_fit[5], par_fit[6], par_fit[7]};
    double * parameter_enum;
    parameter_enum = parameters;
    //for (int i = 1; i <= histogram->GetNbinsX(); ++i) {
    for (int i = 1; i <= histogram->GetNbinsX(); i++) {
    double binContent = histogram->GetBinContent(i); // Get the content of the i-th bin
    double binCenter = histogram->GetBinCenter(i);   // Get the x-value of the bin's center
    double value_expected = Bellamy(&binCenter, parameters);
    //cout << value_expected << endl;
    vec_x.push_back(binCenter);
    vec_observed.push_back(binContent);
    vec_expected.push_back(value_expected);
    //std::cout << "Bin Number: " << i << ", Bin Content: " << binContent << ", Bin X-value: " << binCenter << std::endl;  
    }
    double chi2 =0;
    int bins_num = 0;
    for(int i = 0; i < vec_x.size(); i ++){
        if(i>min_x && i < max_x){
        bins_num ++;
        double residuals = vec_observed[i] - vec_expected[i];
        chi2 += pow(residuals,2)/vec_expected[i];
        }
        
    }
    //int ndf = bins_num - 8;
    //cout << chi2/ndf <<"=================" <<endl;
    return chi2;

}