import pandas as pd
import sciris as sc
import pickle
import hpvsim as hpv
from basePars import base_pars

snap = hpv.snapshot(timepoints=['2000'])
sim = hpv.Sim(base_pars, analyzers=snap)

sim.run()
