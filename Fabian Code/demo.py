

import NHS_2025_lambdamu, NHS_Vacc
from basePars import base_pars
import hpvsim as hpv

pars = base_pars
pars['n_agents'] = 1_000
pars['verbose'] = 1
pars['interventions'] =  NHS_2025_lambdamu.get_interventions(l=10, m=10)  + NHS_Vacc.vaccinations
sim = hpv.Sim(pars) 

sim.run()

sim.plot()