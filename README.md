# OECD_BWR_Benchmark
'''
This code was written to serve as an interface to analyze the submittals for 
the "Comparison of Gd2O3-Bearig BWR Fuel Rods"  benchmark for for a bechmark for: 
The Expert Group on Used Nuclear Fuel (EGUNF) of the Working Party on 
Nuclear Criticality Safety (WPNCS) under the Nuclear Science Committee 
(NSC) of the Organisation for Economic Co-operation and Development/Nuclear
Energy Agency (OECD/NEA)

This interface successfully run using:
Bokeh 0.12.6*
Python 3.6.1

*This is the latest Bokeh version and is required for full functionality of the interface
(Use: "pip install bokeh" to download latest version)


Interface written by Shadi Ghrayeb of the U.S. Nuclear Regulatory Commission (USNRC) in collobration
with Oak Ridge National Laboratory (ORNL)

contact: 
Shadi Ghrayeb
Shadi.Ghrayeb@nrc.gov / ghrays@gmail.com

ORNL: 
Ian Gauld (gauldi@ornl.gov)
William "BJ" Marshall (marshallwj@ornl.gov)

Easiest way to run this interface is to download ANACONDA from www.continuum.io/downloads
Open a terminal to the directory where this file exists and enter following command: 
    
    bokeh serve --show main.py
    
After entering the above command a browser should appear displaying the interface using the following url: 
    
    http://localhost:5006/main
    
When running on windows machine there have been issues using Internet Explorer browser. Try alternative browsers by 
entering the above url into Chrome, FireFox, etc. 

'''
