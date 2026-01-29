import os
import pathlib
import sciris as sc
import matplotlib.pyplot as plt
import hpvsim as hpv
from basePars import base_pars
import NHS_2025_lambdamu, basePars
# -------------------------------------------------------------------
# adjustable settings
# -------------------------------------------------------------------

OUTPUT_DIR = r"C:\Users\richa\Documents\HPV sim Project\Code\ControlCode"
PLOT_FILE      = "control_timeseries.png" #IMPORTANT TO CHANGE EVERYTIME
ALLRUNS   = "control_run2.xlsx" #IMPORTANT TO CHANGE EVERYTIME (maybe?)

N_RUNS = 1 #due to multisim stuff I think 5 is max I can run on a 6 core cpu

desired_pars = [
    "hpv_incidence",
    "hpv_prev",
    "hpv_prevalence",
    "cins",               # CIN2+ / precancerous lesions
    "cancer_incidence",   # Cervical cancer incidence
    "cancer_mortality",   # Cervical cancer mortality (if modelled)
]

seeds = [0, 1, 2, 3] #10 seeds gets us to 5 * 10 = 50 total runs (in theory)

def main():
    #Ensure output directory exists
    outdir = pathlib.Path(OUTPUT_DIR)
    outdir.mkdir(parents=True, exist_ok=True)
    print(f"Outputs will be saved to: {outdir.resolve()}")

    #Define parameters directly here could be prone to adjusting later
    pars = base_pars

    ##add in calibration params

    #Build simulation
    sim = hpv.Sim(pars=pars, label="Control default network")
    print("Created HPVsim simulation.")

    #Run MultiSim
    print(f"Running MultiSim with n_runs = {N_RUNS}  ...")
    msim = hpv.MultiSim(sim)
    msim.run(n_runs = N_RUNS, n_cpus = 5) 
    print("MultiSim run complete.")

    #Plot key outcomes and save as PNG
    #We keep the important indicators in line with what is detectable irl

    skipped_pars = ['genotype_map', 'vaccine map']
    available = []
    #run through each sim done and 
    for sim in msim.sims: 
        for key in sim.results:
            if key not in desired_pars and key not in skipped_pars:
                skipped_pars.append(key)
            if key in desired_pars and key not in available:
                available.append(key)

        #Try to save the run to Excel, need new file name for every 5?
        allruns_path = outdir / ALLRUNS
        try:
            sim.to_excel(allruns_path, skipped_pars)
            print(f"Saved run results to: {allruns_path}")
        except Exception as e:
            print(f"Could not save run results to Excel: {e}")

    if available:
        print(f"Plotting and saving keys: {available}")
        fig = msim.plot(to_plot=available, do_show=False)
        plot_path = outdir / PLOT_FILE
        fig.savefig(plot_path, dpi=300, bbox_inches="tight")
        plt.close(fig)
        print(f"Saved time series plot to: {plot_path}")
    else:
        print("Warning: no desired result keys were found, so no plot was saved.")

    print("Done.")


if __name__ == "__main__":
    main()
