import pandas as pd
import matplotlib.pyplot as plt
from numpy import sqrt

#Creates the a dataframe containing the raw data, and converts the comma seperated values in the total population column into integers#
CCG_rawdata = pd.read_csv(r"https://github.com/LinnHtatLu/NHSEgraphs/blob/main/Similar10CCGs/April2020_SimilarCCGData.csv?raw=true").dropna(axis = 1)
CCG_rawdata["poptot"] = CCG_rawdata['poptot'].str.replace(',','').astype(float).astype(int)

#Calculates the means, standard deviation and then the ceiling in order to cap any outliers later#
means = CCG_rawdata.mean(numeric_only = True)
stdevs = CCG_rawdata.std(numeric_only = True)
ceiling = 5*stdevs + means

#Creates a new dataframe for the transformed data, as a copy of the original dataframe#
CCG_transdata = CCG_rawdata.copy()

#Creates a dictionary containing the weights for each variable, assigning the weights to the appropriate variable as a key#
weight_list = sqrt([0.25,0.15,0.1,0.1,0.1,0.15,0.03,0.03,0.03,0.03,0.03])
weights = {key: value 
           for key, value in 
           zip(ceiling.index,weight_list)}

#For loop, which goes through every column in the transformed dataframe, and does the following (in order):#
for column in ceiling.index:
    CCG_transdata.loc[CCG_rawdata[column] >= ceiling[column], [column]] = ceiling[column] # Caps every value that is higher than the ceiling value for that column to the ceiling value #
    CCG_transdata[column] = sqrt(CCG_transdata[column]) # Takes the squareroot of all the values #
    CCG_transdata[column] = (CCG_transdata[column] - CCG_transdata[column].mean())/CCG_transdata[column].std() # Normalises the data such that the mean is zero and the standard deviation is 1 #
    CCG_transdata[column] = CCG_transdata[column] *weights[column]
# Creates the similarity dataframe, which records how distant every CCG is from every other CCG in vector space, where distance is the weighted squared euclidean distance. The dataframe's columns and index values are CCG codes#
similarity_df = pd.DataFrame(columns =  ["CCG1"] + list(CCG_transdata["CCGcode"].values))
similarity_df["CCG1"] = CCG_transdata["CCGcode"]
similarity_df.set_index("CCG1", inplace = True)


#For loop, which systematically goes through the empty similarity dataframe above starting from the first row and column (top left) and working along until...#
for CCG1 in similarity_df.index:
    for CCG2 in similarity_df.columns:
        if CCG1 == CCG2:
            similarity_df.loc[CCG1, [CCG2]] = 0 #...it reaches the point where the column and row represent the same CCG, at which point it sets the value of that cell to zero and then...#
            break #it moves on to the next row#
        else:
#otherwise, it calculates the distance by summing the difference in all the variables (numerical columns in CCG_transdata) between the two CCGs, and sets both that cell AND its mirror image counterpart (reflecting along the diagonal) to that value. Saves runtime as we don't have to calculate everything twice!#
            sum_list = []
            for variable in ceiling.index:
                sum_list += [((CCG_transdata[CCG_transdata["CCGcode"] == CCG1][variable].values - CCG_transdata[CCG_transdata["CCGcode"] == CCG2][variable].values)**2)[0]]
            similarity_df.loc[CCG1, [CCG2]] = sum(sum_list)
            similarity_df.loc[CCG2, [CCG1]] = similarity_df[CCG2][CCG1]
#Creates an emtpy dataframe that will contain every CCGcode and the CCGcodes of the 10 CCGs it is most simliar to#
similar10_df = pd.DataFrame(columns = ["CCGcode",1,2,3,4,5,6,7,8,9,10])
similar10_df.set_index("CCGcode", inplace = True)

#For every CCG in the distance dataframe sorts its row by ascending values of distance takes the first 11 values and excludes the first (as every CCG is obviously most similar to itself), in order to give the 10 most similar CCGs to that CCG#
for CCG in CCG_transdata["CCGcode"]:
    similar10_df.loc[CCG] = similarity_df.loc[CCG].sort_values(ascending = True).head(11)[1:].index
print(similar10_df)
