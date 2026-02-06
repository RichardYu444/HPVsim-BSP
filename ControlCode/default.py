import pathlib
import sciris as sc
import matplotlib.pyplot as plt
import hpvsim as hpv
import NHS_2025_lambdamu, basePars as basePars
from basePars import base_pars_geno
import pickle
# -------------------------------------------------------------------
# adjustable settings
# -------------------------------------------------------------------

OUTPUT_DIR = r'C:\Users\richa\Documents\HPV sim Project\Code\ControlCode'
#PLOT_FILE      = 'control_timeseries.png' #IMPORTANT TO CHANGE EVERYTIME
ALLRUNS   = 'default.csv' #IMPORTANT TO CHANGE EVERYTIME (maybe?)

N_RUNS = 5 #due to multisim stuff I think 5 is max I can run on a 6 core cpu

# this only really needed if plotting, but for now, we exclude
# desired_results = [
#     'hpv_incidence',
#     'hpv_prev',
#     'hpv_prevalence',
#     'cins',               # CIN2+ / precancerous lesions
#     'cancer_incidence',   # Cervical cancer incidence
#     'cancer_mortality',   # Cervical cancer mortality (if modelled)
# ]

seeds = [0]#, #6, 12, 18, 24, 30, 36, 42, 48, 54] #10 seeds gets us to 5 * 10 = 50 total runs (in theory)

def main():
    #Ensure output directory exists
    outdir = pathlib.Path(OUTPUT_DIR)
    outdir.mkdir(parents=True, exist_ok=True)
    print(f'Outputs will be saved to: {outdir.resolve()}')

    #run through seeds to run sim, 5 at a time, hence the gaps in seeds
    for seed in seeds:
        base_pars_geno['rand_seed'] = seed
        #Build simulation
        sim = hpv.Sim(base_pars_geno, label='Control default network')
        print('Created HPVsim simulation.')
        #Run MultiSim
        print(f'Running MultiSim with n_runs = {N_RUNS}  ...')
        msim = hpv.MultiSim(sim)
        msim.run(n_runs = N_RUNS, n_cpus = 5) 
        print('MultiSim run complete.')

        #We keep the important indicators in line with what is detectable irl

        skipped_pars = ['genotype_map', 'vaccine map'] #these are skipped as their datatype doesn't convert to df
        # available = []
        allruns_path = outdir / ALLRUNS
        #i helps keep track of which seed we are on, but is onlly for debugging purposes really
        i = 0
        #run through each sim done and 
        for sim in msim.sims: 
            # for key in sim.results:
            #     if key not in desired_results and key not in skipped_pars:
            #         skipped_pars.append(key)
            #     if key in desired_pars and key not in available:
            #         available.append(key)

            #Try to save the run to Excel, need new file name for every 5?

            try:
                temp_df = sim.to_df(date_index = True)
                print('sim made into df')
            except Exception as e:
                print(f'Could not save run results to df: {e}')
            temp_df['Seed'] = seed + i
            temp_df.to_csv(ALLRUNS, mode = 'a', index = True)
            print(f'Seed:{seed + i} is done')
            i += 1

        #if available:
         #   print(f'Plotting and saving keys: {available}')
          #  fig = msim.plot(to_plot=available, do_show=False)
           # plot_path = outdir / PLOT_FILE
          #  fig.savefig(plot_path, dpi=300, bbox_inches='tight')
           # plt.close(fig)
           # print(f'Saved time series plot to: {plot_path}')
       # else:
        #    print('Warning: no desired result keys were found, so no plot was saved.')

    print('Done.')


if __name__ == '__main__':
    main()
