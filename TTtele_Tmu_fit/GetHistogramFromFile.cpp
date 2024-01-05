#include <iostream>
#include <fstream>
#include <string>
#include <TFile.h>
#include <TH1.h>
#include <TF1.h>
#include <TCanvas.h>
#include <TFitResult.h>
#include <TLatex.h>
#include <TStyle.h>
#include <TMinuit.h>
#include "TGraph.h"
#include <fstream> // Required for file operations
#include "Mystyle.h"
#include "Bellamy.h"
#include "FitHistogramWithGaussian.h"
#include "Cacaulate_chi2.h"
#include "FitHistogramAfterTMinuit.h"
using namespace std;

TString filename_LED ;
TString filename_PED ;
double fitMin; //style buquzhengshu - 1
double fitMax ;
TString histname;
// Open a file for writing
ofstream outfile;
double par_final[10];

    
void fcn(int &npar, double *gin, double &result, double * par, int flag);

// void GetHistogramFromFile() {
int main(int argc, char** argv){
    //set initial parmeters
    string led_rootfile = "led_cCB-19_2023-11-10_10_50_hist.root";
    string ped_rootfile = "ped_cCB-19_2023-11-10_10_49_hist.root";
    string rob_id = "2";
    string channel_id = "0";
    string fitmax = "100";
    for(int i = 0; i < argc; i ++){
        if(strcmp(argv[i], "-led") == 0){
            led_rootfile = argv[i+1];
        }
        if(strcmp(argv[i], "-ped") == 0){
            ped_rootfile = argv[i+1];
        }
        if(strcmp(argv[i], "-ROB") == 0){
            rob_id = argv[i+1];
        }
        if(strcmp(argv[i], "-channel") == 0){
            channel_id = argv[i+1];
        }
        if(strcmp(argv[i], "-max") == 0){
            fitmax = argv[i+1];
        }
    }
    
    //define canvas style
    SetMystyle();
    gStyle->SetOptFit(1111); 
    // Open the ROOT file containing the histogram
    filename_LED = led_rootfile;
    filename_PED = ped_rootfile;
    
    TString ROB_id = rob_id;
    int Channel_id = atoi(channel_id.c_str());
    double fit_Max_defaut = atoi(fitmax.c_str());

    TFile *file = new TFile(filename_LED, "READ");

    // Check if the file is opened successfully
    if (!file || file->IsZombie()) {
        std::cerr << "Error: Unable to open file!" << std::endl;
        return 0;
    }

  
    // Check if the file is opened successfully
    TString outfilename = "fit_result_ROB_" + ROB_id + ".txt";
    outfile.open(outfilename);
    if (!outfile.is_open()) {
        std::cerr << "Error opening the file!" << std::endl;
        return 0;
    }
    outfile << "channel"<< "\t"<< "Min_x"<< "\t" << "Max_x" << "\t" << "N0" << "\t" << "Q_{0}" << "\t" << "Q_{1}" << "\t" << "#sigma_{0}"<< "\t" <<"#sigma_{1}" << "\t" <<"w" << "\t" << "#alpha"<< "\t" << "#mu" << endl;
    TCanvas *canvas = new TCanvas("canvas", "Histogram Canvas", 800, 600);
    TString canvasname = "fit_graph_ROB_"+ ROB_id + ".pdf";
    canvas->cd();
    for(int id = 0;id < 1; id ++){
    // Get the histogram from the file
    Channel_id = id;
    if (id < 10)
        histname = "h_charge_ROB0" + ROB_id + "_ch0" + Channel_id;
    else
        histname = "h_charge_ROB0" + ROB_id + "_ch" + Channel_id;
    cout << histname << endl;
    TH1F *histogram = (TH1F*)file->Get(histname);
    histogram->GetXaxis()->SetRangeUser(0, 200);
    histogram->GetXaxis()->CenterTitle();
    histogram->GetYaxis()->CenterTitle();
    // Check if the histogram is retrieved successfully
    if (!histogram) {
        std::cerr << "Error: Unable to retrieve histogram!!!!!!!!!!!!!!!!!!!!!" << std::endl;
        file->Close();
        return 0 ;
    }
    //prepare the dataset for fitting
     
    //2.define the fit initial parameters
    //2.1 get the initial of parameters of pedestral
    double * ped_gauss;
    ped_gauss = FitHistogramWithGaussian(filename_PED, histname);
    //cout << ped_gauss[0] << "========"<< ped_gauss[1]<< endl;
    //3.set the initial parameters
    //3.1 prepare the math model  (function with parameters)
    fitMin = ped_gauss[0] - 3 * ped_gauss[1];  
    fitMax = fit_Max_defaut;
        //TMinuit Fitting
        //1. define a TMinuit with the number of parameters
        TMinuit *minuit = new TMinuit(8);
        //2. initialize parameter fitf->SetParNames("N0","Q_{0}","Q_{1}", "#sigma_{0}","#sigma_{1}", "w","#alpha", "#mu");
        minuit->DefineParameter(0, "N0",             66000,        1000,   60000,          75000);
        minuit->DefineParameter(1, "Q_{0}",          ped_gauss[0], 0.2,    ped_gauss[0]-3, ped_gauss[0]+3);
        minuit->DefineParameter(2, "Q_{1}",          14,           0.2,    5,              20);
        minuit->DefineParameter(3, "#sigma_{0}",     ped_gauss[1], 0.02,    0.02,            1);
        minuit->DefineParameter(4, "#sigma_{1}",     10,           4,      2,              16);
        minuit->DefineParameter(5, "w",              0.1,         0.01,   0.01,           0.2);
        minuit->DefineParameter(6, "#alpha",         0.4,          0.05,   0.1,            0.8);
        minuit->DefineParameter(7, "#mu",            1.5,            0.5,    0.5,            3);

        //3. define FCN
        minuit->SetFCN(fcn);

        //4.perform the fitting
        minuit->Migrad();

        // Retrieve fit status
        int status = minuit->GetStatus(); // Get the fit status

        
        //5. retrive fitting result
        double par_fit[8];
        double paraerror[8];
        minuit->GetParameter(0, par_fit[0], paraerror[0]);
        minuit->GetParameter(1, par_fit[1], paraerror[1]);
        minuit->GetParameter(2, par_fit[2], paraerror[2]);
        minuit->GetParameter(3, par_fit[3], paraerror[3]);
        minuit->GetParameter(4, par_fit[4], paraerror[4]);
        minuit->GetParameter(5, par_fit[5], paraerror[5]);
        minuit->GetParameter(6, par_fit[6], paraerror[6]);
        minuit->GetParameter(7, par_fit[7], paraerror[7]);
        

        gPad->SetLogy(); // Sets logarithmic scale for the current pad
        
        canvas->Print(canvasname + "[");
        histogram->Draw();
        // double bin = (fitMax - fitMin)/1000;
        // double *data_x;
        // double *data_y;
        // double x =0;
        // for (int i = 0; i < 1000; i ++){
        //      x = i * bin + fitMin;
        //      data_x[i] = x;
        //      double  value = Bellamy(&x, par_fit);
        //      data_y[i] = value;
        // }
        // TGraph *graph = new TGraph(1000, data_x, data_y); 
        // graph->Draw("same");

        //cout << "fit result : " << par_fit[0] << "\t" << par_fit[1] << "\t" << par_fit[2] << "\t" << par_fit[3] << "\t" << par_fit[4] << "\t" << par_fit[5] << "\t" << par_fit[6] << "\t" << par_fit[7]  <<endl;
        
        // Display the fit status
        // if (status == 0) {
        //     std::cout << "MIGRAD converged successfully." << std::endl;
        //  } else {
        // std::cout << "MIGRAD did not converge." << std::endl;
        // }
           

            // Retrieve chi-square and NDF
            // double fmin = 0.0, fedm = 0.0, errdef;
            // int npari, nparx, isstat;
          
            // minuit->mnstat(fmin, fedm, errdef, npari, nparx, isstat);
            //cout << fmin << "\t" << fedm << "\t" << npari << "\t" <<endl;
            // Calculate and display chi-square per degree of freedom
            // double chiSquareNdf = fmin/npari;
            // std::cout << "Chi-square per degree of freedom: " << chiSquareNdf << std::endl;

            // Delete TMinuit instance
            delete minuit;
    
    }
    canvas->Print(canvasname + "]");   
    file->Close();
    outfile.close();
    return 0;
}

//fcn
void fcn(int &npar, double *gin, double &result, double * par, int flag){
   // cout << par[0] << "\t" << par[1] << "\t" << par[2] << "\t" << par[3] << "\t" << par[4] << "\t" << par[5] << "\t" << par[6] << "\t" << par[7] << endl;
   result = Cacaulatechi2(filename_LED, histname, fitMin, fitMax, par);  
}
  