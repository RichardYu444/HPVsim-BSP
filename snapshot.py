import hpvsim as hpv
import numpy as np
import pandas as pd
import pylab as pl
import matplotlib as mpl

if __name__=="__main__":
    pars = dict(
        n_agents      = 20e3,       # Population size
        n_years       = 35,         # Number of years to simulate
        verbose       = 0,          # Don't print details of the run
        rand_seed     = 2,          # Set a non-default seed
        genotypes     = [16, 18],   # Include the two genotypes of greatest general interest
        location      = 'united kingdom'
    )

    snap = hpv.snapshot(timepoints=['2020'])
    sim = hpv.Sim(pars, analyzers=snap)
    sim.run()

    a = sim.get_analyzer()
    people = a.snapshots[0]

    # Plot age mixing

    fig, ax = pl.subplots(nrows=1, ncols=1, figsize=(5, 4))

    fc = people.contacts['m']['age_f'] # Get the age of female contacts in marital partnership
    mc = people.contacts['m']['age_m'] # Get the age of male contacts in marital partnership
    h = ax.hist2d(fc, mc, bins=np.linspace(0, 75, 16), density=True, norm=mpl.colors.LogNorm())
    ax.set_xlabel('Age of female partner')
    ax.set_ylabel('Age of male partner')
    fig.colorbar(h[3], ax=ax)
    ax.set_title('Marital age mixing')
    pl.show();