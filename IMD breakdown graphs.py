import pandas as pd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Creation of DataFrames#
IMD_df = pd.read_csv(r"C:\Users\LinnLu\OneDrive - NHS England\Documents\IMD breakdown data.csv", low_memory = False).iloc[:,:65].dropna()
Domain_ranks = IMD_df.filter(like = "Rank").iloc[:,1:8]
LSOA11_pops = pd.read_csv("C:\\Users\\LinnLu\\OneDrive - NHS England\\2021_Census_Data_LSOA\\LSOA IMD rankings\\LSOA_11_populations.csv")

ICB_lookup = IMD_df[["LSOA code (2011)", "ICB (2022) Name"]]
IMD_score = IMD_df.filter(like = "(IMD) Score")
Inverted_domain_ranks = (32845 - Domain_ranks)/32844
Exp_trans_domains = -23*np.log(1-Inverted_domain_ranks*(1-np.exp(-100/23)))
Exp_trans_domains.columns = ["Income","Employment","Education, Skills and Training","Health Deprivation and Disability","Crime","Barriers to Housing and Services","Living Environment"]

LSOA11_pops = pd.read_csv("C:\\Users\\LinnLu\\OneDrive - NHS England\\2021_Census_Data_LSOA\\LSOA IMD rankings\\LSOA_11_populations.csv")
LSOA11_pops.columns = ["LSOA11 code","population"]
LSOA11_pops = LSOA11_pops.replace(',','', regex=True)
LSOA11_pops["population"] = LSOA11_pops["population"].apply(pd.to_numeric)
LSOA11_pops = LSOA11_pops[LSOA11_pops["LSOA11 code"].str.startswith("E")]
LSOA11_pops = LSOA11_pops.sort_values(by = "LSOA11 code")

weights = np.array([0.225,0.225,0.135,0.135,0.28/3,0.28/3,0.28/3])
weighted_domains = Exp_trans_domains*weights
weighted_domains_ICB = pd.concat([ICB_lookup,weighted_domains, IMD_score], axis = 1)
weighted_domains_ICB = pd.merge(weighted_domains_ICB, LSOA11_pops, how = "inner", left_on = "LSOA code (2011)", right_on = "LSOA11 code")
weighted_domains_ICB = weighted_domains_ICB.drop(["LSOA11 code"], axis = 1)
LSOA11_pops = weighted_domains_ICB["population"]
weighted_domains_ICB= weighted_domains_ICB.drop(["population"], axis = 1)

ICB_breakdown = pd.concat([weighted_domains_ICB[["LSOA code (2011)", "ICB (2022) Name"]],weighted_domains_ICB.select_dtypes(np.number).mul(LSOA11_pops, axis = "index"),LSOA11_pops], axis =1).groupby("ICB (2022) Name").sum(numeric_only = True)
ICB_breakdown = ICB_breakdown.select_dtypes(np.number).drop(["population"], axis = 1).div(ICB_breakdown["population"], axis = "index").sort_values(by = "Index of Multiple Deprivation (IMD) Score")

#Creation of first figure, ICS IMD scores broken down by domain#
fig1, ax1 = plt.subplots()
fig1.set_figwidth(12)
x = ICB_breakdown.index.values
Income_bar = ax1.bar(x, ICB_breakdown["Income"])
Employment_bar = ax1.bar(x, ICB_breakdown["Employment"], bottom = ICB_breakdown["Income"])
Education_bar = ax1.bar(x, ICB_breakdown["Education, Skills and Training"], bottom = ICB_breakdown["Income"] + ICB_breakdown["Employment"])
Health_bar = ax1.bar(x, ICB_breakdown["Health Deprivation and Disability"], bottom = ICB_breakdown["Income"] + ICB_breakdown["Employment"] + ICB_breakdown["Education, Skills and Training"])
Crime_bar = ax1.bar(x, ICB_breakdown["Crime"], bottom = ICB_breakdown["Income"] + ICB_breakdown["Employment"] + ICB_breakdown["Education, Skills and Training"] + ICB_breakdown["Health Deprivation and Disability"])
Barriers_bar = ax1.bar(x, ICB_breakdown["Barriers to Housing and Services"], bottom =ICB_breakdown["Income"] + ICB_breakdown["Employment"] + ICB_breakdown["Education, Skills and Training"] + ICB_breakdown["Health Deprivation and Disability"] + ICB_breakdown["Crime"])
Living_bar = ax1.bar(x, ICB_breakdown["Living Environment"], bottom = ICB_breakdown["Income"] + ICB_breakdown["Employment"] + ICB_breakdown["Education, Skills and Training"] + ICB_breakdown["Health Deprivation and Disability"] + ICB_breakdown["Crime"] + ICB_breakdown["Barriers to Housing and Services"])

ax1.set_xticklabels(x, rotation=90)
ax1.set_ylabel("IMD score")
ax1.legend([Income_bar,Employment_bar,Education_bar,Health_bar,Crime_bar,Barriers_bar,Living_bar][::-1], ICB_breakdown.columns[6::-1], bbox_to_anchor=[1.01,1])
ax1.set_title("Breakdown of ICBs by contribution of Domains to IMD score")

#Creation of second figure,  scatter of LSOAs by IMD score against weighted domain ranks#
fig2, axs = plt.subplots(1,7, sharey = True)
fig2.set_figwidth(20)
fig2.suptitle("IMD19 score against exponentially transformed domain score for LSOA11s in England", weight = "bold")

axs[0].set(ylim=(0,100))
axs[0].set_ylabel("IMD score")

coeff_list = [0,0,0,0,0,0,0]
for i in range(7):
    axs[i].scatter(Exp_trans_domains[Exp_trans_domains.columns[i]], IMD_score, s = 1)
    axs[i].set_xlabel(Exp_trans_domains.columns[i])
    axs[i].set(xlim = (0,100))
    coeff_list[i] = np.polyfit(Exp_trans_domains[Exp_trans_domains.columns[i]], IMD_score, 1).astype(float)
    coeff_list[i] = np.concatenate(coeff_list[i])
    poly1d_fn = np.poly1d(coeff_list[i])
    regression = axs[i].plot(Exp_trans_domains[Exp_trans_domains.columns[i]],poly1d_fn(Exp_trans_domains[Exp_trans_domains.columns[i]]), '--k')

#Creation of final figure, Proportion of IMD score from domain against IMD score#
fig3, axs2 = plt.subplots(1,7, sharey = True)
fig3.set_figwidth(20)
fig3.suptitle("IMD19 score against proportion of score from title domain for LSOA11s in England", weight = "bold")

axs2[0].set_ylabel("Proportion of IMD score")
axs2[0].set(ylim = (0,1))
coeff_list2 = [0,0,0,0,0,0,0]
for i in range(7):
    axs2[i].scatter(IMD_score, weighted_domains[weighted_domains.columns[i]]/np.concatenate(np.array(IMD_score)), s = 1)
    axs2[i].set_xlabel(weighted_domains.columns[i])
    axs2[i].set(xlim = (0,100))
    coeff_list2[i] = np.polyfit(np.concatenate(np.array(IMD_score)),weighted_domains[weighted_domains.columns[i]]/np.concatenate(np.array(IMD_score)), 5)
    poly1d_fn = np.poly1d(coeff_list2[i])
    regression = axs2[i].plot(IMD_score.sort_values(by = "Index of Multiple Deprivation (IMD) Score"),poly1d_fn(IMD_score.sort_values(by = "Index of Multiple Deprivation (IMD) Score")), '--k')