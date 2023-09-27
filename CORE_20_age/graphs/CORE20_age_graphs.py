import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.cm import get_cmap
cmap = get_cmap("tab20")

age_df = pd.read_csv(r"https://github.com/LinnHtatLu/NHSEgraphs/blob/main/CORE_20_age/census2021-age-lsoa.csv?raw=true")
age_df = age_df.drop(["date","geography"], axis = 1)

LSOA21_IMD = pd.read_csv(r"https://github.com/LinnHtatLu/NHSEgraphs/blob/main/CORE_20_age/LSOA21_IMD.csv?raw=true")
LSOA21_IMD = LSOA21_IMD.sort_values(by = "LSOA21 code")

age_df = age_df.merge(LSOA21_IMD, how = 'inner', left_on = "geography code", right_on = "LSOA21 code").drop(["Unnamed: 0","LSOA21 code", "IMD score"], axis = 1)

x = sorted(age_df["IMD decile"].unique())

age_list = []
bar_names = []
for i in age_df.columns[2:-1]:
    age_list += [age_df.groupby(["IMD decile"])[i].sum()]
    bar_names += [i[9:].replace(" years","")]
    
prop_list = []
bar_list = []
fig2, ax2 = plt.subplots()
ax2.set_xticks(x)
for i in range(len(age_list)):
    prop_list += [age_list[i]/age_df.groupby(["IMD decile"]).sum(numeric_only = True)["Age: Total"]]
    bar_list += [ax2.bar(x,prop_list[i], color = cmap.colors[i], bottom = sum(prop_list[:i]))]
ax2.legend(bar_list[::-1], bar_names[::-1], bbox_to_anchor = (1.05, 1))
ax2.set_ylabel("Proportion")
ax2.set_xlabel("IMD decile - where 1 is most deprived")
ax2.set_title("Proportion of IMD deciles in England by age band")
plt.show(fig2)

fig3, axs = plt.subplots(2,9, sharey = True, sharex = True)
fig3.set_figwidth(36)
fig3.set_figheight(10)
fig3.suptitle("Populations of age bands across IMD deciles in England", y = 1, weight = "bold", size = 25)
for i in range(len(age_list)):
    if i <= 8:
        axs[0,i].bar(x,age_list[i], color = cmap.colors[i])
        axs[0,i].set_title(bar_names[i], size = 18)
    else:
        axs[1,i-9].bar(x,age_list[i], color = cmap.colors[i])
        axs[1,i-9].set_title(bar_names[i], size = 18)
axs[0,0].set_ylabel("Population", size = 18)
axs[1,0].set_xlabel("IMD decile - where 1 is most deprived", size = 18)
axs[0,0].set_xticks(x)
plt.show(fig3)
