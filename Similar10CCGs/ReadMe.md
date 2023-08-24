<b>This code creates a dataframe containing every CCG in in England as lists the 10 CCGs most similar to that CCG by comparing (taken from methodology guide).</b>

•	The average Index of Multiple Deprivation (2015) score in the LSOAs where CCGs' registered patients lived in April 2019
•	The total population registered with CCGs' practices (April 2019)
•	% of population age 18 to 39 (April 2019)
•	% of population age 65 to 84 (April 2019)
•	% of population age 85+ (April 2019)
•	% of population who live in areas defined by the ONS Rural Urban Classification as "Rural town and fringe in a sparse setting", "Rural village and dispersed" or "Rural village and dispersed in a sparse setting" (April 2019)
•	The percentage of people who said they are of white (non-British) ethnic origin (GP Patient Surveys 2016, 2017 and 2018)
•	The percentage of people who said they are of Mixed ethnic origin (GP Patient Surveys 2016, 2017 and 2018)
•	The percentage of people who said they are of Asian ethnic origin (GP Patient Surveys 2016, 2017 and 2018)
•	The percentage of people who said they are of Black ethnic origin (GP Patient Surveys 2016, 2017 and 2018)
•	The percentage of people who said they are of Arab or Other ethnic origin (GP Patient Surveys 2016, 2017 and 2018)

These variables were weighted according to the methodology guide, and each CCG could then be treated as a 11- dimensional vector with these weighted variables as elements.
The closest 10 CCGs to a given CCG by euclidean distance in this phase space were the 10 most similar CCGs.
