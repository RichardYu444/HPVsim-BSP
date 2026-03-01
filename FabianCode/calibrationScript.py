# Import HPVsim
import hpvsim as hpv
import numpy as np

import numpy as np

import pickle



#Importing interventions from specific models of NHS England interventions
import NHS_2025_lambdamu, NHS_Vacc
from CalibbasePars import base_pars

#NOTE: this calibration is using the NHS alg of 2025+ as an approximation of the full history of NHS screening - note that my F caloibrations show that this works when trainign to all the data, so I may as well go and train on just the start of teh data right now!

if __name__=="__main__":
    #---SET UP SIMULATION TO CALIBRATE---#
    pars = base_pars
    pars['interventions'] =  NHS_2025_lambdamu.get_interventions(l=1, m=1)  + NHS_Vacc.vaccinations
    
    sim = hpv.Sim(pars) 
    
    #sim.run()
    #quit()

    #---SET UP CALIBRATION---#

    # Configure a simulation with some parameters
    
    #I have added new extended ranges where the best parameters from the [B] cals are near to the sides of the ranges. old ranges commented to the right  
    calib_pars = dict(
            beta=[0.25,0.00,0.50],# 1st, [0.25,0.00,0.50], 2nd [0.25,0.00,0.50]
            f_cross_layer= [0.15, 0, 1], #1st,  [0.15, 0, 1]
            m_cross_layer= [0.25, 0, 1], #1st, [0.25, 0, 1]
            
        )

    genotype_pars = dict(
        hpv16=dict(
            cin_fn=dict(k=[0.25, 0.0, 1.0]),#1st, dict(k=[0.25, 0.0, 1.0])
            dur_cin=dict(par1=[5, 1, 12])#1st, dict(par1=[5, 1, 12])
        ),
        hpv18=dict(
            cin_fn=dict(k=[0.25, 0.0, 1.0]),#1st dict(k=[0.25, 0.0, 1.0])
            dur_cin=dict(par1=[5, 1, 12])#1st dict(par1=[5, 1, 12])
        ),
        hi5=dict(
            cin_fn=dict(k=[0.1, 0.0, 1.5]), #1st, dict(k=[0.25, 0.0, 1.0])
            dur_cin=dict(par1=[3, 0.5, 12]), #1st, dict(par1=[5, 1, 12])
            rel_beta=[0.9,0,1] #1st, [0.9,0,1]
        ),
        ohr=dict(
            cin_fn=dict(k=[0.1, 0.0, 1.5]), #1st, dict(k=[0.25, 0.0, 1.0])
            dur_cin=dict(par1=[5, 1, 12]), #1st dict(par1=[5, 1, 12])
            rel_beta=[0.9,0,1] #1st [0.9,0,1]
        )
    )

    # List the datafiles that contain data that we wish to compare the model to:
    datafiles=["caldata/new_cervical_cancer_cases_ENGSCALED1P19TOUK_START.csv",
               "caldata/mesherHPVCancerDist.csv"]

    # Create the calibration object, run it, and plot the results
    name = "CalibrationRawResults/01Mar_01"
    
    calib = hpv.Calibration(
        sim,
        calib_pars=calib_pars,
        genotype_pars=genotype_pars,
        datafiles=datafiles,

        total_trials=2000,
        n_workers= 5, #to be changed according to the multiprocessing capability of the hardware being used

        keep_db=True,
        name=name
    )

    #---PERFORM CALIBRATION---#
    calib.calibrate(die=False)

    #---ASSESS CALIBRATION QUALITY---#
    #Plot goodness of fit compared to observed data
    calib.plot(res_to_plot=50)
    calib.plot(res_to_plot=10)
    calib.plot(res_to_plot=5)
    calib.plot(res_to_plot=1)

    #---OUTPUT AND SAVE CALIBRATED PARAMETERS---#
    print(calib.df.head(10))

    calib.df.to_csv(f"{name}.csv")

    #TODO: Once I have settled on a final initial setup for calibration: any changes I make to how I calibrate must be shown where relevant in the excel paramter spreadsheet!!

    #TODO: delete all practice/test calibrations from my local copy of the git repo and then change the .gitignore so that my calibration files get uploaded 

    #TODO: cal evaluation shpuld include plots just along an axis for each param with dots on the axis for the sampled parameter positions, with the size + height of teh dot according to its GOF so the goopd ones are most visible in a sea of samples, and we colouyr dots by the calibration we got them from, so we can see how cals differ in the parameters they pick, in the marginals (some persoective, if only in the marginals, is better than none)