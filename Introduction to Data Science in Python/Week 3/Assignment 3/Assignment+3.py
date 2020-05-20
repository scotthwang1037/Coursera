
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.5** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# # Assignment 3 - More Pandas
# This assignment requires more individual learning then the last one did - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.

# ### Question 1 (20%)
# Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']`
# 
# Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
# 
# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, 
# 
# e.g. 
# 
# `'Bolivia (Plurinational State of)'` should be `'Bolivia'`, 
# 
# `'Switzerland17'` should be `'Switzerland'`.
# 
# <br>
# 
# Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# <br>
# 
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.
# 
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# 
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
# 
# *This function should return a DataFrame with 20 columns and 15 entries.*

# In[1]:


import pandas as pd
import re
import numpy as np
def Q1():
    energy=pd.read_excel("Energy Indicators.xls", names=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'], skiprows=17, skipfooter=38, parse_cols="C:F")
    energy["Energy Supply"][energy["Energy Supply"] == '...'] = np.NaN
    energy["Energy Supply per Capita"][energy["Energy Supply per Capita"] == '...'] = np.NaN
    dic = {
        "Republic of Korea": "South Korea",
        "United States of America": "United States",
        "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
        "China, Hong Kong Special Administrative Region": "Hong Kong"
    }  
    energy['Energy Supply'] = energy['Energy Supply']*10**6
    energy['Country'] = energy['Country'].str.replace(r"([0-9]+)$","")
    energy['Country'] = energy['Country'].str.replace(r" \(.*\)","")
    energy['Country'].replace(to_replace=dic,inplace=True)
    energy.set_index('Country',inplace=True)
    #Load the GDP data from the file world_bank.csv
    GDP = pd.read_csv('world_bank.csv', skiprows=4)
    replace_dict = {"Korea, Rep.": "South Korea", 
                    "Iran, Islamic Rep.": "Iran",
                    "Hong Kong SAR, China": "Hong Kong"
                   }
    GDP['Country Name'].replace(to_replace=replace_dict, inplace=True)
    GDP.drop(GDP.iloc[:, 3:50],axis=1,inplace=True)
    GDP.set_index('Country Name',inplace=True)
    ScimEn = pd.read_excel("scimagojr-3.xlsx", header=0)
    ScimEn.set_index('Country',inplace=True)
    first_merge = pd.merge(GDP, energy, how='inner', left_index=True, right_index=True)
    result = pd.merge(ScimEn, first_merge, how='inner', left_index=True, right_index=True)
    result = result.dropna(thresh=result.shape[1]-10)
    top = result.loc[result['Rank']<=15]
    return energy, GDP, ScimEn, result, top
Q1()


# ### Question 2 (6.6%)
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# 
# *This function should return a single number.*

# In[2]:


get_ipython().run_cell_magic('HTML', '', '<svg width="800" height="300">\n  <circle cx="150" cy="180" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="blue" />\n  <circle cx="200" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="red" />\n  <circle cx="100" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="green" />\n  <line x1="150" y1="125" x2="300" y2="150" stroke="black" stroke-width="2" fill="black" stroke-dasharray="5,3"/>\n  <text  x="300" y="165" font-family="Verdana" font-size="35">Everything but this!</text>\n</svg>')


# In[3]:


def Q2():
    energy, GDP, ScimEn, result, top = Q1()
    first_merge = pd.merge(GDP, energy, how='inner', left_index=True, right_index=True)
    second_merge = pd.merge(GDP, ScimEn, how='inner', left_index=True, right_index=True)
    third_merge = pd.merge(energy, ScimEn, how='inner', left_index=True, right_index=True)
    return energy.shape[0] + GDP.shape[0] + ScimEn.shape[0] - first_merge.shape[0] - second_merge.shape[0] - third_merge.shape[0] 
Q2()


# ## Answer the following questions in the context of only the top 15 countries by Scimagojr Rank (aka the DataFrame returned by `answer_one()`)

# ### Question 3 (6.6%)
# What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
# 
# *This function should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*

# In[4]:


def Q3():
    energy, GDP, ScimEn, result, top = Q1()
    avg = result.iloc[:,2:].mean(axis=1,skipna=True).sort_values(ascending=False)
    return avg
Q3()


# ### Question 4 (6.6%)
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
# 
# *This function should return a single number.*

# In[5]:


def Q4():
    energy, GDP, ScimEn, result, top = Q1()
    result['2006-2015'] = result['2015'] - result['2006']
    result1 = result.iloc[:,2:].mean(axis=1,skipna=True).sort_values(ascending=False)
    return result.loc[result1.index[5]]['2006-2015']
Q4()


# ### Question 5 (6.6%)
# What is the mean `Energy Supply per Capita`?
# 
# *This function should return a single number.*

# In[6]:


def Q5():
    energy, GDP, ScimEn, result, top = Q1()
    return top['Energy Supply per Capita'].mean(skipna=True)
Q5()


# ### Question 6 (6.6%)
# What country has the maximum % Renewable and what is the percentage?
# 
# *This function should return a tuple with the name of the country and the percentage.*

# In[7]:


def Q6():
    energy, GDP, ScimEn, result, top = Q1()
    return (top['% Renewable'].idxmax(axis=1), top['% Renewable'].max())
Q6()


# ### Question 7 (6.6%)
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 
# *This function should return a tuple with the name of the country and the ratio.*

# In[8]:


def Q7():
    energy, GDP, ScimEn, result, top = Q1()
    top['% Ratio of Self-citations'] = top['Self-citations'] / top['Citations']
    return (top['% Ratio of Self-citations'].idxmax(axis=1), top['% Ratio of Self-citations'].max())
Q7()


# ### Question 8 (6.6%)
# 
# Create a column that estimates the population using Energy Supply and Energy Supply per capita. 
# What is the third most populous country according to this estimate?
# 
# *This function should return a single string value.*

# In[9]:


def Q8():
    energy, GDP, ScimEn, result, top = Q1()
    top['PopEst'] = top['Energy Supply'] / top['Energy Supply per Capita']
    return top['PopEst'].sort_values(ascending=False).index[2]
Q8()


# ### Question 9 (6.6%)
# Create a column that estimates the number of citable documents per person. 
# What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the `.corr()` method, (Pearson's correlation).
# 
# *This function should return a single number.*
# 
# *(Optional: Use the built-in function `plot9()` to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)*

# In[10]:


def Q9():
    energy, GDP, ScimEn, result, top = Q1()
    top['Energy Supply'] = top['Energy Supply'].astype(float)
    top['Energy Supply per Capita'] = top['Energy Supply per Capita'].astype(float)
    top['PopEst'] = top['Energy Supply'] / top['Energy Supply per Capita']
    top['Citable docs per Capita'] = top['Citable documents'].astype(float) / top['PopEst']
    return top.corr(method='pearson')['Citable docs per Capita']['Energy Supply per Capita']
Q9()


# In[11]:


def plot9():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    
    energy, GDP, ScimEn, result, top = Q1()
    top['Energy Supply'] = top['Energy Supply'].astype(float)
    top['Energy Supply per Capita'] = top['Energy Supply per Capita'].astype(float)
    top['PopEst'] = top['Energy Supply'] / top['Energy Supply per Capita']
    top['Citable documents'] = top['Citable documents'].astype(float)
    top['Citable docs per Capita'] = top['Citable documents']/ top['PopEst']
    top.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter',xlim=[0,0.0006])
    
plot9()


# ### Question 10 (6.6%)
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
# 
# *This function should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*

# In[12]:


def Q10():
    energy, GDP, ScimEn, result, top = Q1()
    top['HighRenew'] = np.where(top['% Renewable'] >= top['% Renewable'].median(), 1, 0)
    return top.sort_values('Rank',ascending=True)['HighRenew']
Q10()


# ### Question 11 (6.6%)
# Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# 
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# 
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*

# In[13]:


def Q11():
    energy, GDP, ScimEn, result, top = Q1()
    top.rename(index={'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'},inplace = True)
    top['PopEst'] = top['Energy Supply'].astype(float) / top['Energy Supply per Capita'].astype(float)
    return top['PopEst'].groupby(level=0).agg({'size':np.count_nonzero, 'sum': np.nansum, 'mean': np.nanmean, 'std':np.std})
Q11()


# ### Question 12 (6.6%)
# Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
# 
# *This function should return a __Series__ with a MultiIndex of `Continent`, then the bins for `% Renewable`. Do not include groups with no countries.*

# In[15]:


def Q12():
    energy, GDP, ScimEn, result, top = Q1()
    top.rename(index={'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'},inplace = True)
    top['% Renewable'] = pd.cut(top['% Renewable'], 5)
    return top.groupby([top.index,'% Renewable'])['Rank'].count()
Q12()


# ### Question 13 (6.6%)
# Convert the Population Estimate series to a string with thousands separator (using commas). Do not round the results.
# 
# e.g. 317615384.61538464 -> 317,615,384.61538464
# 
# *This function should return a Series `PopEst` whose index is the country name and whose values are the population estimate string.*

# In[16]:


def Q13():
    energy, GDP, ScimEn, result, top = Q1()
    top['PopEst'] = top['Energy Supply'].astype(float) / top['Energy Supply per Capita'].astype(float)
    top['PopEst'] = top['PopEst'].apply('{:,}'.format)
    return top['PopEst']
Q13()


# ### Optional
# 
# Use the built in function `plot_optional()` to see an example visualization.

# In[18]:


def plot_optional():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    energy, GDP, ScimEn, result, top = Q1()
    ax = top.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*top['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(top.index):
        ax.annotate(txt, [top['Rank'][i], top['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries 2014 GDP, and the color corresponds to the continent.")


# In[19]:


plot_optional()

