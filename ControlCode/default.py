import os
import pathlib

import matplotlib.pyplot as plt
import hpvsim as hpv


# -------------------------------------------------------------------
# adjustable settings
# -------------------------------------------------------------------

OUTPUT_DIR = r"C:\Users\richa\Documents\HPV sim Project\Code\Control Code"
PLOT_FILE      = "control_timeseries.png"
REDUCED_XLSX   = "control_reduced.xlsx"
ALLRUNS_XLSX   = "control_all_runs.xlsx"
METADATA_TXT   = "control_metadata.txt"
N_RUNS = 5 

desired_keys = [
    "hpv_incidence",
    "hpv_prev",
    "hpv_prevalence",
    "cins",               # CIN2+ / precancerous lesions
    "cancer_incidence",   # Cervical cancer incidence
    "cancer_mortality",   # Cervical cancer mortality (if modelled)
]

def main():
    #Ensure output directory exists
    outdir = pathlib.Path(OUTPUT_DIR)
    outdir.mkdir(parents=True, exist_ok=True)
    print(f"Outputs will be saved to: {outdir.resolve()}")

    #Define parameters directly here could be prone to adjusting later
    pars = dict(
        location = 'united kingdom',
        n_agents = 1e5,             #6e5 for 1% of England population
        start    = 1995,
        n_years  = 40,
        burnin   = 15,
        verbose  = 0,
        network  = "default",   # default sexual network
    )

    #Build simulation
    sim = hpv.Sim(pars=pars, label="Control default network")
    print("Created HPVsim simulation.")

    #Run MultiSim
    print(f"Running MultiSim with n_runs = {N_RUNS}  ...")
    msim = hpv.MultiSim(sim)
    msim.run(n_runs = N_RUNS, n_cpus = 5) #since 8 thread computer let's stick with 5 workers to be safe
    print("MultiSim run complete.")
    reduced = msim.reduce(output=True)

    #Plot key outcomes and save as PNG
    #We keep the important indicators in line with what is detectable irl


    base_sim = msim.base_sim
    available = []
    for key in desired_keys:
        if key in base_sim.results and key not in available:
            available.append(key)

    if available:
        print(f"Plotting and saving keys: {available}")
        fig = msim.plot(to_plot=available, do_show=False)
        plot_path = outdir / PLOT_FILE
        fig.savefig(plot_path, dpi=300, bbox_inches="tight")
        plt.close(fig)
        print(f"Saved time series plot to: {plot_path}")
    else:
        print("Warning: no desired result keys were found, so no plot was saved.")

    #Save reduced simulation results to Excel
    reduced_path = outdir / REDUCED_XLSX
    try:
        reduced.to_excel(reduced_path)
        print(f"Saved reduced simulation results to: {reduced_path}")
    except Exception as e:
        print(f"Could not save reduced simulation to Excel: {e}")

    # 7. Try to save all runs (MultiSim) to Excel (may not be supported in all versions)
    allruns_path = outdir / ALLRUNS_XLSX
    try:
        msim.to_excel(allruns_path)
        print(f"Saved all-run MultiSim results to: {allruns_path}")
    except Exception as e:
        print(f"Could not save MultiSim all-run results to Excel: {e}")

    # 8. Write a small metadata summary file
    meta_path = outdir / METADATA_TXT
    try:
        with open(meta_path, "w", encoding="utf-8") as f:
            f.write("default-network control scenario\n")
            f.write("-----------------------------------\n")
            f.write(f"n_runs (MultiSim): {N_RUNS}\n")
        print(f"Saved metadata to: {meta_path}")
    except Exception as e:
        print(f"Could not write metadata file: {e}")

    print("Done.")


if __name__ == "__main__":
    main()
