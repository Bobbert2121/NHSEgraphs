import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from ipywidgets import widgets, interact

COPD_df_base = pd.read_csv(r"https://github.com/Bobbert2121/NHSEgraphs/main/COPD_IMD_by_region/")

COPD_df_base["Colour"] = COPD_df_base["Region"].replace(COPD_df_base.Region.unique(),["red","orange","yellow","green","cyan","blue","violet"])
Region = widgets.Dropdown(options = ["England","All Regions except London and Midlands"]+ list(COPD_df_base["Region"].unique()), description = "Region:",)

def plotit(area_of_interest):
    if area_of_interest == "England":
        COPD_df = COPD_df_base
    elif area_of_interest == "All Regions except London and Midlands":
        COPD_df= COPD_df_base.drop(COPD_df_base[(COPD_df_base.Region == "London")|(COPD_df_base.Region == "Midlands")].index)
    else:
        COPD_df = COPD_df_base.drop(COPD_df_base[~(COPD_df_base.Region == area_of_interest)].index)

    unfitted_y = COPD_df["Prevalence (%)"]
    y, unfitted_lambda = stats.boxcox(unfitted_y)

    fig, axs = plt.subplots(1,8, sharey = True, sharex = True)
    fig.set_size_inches(25,3)
    corr_dic = {}
    for i in range(0,8):
        x = COPD_df.iloc[:,i+3]
        axs[i].scatter(x, y, c = COPD_df["Colour"])
        axs[i].set_xlabel(COPD_df.columns[i+3][:-14])
        axs[i].plot(x,np.poly1d(np.polyfit(COPD_df.iloc[:,i+3],y,1))(x), linestyle = ":", color = "black")
        corr_dic[COPD_df.columns[i+3]] = {stats.pearsonr(x, y)}
        axs[i].text(min(x),min(y)-abs(max(y)-min(y))/2, str("R =" + str(np.format_float_positional(list(corr_dic[COPD_df.columns[i+3]])[0][0],precision =4, fractional = False)) + "\np =" + str(np.format_float_scientific(list(corr_dic[COPD_df.columns[i+3]])[0][1],precision= 4))))
    axs[0].set_ylabel("Transformed Prevalence")
    fig.suptitle("Box-Cox transformed COPD % prevalence against IMD19 and domain population-averaged ranks for CCG19s in "+ str(area_of_interest), weight = "bold")

    fig2, axs2 = plt.subplots(1,8,sharey = True)
    fig2.set_size_inches(30,3)
    for i in range(0,8):
        residuals = y - np.poly1d(np.polyfit(COPD_df.iloc[:,i+3],y,1))(COPD_df.iloc[:,i+3])
        std_err = np.sqrt(residuals.var())
        std_residuals = residuals/std_err
        axs2[i].scatter(np.poly1d(np.polyfit(COPD_df.iloc[:,i+3],y,1))(COPD_df.iloc[:,i+3]), std_residuals, c = COPD_df["Colour"])
        axs2[i].set_xlabel(COPD_df.columns[i+3][:-14])
    fig2.suptitle("Fitted against standardised residual plot for Box-Cox transformed COPD % prevalance against IMD and domain population-averaged ranks for CCG19s in " + str(area_of_interest), weight = "bold")
    plt.show(fig,fig2)
interact(plotit,area_of_interest = Region)
