[![Build Status](https://travis-ci.org/Tanganelli/CoAPthon3.svg?branch=master)](https://travis-ci.org/Tanganelli/CoAPthon3)

# CoAPthon3
CoAPthon3 is a porting to python3 of my CoAPthon library. CoAPthon3 is a python3 library to the CoAP protocol compliant with the RFC. Branch is available for the Twisted framework.


# Running Automated OCF CTT - Added by Frank Zhong on 20/Jul/2021
The 'client_attempt.py' script can be used for running OCF Certification Tests automatically.

## Prerequisites
This script needs to be run in association with the 'autoctt' library, so please first download the library (https://github.com/Cascoda/autoctt) and follow the instructions in README.md to set up an HTTP server. During an OCF CTT test run, this server handles HTTP requests sent by the basic/extended API of OCTT's Tool Automation Framework.

Please also make sure that 'OCF Conformance Test Tool', the application that actually runs the tests, is installed on your PC; Check that it contains 'CTT_CLI.exe', which is the command line interface version of the test tool. 

## Modifying the Script
For 'client_attempt' to initiate OCF Certification Tests successfully, please follow the steps below to modify the script before running it: 

    1. Search for the 'Run OCF CTT' section of the script and locate where the subprocess.Popen() function is called, which contains the Powershell command to start a test run; 

    2. Change the path to 'CTT_CLI.exe' based on its location on your PC; 

    3. Change the path to the profile (.xml) file you want to include. There are 3 options inside the 'autoctt' library to choose from: 

        I. full_run.xml runs a full test;
        II. single_test.xml runs one specific test (default 1.2.6). This is recommended for debugging purposes;
        III. OCF_profile.xml runs a selected set of tests. Feel free to modify this file according to your needs. 

    4. Change the path to the 'PICS_module.json' file. This is a file inside the 'autoctt' library that needs to be included for running OCF Certification Tests on a Chili 2 module. 

## Usage
After completing all the abovementioned settings, you can simply start 'client_attempt' using: 

'py client_attempt.py'

All test results will be logged into .txt files inside the 'autoctt' library. 