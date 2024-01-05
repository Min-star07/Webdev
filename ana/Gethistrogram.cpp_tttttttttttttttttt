#include <iostream>
#include <fstream>
#include <string>
#include <TFile.h>
#include <TTree.h>
#include <TH1.h>
#include <TF1.h>
#include <TCanvas.h>
#include <TFitResult.h>
#include <TStopwatch.h>
#include <TLatex.h>
#include <TStyle.h>
#include <iomanip>
#include "Mystyle.h"
using namespace std;

int *Getsigma(TString inputfilename, TString ROB){
    int  rob[64]={0};
    int  channel[64]={0};
    int  method[64]={0};
    int  chi2[64]={0};
    double chi2ndf[64]={0};
    static int sigma[64]={0};
    double ped_mean[64] ={0};
    double ped_sigma[64]={0};
    double min[64]={0};
    double max[64]={0};
    double n[64]={0.0};
    double q0[64]={0};
    double q1[64]={0};
    double sigma0[64]={0};
    double sigma1[64]={0};
    double w[64]={0};
    double alpha[64]={0};
    double mu[64]={0};
    string A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,R,S;
    TString outfilename =  "./Final_Result/ROB_"+ ROB + "_final_fit_para.root";
    TFile *outfile = new TFile(outfilename, "RECREATE");
    TTree *tree = new TTree("Events", "Event data");
    tree->Branch("ROB", rob, "rob/I");
    tree->Branch("Channel", channel, "Channel/I");
    tree->Branch("Method", method, "method/I");
    tree->Branch("Chi2", chi2, "chi2/I");
    tree->Branch("Chi2ndf", chi2ndf, "chi2ndf/D");
    tree->Branch("ped_mean", ped_mean, "ped_mean/D");
    tree->Branch("ped_sigma", ped_sigma, "ped_sigma/D");
    tree->Branch("Sigma", sigma, "sigma/I");
    tree->Branch("Min", min, "min/D");
    tree->Branch("Max", max, "max/D");
    tree->Branch("N", n, "n/D");
    tree->Branch("Q0", q0, "q0/D");
    tree->Branch("Q1", q1, "q1/D");
    tree->Branch("Sigma0", sigma0, "sigma0/D");
    tree->Branch("Sigma1", sigma1, "sigma1/D");
    tree->Branch("w", w, "w/D");
    tree->Branch("alpha", alpha, "alpha/D");
    tree->Branch("mu", mu, "mu/D");
    ifstream inputfile;
    inputfile.open(inputfilename, ios::in);
    inputfile>>A >>B >>C >> D>> E >>F >>G >>H >>I >>J >>K >>L >>M >> N >> O >>P>>R>>S;
    // cout << A << "\t" << B <<endl;
    int i =0;
    while(i<64){
        inputfile>> rob[i] >> channel[i] >> method[i] >> chi2[i] >> chi2ndf[i] >>ped_mean[i] >>ped_sigma[i]>> sigma[i] >> min[i] >> max[i] >> n[i] >> q0[i] >> q1[i] >> sigma0[i] >> sigma1[i] >> w[i] >> alpha[i] >> mu[i];
        
        cout << rob[i] << "\t"<< channel[i] << "\t"<< method[i] << "\t"<< chi2[i] << "\t"<<  chi2ndf[i] << "\t"<< sigma[i] << "\t"<< min[i] << "\t"<< max[i] << "\t"<< n[i] << "\t"<< q0[i] << "\t"<< q1[i] << "\t"<< sigma0[i] << "\t"<< sigma1[i] << "\t"<< w[i] << "\t"<< alpha[i] << "\t"<< mu[i]<< endl;
  
        i++;
        //cout << i << endl;
    }
    inputfile.close();

    tree->Fill();
    tree->Write();
    outfile->Close();
    return sigma;

}
int main (int argc, char** argv){
    SetMystyle();  
    // gStyle->SetOptFit(1111);                                                        
    //set initial parmeters
    TString rootfile;
    TString inputfilename;
    TString rob_id = "2";
     for(int i = 0; i < argc; i ++){
        if(strcmp(argv[i], "-ROB") == 0){
            rob_id = argv[i+1];
        }
    }
    TString ROB_id = rob_id;

    TString pathDir1 = "../Result";
    TString pathDir2 = "./Final_Result";
    rootfile = pathDir1 + "/fit_result_ROB_"+ ROB_id +".root";
    inputfilename = pathDir2 + "/ROB_"+ ROB_id +"_final_result.txt";

    int *Sigma = Getsigma(inputfilename, ROB_id);
    TString filename = rootfile;
    TFile *infile = new TFile(filename, "READ");
    // Check if the file is opened successfully
    if (!infile || infile->IsZombie()) {
        std::cerr << "Error: Unable to open file!" << std::endl;
        return 0;
    }

    // for(int id = 0 ; id < 64; id ++){
    //     TString histname;
    //     if (id < 10)
    //         histname = "h_charge_ROB0" + ROB_id + "_ch0" + id  + "_sigma_" + Sigma[id];
    //     else
    //         histname = "h_charge_ROB0" + ROB_id + "_ch" + id + "_sigma_" + Sigma[id];
    //     cout << histname << endl;
    //     TH1F *histogram = (TH1F*)infile->Get(histname);
    //     histogram->SetLineWidth(2); // Set the line width to 2
    //     histogram->SetLineColor(1); // Set the line width to 2
        
    //     TCanvas *canvas1 = new TCanvas("canvas1", "Histogram Canvas", 800, 600);
    //     canvas1->cd();
    //     gPad->SetLogy(); // Sets logarithmic scale for the current pad
    //     histogram->Draw();
    //     canvas1->SaveAs(Form("./ROB"+ ROB_id + "/charge_rob" + ROB_id + "_channel_%d" + "_sigma_" + Sigma[id]+ ".pdf", id));
    // }
    TCanvas *canvas1 = new TCanvas("canvas1", "Histogram Canvas", 800, 600);
    canvas1->Print("Final_Result/ROB_" + ROB_id + "_final_result.pdf[");
    gPad->SetLogy();     
    for(int id = 0 ; id < 64; id ++){
        
        TString histname;

         if (ROB_id <10){
        if (id < 10)
            histname = "h_charge_ROB0" + ROB_id + "_ch0" + id  + "_sigma_" + Sigma[id];
        else
            histname = "h_charge_ROB0" + ROB_id + "_ch" + id + "_sigma_" + Sigma[id];
    }
    else{
       if (id < 10)
            histname = "h_charge_ROB" + ROB_id + "_ch0" + id  + "_sigma_" + Sigma[id];
        else
            histname = "h_charge_ROB" + ROB_id + "_ch" + id + "_sigma_" + Sigma[id];
    }
    
        
        cout << histname << endl;
        TH1F *histogram = (TH1F*)infile->Get(histname);
        histogram->SetLineWidth(2); // Set the line width to 2
        histogram->SetLineColor(1); // Set the line width to 2
        histogram->GetXaxis()->SetRangeUser(0, 1500);
         // Sets logarithmic scale for the current pad
        histogram->Draw();
        canvas1->Print("Final_Result/ROB_" + ROB_id + "_final_result.pdf");    
    }
    canvas1->Print("Final_Result/ROB_" + ROB_id + "_final_result.pdf]");
    return 0;
}