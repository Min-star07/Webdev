#include <iostream>
#include <fstream>
#include <string>
#include <TFile.h>
#include <TH1.h>
#include <TF1.h>
#include <TCanvas.h>
#include <TFitResult.h>
#include <TStopwatch.h>
#include <TLatex.h>
#include <TStyle.h>
#include <iomanip>
#include <fstream> // Required for file operations
#include "Mystyle.h"
#include "Bellamy.h"
#include "FitHistogramWithGaussian.h"
#include "GetXmax_hist.h"
#include "ChiSquare.h"
#include "Checkpath.h"
using namespace std;


int main(int argc, char** argv){
    //set initial parmeters
    string led_rootfile = "../TTtele/data/led_cCB-19_2023-11-10_10_50_hist.root";
    string ped_rootfile = "../TTtele/data/ped_cCB-19_2023-11-10_10_49_hist.root";
    string rob_id = "1";
    string channel_start = "0";
    string channel_end = "64";
    string sigma = "3";
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
        if(strcmp(argv[i], "-channel_start") == 0){
            channel_start = argv[i+1];
        }
        if(strcmp(argv[i], "-channel_end") == 0){
            channel_end = argv[i+1];
        }
        // if(strcmp(argv[i], "-sigma") == 0){
        //     sigma = argv[i+1];
        // }
    }
    
    //define canvas style
    SetMystyle();
    
    // Open the ROOT file containing the histogram
    TString filename_LED = led_rootfile;
    TString filename_PED = ped_rootfile;
    
    TString ROB_id = rob_id;
    int Chanel_start = atoi(channel_start.c_str());
    int Chanel_end = atoi(channel_end.c_str());
    // int Sigma = atoi(sigma.c_str());
    int Sigma = -5;

    TFile *infile = new TFile(filename_LED, "READ");

    // Check if the file is opened successfully
    if (!infile || infile->IsZombie()) {
        std::cerr << "Error: Unable to open file!" << std::endl;
        return 0;
    }
    string pathDir = "./Result";
    //handlePath(pathDir);
    TString outrootfilename =  pathDir + "/fit_result_ROB_" + ROB_id + ".root";
    TFile *outfile_root = new TFile(outrootfilename, "RECREATE");
    // Open a file for writing
    ofstream outfile_txt;
    TString outfilename = pathDir   + "/fit_result_ROB_" + ROB_id  + ".txt"; 

     // Check if the file exists
    std::ifstream outfileexist(outfilename);
    if (outfileexist.good()) {
        outfileexist.close(); // Close the file if it exists

        // Delete the file
        if (std::remove(outfilename.Data()) != 0) {
            std::cerr << "Error deleting file!" << std::endl;
            return 1;
        } else {
            std::cout << "File deleted successfully!" << std::endl;
        }
    } else {
        std::cout << "File does not exist." << std::endl;
    }
    outfile_txt.open(outfilename, ios::app);


    // Check if the file is opened successfully
    if (!outfile_txt.is_open()) {
        std::cerr << "Error opening the file!" << std::endl;
        return 0;
    }
    outfile_txt << "ROB" << "\t" << "Channel" << "\t" << "flag_fit_method" << "\t" << "flag_chi2" <<"\t" << "Chi2NDF"<< "\t"<<"ped_mean"<<"\t" << "ped_sigma"<<"\t"<< "Sigma" << "\t" << "Min_x"<< "\t" << "Max_x" << "\t" << "N0" << "\t" << "Q_{0}" << "\t" << "Q_{1}" << "\t" << "#sigma_{0}"<< "\t" <<"#sigma_{1}" << "\t" <<"w" << "\t" << "#alpha"<< "\t" << "#mu" << endl;
    
    while(Sigma < 4){
    for(int id = Chanel_start;id < Chanel_end; id ++){
    //for(int id = 7;id < 8; id ++){
    // Get the histogram from the file
    TString histname;
    if (ROB_id <10){
        if (id < 10)
        histname = "h_charge_ROB0" + ROB_id + "_ch0" + id;
        else
        histname = "h_charge_ROB0" + ROB_id + "_ch" + id;
    }
    else{
        if (id < 10)
        histname = "h_charge_ROB" + ROB_id + "_ch0" + id;
        else
        histname = "h_charge_ROB" + ROB_id + "_ch" + id;
    }
    
    cout << histname << endl;
    TH1F *histogram = (TH1F*)infile->Get(histname);
    TH1F *histogram1 = (TH1F*)infile->Get(histname);
    // histogram->GetXaxis()->SetRangeUser(0, 250);
    histogram->GetXaxis()->SetRangeUser(0, 1500);
    histogram->GetXaxis()->CenterTitle();
    histogram->GetYaxis()->CenterTitle();
    cout << "=====================" << endl;
    // Check if the histogram is retrieved successfully
    if (!histogram) {
        std::cerr << "Error: Unable to retrieve histogram!" << std::endl;
        infile->Close();
        return 0 ;
    }
    //prepare the dataset for fitting

    //2.define the fit initial parameters
    //2.1 get the initial of parameters of pedestral
    double * ped_gauss;
    ped_gauss = FitHistogramWithGaussian(filename_PED, histname);
    cout << ped_gauss[0] << "========"<< ped_gauss[1]<< endl;
    //2.2 set the fit range
    // double fitMin = ped_gauss[0]- Sigma * 2; //fit left range: mu - 3 * sigma
    double fitMin = ped_gauss[0]- Sigma * ped_gauss[1]; //fit left range: mu - 3 * sigma
    double fitMax = Getxmax(histogram);
    // double fitMax = 200;
    //3.fit use atleastsquare and likelihood and select min chi2/ndf method as final result
    double chi2ndf_chi2, chi2ndf_likelihood;
    double *para_chi2, *para_likelihood; 
    int flag_fit_method=0, flag_chi2=0;
    TF1 *func[2];
    for(int i = 0; i < 2; i++) { //0: least square 1:likelihood
        func[i] = new TF1(Form("func%d", i), Bellamy, fitMin, fitMax, 8);
        int entries_number = histogram->Integral();
        // func[i]->SetParameters(55000, ped_gauss[0], 12, ped_gauss[1], 10, 0.1, 0.2, 1.0);
        double mu_init = 0.007 * fitMax;
        func[i]->SetParameters(entries_number, ped_gauss[0], 11, ped_gauss[1], 10, 0.1, 0.2, 0.5);
        // func[i]->SetParameters(entries_number, 20, 12, 1, 10, 0.1, 0.2, 0.5);
        func[i]->SetParNames("N_{0}","Q_{0}","Q_{1}", "#sigma_{0}","#sigma_{1}", "w","#alpha", "#mu");
        // func[i]->FixParameter(0, histogram->Integral());
        func[i]->SetRange(fitMin, fitMax);
        func[i]->SetNpx(500);
        if(i % 2 == 0){
            histogram->Fit(func[0], "R");
            func[0]->SetLineColor(4);
            chi2ndf_chi2 = func[0]->GetChisquare() / func[0]->GetNDF();
            }
        else{
            histogram1->Fit(func[1], "RL");
            func[1]->SetLineColor(2);
            chi2ndf_likelihood = func[1]->GetChisquare() / func[1]->GetNDF();
            }
    }
    // TCanvas *canvas1 = new TCanvas("canvas1", "Histogram Canvas", 800, 600);
    // canvas1->cd();
    // gPad->SetLogy(); // Sets logarithmic scale for the current pad
    TString histname_new = histname + "_sigma_" + Sigma;
    if(chi2ndf_chi2 < chi2ndf_likelihood){        
            func[0]->SetRange(fitMin, fitMax);
            histogram->Fit(func[0], "R");
            outfile_root->cd();
            //Rename the histogram
            histogram->SetName(histname_new)  ;
            histogram->Write();
            chi2ndf_chi2 = func[0]->GetChisquare() / func[0]->GetNDF();
            // canvas1->SaveAs(Form("./ROB"+ ROB_id + "/charge_rob" + ROB_id + "_channel_%d" + "_sigma_" + Sigma+ ".pdf", id));
            flag_fit_method = 1;
            //save data
              if(chi2ndf_chi2 > 3){
              flag_chi2 = 1;
           }
        
        para_chi2 = func[0]->GetParameters();
        //CalculateChiSquare(histogram, fitMin, fitMax, para_chi2);
        outfile_txt << ROB_id << "\t" << id << "\t" << flag_fit_method << "\t" << flag_chi2 << "\t" << setprecision(5)<< chi2ndf_chi2 << "\t"<<ped_gauss[0] << "\t" << ped_gauss[1] << "\t" <<Sigma << "\t" << fitMin << "\t" << fitMax ;
        for(int i = 0; i < 8; i++){
        outfile_txt << "\t" << para_chi2[i];
        }
        }
    else{
        func[1]->SetRange(fitMin, fitMax);
        flag_fit_method = 2;
        histogram1->Fit(func[1], "RL");
        outfile_root->cd();
         //Rename the histogram
        histogram1->SetName(histname_new) ; 
        histogram1->Write();
        chi2ndf_likelihood = func[1]->GetChisquare() / func[1]->GetNDF();
        // canvas1->SaveAs(Form("./ROB"+ ROB_id + "/charge_rob" + ROB_id  +"_channel_%d" + "_sigma_" + Sigma + ".pdf", id));
        if(chi2ndf_likelihood > 3){
             flag_chi2 = 1;
           }
        //save data
        para_likelihood = func[1]->GetParameters();
        //CalculateChiSquare(histogram, fitMin, fitMax, para_likelihood);
        outfile_txt << ROB_id << "\t" << id << "\t" << flag_fit_method << "\t" << flag_chi2 << "\t" << setprecision(5)<< chi2ndf_likelihood << "\t"<<ped_gauss[0] << "\t" << ped_gauss[1]<< "\t" <<Sigma<< "\t" << fitMin << "\t" << fitMax ;
        for(int i = 0; i < 8; i++){
        outfile_txt << "\t" << para_likelihood[i];
        }
        }
    outfile_txt << endl;  
   }
   Sigma ++;
}
    outfile_root->Close();
    infile->Close();
    outfile_txt.close();
return 0;
}