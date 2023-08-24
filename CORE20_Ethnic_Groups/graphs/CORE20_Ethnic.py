import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = ["Arial"]

#Import LSOA21 IMD scores and deciles, in order to create dataframe#
LSOA21_IMD = pd.read_csv(r"https://github.com/Bobbert2121/NHSEgraphs/blob/main/CORE20_Ethnic_Groups/LSOA21_IMD.csv?raw=true")

#Create DataFrame of Ethnic populations of LSOA21s#
Ethnic_pop = pd.read_csv(r"https://github.com/Bobbert2121/NHSEgraphs/blob/main/CORE20_Ethnic_Groups/Ethnic_Group_LSOA_IMD_2021Census.csv?raw=true")
Ethnic_pop=Ethnic_pop[["geography code","Ethnic group: Total: All usual residents","Ethnic group: Asian, Asian British or Asian Welsh","Ethnic group: Black, Black British, Black Welsh, Caribbean or African", "Ethnic group: Mixed or Multiple ethnic groups","Ethnic group: White","Ethnic group: Other ethnic group"]]
Ethnic_pop["Index of Multiple Deprivation (IMD) Decile (where 1 is most deprived 10% of LSOAs)"] = ''

#Creates additional column in Ethnic_pop with the IMD decile of every LSOA21 using the LSAO21_IMD DataFrame as a reference#
for LSOA21 in LSOA21_IMD["LSOA21 code"]:
    Ethnic_pop["Index of Multiple Deprivation (IMD) Decile (where 1 is most deprived 10% of LSOAs)"].loc[Ethnic_pop[Ethnic_pop["geography code"] == LSOA21].index] = int(LSOA21_IMD[LSOA21_IMD["LSOA21 code"] == LSOA21]["IMD decile"].sum())

#Cleaning the data#
Ethnic_pop["Index of Multiple Deprivation (IMD) Decile (where 1 is most deprived 10% of LSOAs)"].replace('',np.nan, inplace = True)
Ethnic_pop = Ethnic_pop.dropna()
Ethnic_pop["Index of Multiple Deprivation (IMD) Decile (where 1 is most deprived 10% of LSOAs)"] = Ethnic_pop["Index of Multiple Deprivation (IMD) Decile (where 1 is most deprived 10% of LSOAs)"].astype(int)

#Defining Values from DataFrame#
x = sorted(Ethnic_pop["Index of Multiple Deprivation (IMD) Decile (where 1 is most deprived 10% of LSOAs)"].unique())
White = Ethnic_pop.groupby(["Index of Multiple Deprivation (IMD) Decile (where 1 is most deprived 10% of LSOAs)"]).sum(numeric_only = True)["Ethnic group: White"]/1000000
Black = Ethnic_pop.groupby(["Index of Multiple Deprivation (IMD) Decile (where 1 is most deprived 10% of LSOAs)"]).sum(numeric_only = True)["Ethnic group: Black, Black British, Black Welsh, Caribbean or African"]/1000000
Asian = Ethnic_pop.groupby(["Index of Multiple Deprivation (IMD) Decile (where 1 is most deprived 10% of LSOAs)"]).sum(numeric_only = True)["Ethnic group: Asian, Asian British or Asian Welsh"]/1000000
Mix = Ethnic_pop.groupby(["Index of Multiple Deprivation (IMD) Decile (where 1 is most deprived 10% of LSOAs)"]).sum(numeric_only = True)["Ethnic group: Mixed or Multiple ethnic groups"]/1000000
Other = Ethnic_pop.groupby(["Index of Multiple Deprivation (IMD) Decile (where 1 is most deprived 10% of LSOAs)"]).sum(numeric_only = True)["Ethnic group: Other ethnic group"]/1000000
Total = Ethnic_pop.groupby(["Index of Multiple Deprivation (IMD) Decile (where 1 is most deprived 10% of LSOAs)"]).sum(numeric_only = True)["Ethnic group: Total: All usual residents"]/1000000

#Creating first figure, a stacked bar graph of the population of ethnic minorities in each IMD decile#
fig, ax1 = plt. subplots()

Asian_bar = ax1.bar(x, Asian)
Black_bar = ax1.bar(x, Black, bottom = Asian)
Mix_bar = ax1.bar(x , Mix, bottom = Black + Asian)
Other_bar = ax1.bar(x, Other, bottom = Black + Asian + Mix)
ax1.set_xticks(x)
ax1.set_title("Populations of Minority Ethnic Groups by IMD Decile")
ax1.set_xlabel("IMD Decile - where 1 is most deprived")
ax1.set_ylabel("Population(in Millions)")
ax1.legend([Other_bar, Mix_bar, Black_bar, Asian_bar],["Other","Mixed","Black","Asian"], bbox_to_anchor= (1.2, 1))

# Second figure, a stacked bar graph of the proportion of the population of each IMD decile belonging to each broad ethnic group#
fig2, ax2 = plt.subplots()

White_prop = White/Total
Asian_prop = Asian/Total
Black_prop = Black/Total
Mix_prop = Mix/Total
Other_prop = Other/Total

Asian_prop_bar = ax2.bar(x, Asian_prop, bottom = White_prop)
Black_prop_bar = ax2.bar(x, Black_prop, bottom = White_prop + Asian_prop)
Mix_prop_bar = ax2.bar(x, Mix_prop, bottom = White_prop + Asian_prop + Black_prop)
White_prop_bar = ax2.bar(x, White_prop, color = "tab:purple")
Other_prop_bar = ax2.bar(x, Other_prop, bottom = Asian_prop + Black_prop + Mix_prop + White_prop)

ax2.set_xticks(x)
ax2.set_title("Ethnic Group Proportions by IMD19 Decile")
ax2.set_xlabel("IMD Decile - where 1 is most deprived")
ax2.set_ylabel("Proportion")
ax2.legend([Other_prop_bar,Mix_prop_bar,Black_prop_bar,Asian_prop_bar,White_prop_bar],["Other","Mixed","Black","Asian","White"], bbox_to_anchor = (1.05,1))

ax2.bar_label(White_prop_bar, label_type = "center", color = "white", fmt='%.2f')
for i in range(10):
    ax2.plot([i+1.42,i+1.45,i+1.45 ,i+1.42], [White_prop[i+1],White_prop[i+1],1,1], 'k-', lw=2)
    ax2.text(i+1, 1.01, round(1 - White_prop[i+1],2), fontsize = 10, weight = "bold", color = "black")

#Third figure, a series of subplots of the populations of each minority ethnic group in each IMD decile#
fig3, axs = plt.subplots(1,4, sharex = True, sharey = True)
fig3.tight_layout(h_pad = 3)
fig3.set_figwidth(15)
fig3.set_figheight(5)
fig3.suptitle("Populations of minortiy ethnic groups in each IMD decile", y = 1.05, weight = "bold")

axs[0].bar(x,Asian)
axs[0].set_title("Asian")
axs[0].set_xticks(x)
axs[0].set_ylabel("Population(in Millions)")
axs[0].set_xlabel("IMD Decile - where 1 is most deprived")

axs[1].bar(x,Black, color = "tab:orange")
axs[1].set_title("Black")
axs[1].set_xlabel("IMD Decile - where 1 is most deprived")

axs[2].bar(x,Mix, color = "tab:green")
axs[2].set_title("Mixed")
axs[2].set_xlabel("IMD Decile - where 1 is most deprived")

axs[3].bar(x,Other, color = "tab:red")
axs[3].set_title("Other")
axs[3].set_xlabel("IMD Decile - where 1 is most deprived")

#Adds an additional boolean column to Ethnic_pop, which is True if the LSOA is in the CORE20 and false otherwise#
Ethnic_pop["Core20?"] = Ethnic_pop["Index of Multiple Deprivation (IMD) Decile (where 1 is most deprived 10% of LSOAs)"] <= 2

#Defines the values for the fourth figure#
Total_CORE20 = Ethnic_pop.groupby(["Core20?"])["Ethnic group: Total: All usual residents"].sum()
White_prop_CORE20 = Ethnic_pop.groupby(["Core20?"])["Ethnic group: White"].sum()/Total_CORE20
Asian_prop_CORE20 = Ethnic_pop.groupby(["Core20?"])["Ethnic group: Asian, Asian British or Asian Welsh"].sum()/Total_CORE20
Black_prop_CORE20 = Ethnic_pop.groupby(["Core20?"])["Ethnic group: Black, Black British, Black Welsh, Caribbean or African"].sum()/Total_CORE20
Mix_prop_CORE20 = Ethnic_pop.groupby(["Core20?"])["Ethnic group: Mixed or Multiple ethnic groups"].sum()/Total_CORE20
Other_prop_CORE20 = Ethnic_pop.groupby(["Core20?"])["Ethnic group: Other ethnic group"].sum()/Total_CORE20

#Creating 4th figure, a bar graph showing the proportions of the ethnic groups in the CORE20 and non-CORE20 populations of England#
fig4, ax4 = plt.subplots()
White_CORE20_bar = ax4.bar(["All other quintiles","Most deprived quintile"], White_prop_CORE20, color = "tab:purple")
Asian_CORE20_bar = ax4.bar(["All other quintiles","Most deprived quintile"], Asian_prop_CORE20, bottom = White_prop_CORE20,  color = "tab:blue")
Black_CORE20_bar = ax4.bar(["All other quintiles","Most deprived quintile"], Black_prop_CORE20, bottom = White_prop_CORE20 + Asian_prop_CORE20,  color = "tab:orange")
Mix_CORE20_bar = ax4.bar(["All other quintiles","Most deprived quintile"], Mix_prop_CORE20, bottom = White_prop_CORE20 + Asian_prop_CORE20 + Black_prop_CORE20,  color = "tab:green")
Other_CORE20_bar = ax4.bar(["All other quintiles","Most deprived quintile"], Other_prop_CORE20, bottom = White_prop_CORE20 + Asian_prop_CORE20 + Black_prop_CORE20 + Mix_prop_CORE20,  color = "tab:red")

ax4.bar_label(White_CORE20_bar, label_type = "center", color = "white", fmt='%.2f')
ax4.plot([0.41,0.43,0.43,0.41], [0.84,0.84,1,1], 'k-', lw=2)
ax4.text(0.45, 0.9, "0.16", fontsize = 10)
ax4.plot([1.41,1.43,1.43,1.41], [0.71,0.71,1,1], 'k-', lw=2)
ax4.text(1.45, 0.9, "0.29", fontsize = 10)
ax4.set(xlim = [-0.6,1.6])

ax4.legend([Other_CORE20_bar, Mix_CORE20_bar, Black_CORE20_bar,Asian_CORE20_bar,White_CORE20_bar],["Other","Mixed","Black","Asian","White"], bbox_to_anchor = (1.05,1))
ax4.set_title("Proportions of the populations of the most deprived quintile compared to all other quintiles belonging to broad ethnic groups")
ax4.set_ylabel("Proportion")
