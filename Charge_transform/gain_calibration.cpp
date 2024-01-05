#include <iostream>
#include <cmath> // Include the cmath library for mathematical functions
#include "TMath.h"
using namespace std;
// Define a function for a linear equation: y = mx + c
double linearFunction(double y, double a1) {
    // return a1 * x + a0;
    return y / a1;
}
double expfunction(double y, double a00, double a2, double a3,  double a4)
{
    // double exponent = -1 * a3 * pow(x, a4); // Exponent value
    // cout << exponent << endl;
    
    // return a00 + a2 * (1 - exp(exponent));

    double f1 = TMath::Log(1 - (y - a00) / a2);
    double f2 = -f1 / a3;
    double exponent = 1 / a4;
    double f = TMath::Power(f, exponent);
    cout << f1 << "\t"
         << f2
         << "\t" << exponent << "\t" << f << endl;
    return f;
}
// Define a function for an exponential equation: y = e^(ax)
// double exponentialFunction(double x, double a) {
//     return exp(a * x);
// }
// // Define a function to calculate the power: x^y
// double powerFunction(double x, double y) {
//     return pow(x, y);
// }
int gain_calibration() {
    double x = 319.853; // Input value for x
    double a1 = 65.95; // Slope of the line (m)
    double a0 = 0; // Intercept (c)
    double par1 = 35.19; // a00
    double par2 = 288.98; // a2
    double par3 = 0.1268; // a3
    double par4 = 1.6837; // a4
    double result = expfunction(x, par1, par2, par3, par4);
    // Output the result
    std::cout << "For x = " << x << ", the result is: " << result << std::endl;

    return 0;
}