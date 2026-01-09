# Import HPVsim
import hpvsim as hpv
import numpy as np

import numpy as np

import pickle

#NOTE: this calibration is using the NHS alg of 2025+ as an approximation of the full history of NHS screening - note that my F caloibrations show that this works when trainign to all the data, so I may as well go and train on just the start of teh data right now!

if __name__=="__main__":
    #---SET UP SIMULATION TO CALIBRATE---#

    sim = hpv.Sim() 

    #---SET UP CALIBRATION---#

    # Configure a simulation with some parameters
    
    #I have added new extended ranges where the best parameters from the [B] cals are near to the sides of the ranges. old ranges commented to the right  
    calib_pars = dict(
            beta=[0.25,0.00,0.50],#[0.05, 0.00, 0.20], #still happy
            f_cross_layer= [0.15, 0, 1], #always close to 0 but as i think this cant be negaative, still happy
            m_cross_layer= [0.25, 0, 1], #pretty close to 0, not quite aas much aas f, but still i think i cnt extend the range so happy (for 3, this is also super super close to 0)
            
        )

    genotype_pars = dict(
        hpv16=dict(
            cin_fn=dict(k=[0.5, 0.0, 1.0]),#(k=[0.5, 0.2, 1.0]), haappy now they can be around 0.1 - 3 agrees
            dur_cin=dict(par1=[6, 1, 12])#dict(par1=[6, 4, 12]) perhaaps push this even lower to 1 min, it seems aaraound 2-3.5 but still. 3 cnt seem to settle here, maybe doesnt maatter thaat much
        ),
        hpv18=dict(
            cin_fn=dict(k=[0.5, 0.0, 1.0]),#dict(k=[0.5, 0.2, 1.0]), haappy now these cn be v small for both caals, it does seem to waant to be quite small
            dur_cin=dict(par1=[6, 1, 12])#dict(par1=[6, 4, 12]) these seem to waant to be big in 2 and 3, but i wamnder if th9is is because of asymmtery with range of 16, so first lets make them match
        ),
        hi5=dict(
            cin_fn=dict(k=[0.5, 0.0, 1.0]),
            dur_cin=dict(par1=[6, 1, 12]),
            rel_beta=[0.9,0,1]
        )
    )

    # List the datafiles that contain data that we wish to compare the model to:
    datafiles=["mesherHPVCancerDist.csv"]

    # List extra results that we don't have data on, but wish to include in the
    # calibration object so we can plot them.
    results_to_plot = ['cancer_incidence', 'asr_cancer_incidence']

    # Create the calibration object, run it, and plot the results
    name = "d3Cal_7OOct25_ZB_G_butNHS2025ONLYsimplyStartingAt1980_5"
    
    calib = hpv.Calibration(
        sim,
        calib_pars=calib_pars,
        genotype_pars=genotype_pars,
        #extra_sim_result_keys=results_to_plot,
        datafiles=datafiles,

        total_trials=1, #50
        n_workers=1,#12, #5

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

    #Additional plotting to assess how the calibration went
    #calib.plot_learning_curve()
    #calib.plot_timeline()

    #---OUTPUT AND SAVE CALIBRATED PARAMETERS---#
    print(calib.df.head(10))

    #calib.df.to_csv(f"{name}.csv")