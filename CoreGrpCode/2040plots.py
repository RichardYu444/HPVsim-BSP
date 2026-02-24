import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import numpy as np
from matplotlib.ticker import MaxNLocator
#This is the code that I will use to tplot 2040 stats against our UK target (below 4 per 100,000)

# Load csv file, change name/path as needed
df_all = pd.read_csv("defaultallparam02Feb.csv")
df_noInter  = pd.read_csv("defaultnointer02Feb.csv")
df_noScreen  = pd.read_csv("defaultNoScreen02Feb.csv")
df_noVacc  = pd.read_csv("defaultNoVacc02Feb.csv")

year_target = 2040
col = "cancer_incidence"

s1 = df_all.loc[df_all["year"] == year_target, col].dropna().to_numpy()
s2 = df_noInter.loc[df_noInter["year"]  == year_target, col].dropna().to_numpy()
s3 = df_noScreen.loc[df_noScreen["year"]  == year_target, col].dropna().to_numpy()
s4 = df_noVacc.loc[df_noVacc["year"]  == year_target, col].dropna().to_numpy()

plt.figure(figsize=(7,4))
plt.boxplot([s1, s2, s3, s4],
            tick_labels=["All Interventions", "No Interventions", "Vaccination Only", "Screening Only"],
            showmeans=True,
            showfliers=False
            )
plt.ylabel(f"Cancer incidence in {year_target}")
plt.title("Cancers per 100,000 Women - Default Network")

target_line = plt.axhline(y= 4, color='r', linestyle='-', label = '2040 Target')  
plt.legend(handles = [target_line])
plt.ylim(0, 20)
plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
plt.show()


