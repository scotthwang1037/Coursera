#!/usr/bin/env python
# coding: utf-8

# # Import Data

# In[1]:


import csv
import pandas as pd
import numpy as np
import datetime

file = pd.read_csv("hourly_irish_weather.csv")
file.head()


# In[2]:


#Business Understanding: Is the rain difference from each region? By solving this question, the goverment is able to identify the most possible region that might suffer from drought and they can do some precautions in case of water shortage.
#Analytical Approach: Use coloumns date, county and rain, find the average rain each year, create a distribution, and then utilize T test to determine whether they are different.


# # Data Processing

# In[9]:


#drop the unnecessary columns
rain = file[['date', 'county', 'rain']]
rain['date'] = pd.to_datetime(rain['date'], format = '%Y-%m-%d %H:%M:%S')
rain.set_index('date',inplace=True)


# In[10]:


rain = pd.pivot_table(rain, values='rain', index=rain.index,
                    columns=['county'], aggfunc=np.sum)
rain = rain.groupby(rain.index.year).sum(skipna=True)


# In[11]:


result = rain.iloc[19:]


# # Plotting

# In[6]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors
import scipy.stats
get_ipython().run_line_magic('matplotlib', 'notebook')

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * data
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m-h, m+h


# In[24]:


plt.figure(figsize=(16,12))

plt.subplot(211)
for x in list(result.columns):
    sns.kdeplot(np.array(result[x]), label = '{}'.format(x))
    
plt.title('Rainfall in Ireland (2008-2017)')
plt.xlabel('Rainfall(mm)')
plt.legend();

cmap = plt.cm.RdBu_r
norm = matplotlib.colors.Normalize(vmin=1000, vmax=2000)

ci = []
mean = []
for x in list(result.columns):
    ci.append(mean_confidence_interval(result[x]))
    mean.append(result[x].mean())

y_r = [mean[i] - ci[i][1] for i in range(len(ci))]

plt.figure(figsize=(16,22))

plt.subplot(212)
plt.bar(range(len(mean)), mean, yerr=y_r, color=cmap(norm(mean)), alpha=1, align='center', edgecolor = "black", error_kw=dict(ecolor='black', lw=1.5, capsize=8, capthick=1.5))
plt.xticks(range(len(mean)), list(result.columns))
plt.title('Rainfall in Ireland(2008-2017)')
plt.xlabel('County')
plt.ylabel('Rainfall(mm)')


# # T Test

# In[26]:


from scipy.stats import ttest_ind
for x in list(result.columns):
    for y in list(result.columns):
        st, p = ttest_ind(np.array(result[x]), np.array(result[y]), nan_policy='omit')

        if p < 0.01:
            different = True
            print("The rainfall in {} is different from the rainfall in {}".format(x,y), p)
        else: 
            different = False
            print("The rainfall in {} is not different from the rainfall in {}".format(x,y), p)


# In[ ]:


#Co. Carlow, Cavan, Clare, Meath, Roscommon, Sligo, Tipperary, Westmeath, and Wexford has significant lower rainfall than other regions, which means it's highly possible that those county might face drought if there is no control of water usage.

