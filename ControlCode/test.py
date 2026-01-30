import pandas as pd
import sciris as sc
import pickle
import hpvsim as hpv
from basePars import base_pars


sim = hpv.Sim(base_pars) 


calib_pars = dict( #to make the dummy calibration work, doing a cal with just beta. to make sure this script works as desired, make sure the dummy calibration is for a varaible which will be overriden with our hardcoded parameters - picking beta here as i think any calibration I do will involve beta, in which case it will be always overriden
                beta=[0.05, 0.00, 0.20], 
            )
calib = hpv.Calibration(
    sim,
    calib_pars=calib_pars,
    datafiles= [#"C:\Users\richa\Documents\HPV sim Project\Code\ControlCode",
                "mesherHPVCancerDist.csv",
                ],
    total_trials=1,
    n_workers=1,
    keep_db=True,
    name= "dummycalib2"
)
calib.calibrate(die=False)            
sim_pars = calib.trial_pars_to_sim_pars()
print(sim_pars)