#!/usr/bin/env python
# coding: utf-8

# # Project: Investigate the TMDB movie dataset

# ## Table of contents

# * [Introduction](#Introduction)
# * [Data Wrangling](#Data-Wrangling)
# * [Exploratory Data Analysis](#Exploratory_Data_Analysis)
# * [Conclusions](#Conclusion)
# 

# ## Introduction

# ### About TMDB
# In this notebook, I will investigate the TMDB mavie dataset. The Movie Database (TMDB) is a popular user editable database for movies and TV shows. It has columns for variables such as release year, revenue, budget, director, runtime, and popularity, as well as the IMDB ID for each entry.
# 
# ### Proposed Questions
# 
# 1-Which ten directors produce movies more frequently?
# 
# 2-How did each of the following variables evolve through the years?
# 
#   * Average movie popularity
#   
#   * Average movie rating
#   
#   * Average runtime
#   
#   * Average revenue
#   
#   * Total revenue for movies produced each year
#   
#   * Number of movies produced
#   
# 3-Which months of the year are more likely to produce more revenue?
# 
# 4-How is revenue affected by each of the following variables?
# 
#   * Budget
#   
#   * Popularity
#   
#   * Runtime
#   
#   * Vote count

# In[1]:


# Import required packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ## Data-Wrangling

# In[2]:


# import our data file into pandas Dataframe

df=pd.read_csv('tmdb-movies.csv')


# In[3]:


# checking for columns info and data types

df.info()


# In[4]:


df.head(1)


# In[5]:


df.tail(1)


# In[6]:


# checking for null values

df.isnull().sum()


# In[7]:


# checking for dupliactes

df.duplicated().any()


# In[8]:


df[df.duplicated()]


# #### Observation
# * The dataset contains 10,866 rows and 21 columns.
# * The column data types vary among ints, floats, and objects (i.e. strings).
# * There is a duplicated row in the dataset.
# * There are columns in the dataset that we don't need for this analysis. We can drop these columns.
# * The release_date column has a string data type. It will be more convenient to use it after converting to date-time format.

# ### Data Cleaning

# In[9]:


# Remove the duplicated row

df=df.drop(2090)


# In[10]:


# remove the 10 null value rows in the imdb_id column

df=df[df['imdb_id'].notna()]


# In[11]:


# checking for the result

df.isnull().sum()


# In[12]:


# Transforming date columns to datetime format

df['release_date']=pd.to_datetime(df['release_date'])
df['release_year']=pd.to_datetime(df['release_year'])


# In[13]:


df.head(1)


# In[14]:


# Creat two columns one for month name and one for year 

import calendar
df['month']=df['release_date'].dt.month
df['month']=df['month'].apply(lambda x:calendar.month_abbr[x])
df['year']=df['release_date'].dt.year


# In[15]:


df.head(1)


# In[16]:


# remove columns that are not needed to answer the questions

df.drop(['imdb_id', 'original_title', 'cast', 'homepage', 'tagline', 'keywords', 'overview', 'genres', 'production_companies'], axis=1, inplace=True)


# In[17]:


# Print final columns information

df.info()


# ## Exploratory_Data_Analysis

# ##### Now that the data is clean, let us start our investigation of the above questions.

# ### Research Question 1: Which ten directors produce movies more frequently?

# In[18]:


Directors=df['director'].value_counts(ascending=False).head(10)
print(Directors)


# In[19]:


colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
Directors.plot.bar(color=colors,figsize=(10,5),title='Top 10 directors');
plt.title('Top 10 Directors',size=18);
plt.xlabel('Directots',size=18);
plt.ylabel('Number of movies',size=18);


# Top 10 Directors:
#     
# 1. Woody Allen
# 2. Clint Eastwood       
# 3. Martin Scorsese      
# 4. Steven Spielberg    
# 5. Ridley Scott         
# 6. Steven Soderbergh    
# 7. Ron Howard           
# 8. Joel Schumacher      
# 9. Brian De Palma       
# 10. Barry Levinson       

# ### Research Question 2 : How did each of the following variables evolve through the years of 2005 to 2015?

# * Average movie popularity
# * Average movie rating
# * Average runtime
# * Average revenue
# * Total revenue for movies produced each year
# * Number of movies produced

# In[20]:


df_years=df.sort_values('year',ascending=True)
df_years.head(1)


# In[21]:


df2020=df[df['year'].between(2005,2015)]


# In[22]:


Average_popularity_change=df2020.groupby('year')['popularity'].mean()
Average_movie_rating=df2020.groupby('year')['vote_average'].mean()
Average_runtime=df2020.groupby('year')['runtime'].mean()
Total_revenue=df2020.groupby('year')['revenue'].sum()
movies_number=df2020.groupby('year')['id'].count()


# In[23]:


Average_popularity_change


# In[24]:


plt.figure(figsize=(10,5));
Average_popularity_change.plot.line('year','popularity');
plt.title('Year vs popularity',size=12);
plt.xlabel('Year',size=12);
plt.ylabel('Populrity',size=12);


# #### Popularity started at (0.628663) in 2005 and started to fluctuate along the years until it reached it's higher peak in 2015 with (1.032126)

# In[25]:


Average_movie_rating


# In[26]:


plt.figure(figsize=(10,5));
Average_movie_rating.plot.line('year','vote_average')
plt.title('Year vs vote_average',size=12);
plt.xlabel('Year',size=12);
plt.ylabel('vote_average',size=12);


# #### Vote avergae fluctuates over the years it increased from 2006 (5.866484) to 2010 (5.987500) to reach it's highest peack and reduced in 2012 (5.795392) to it's most decrease and it reached  stable area at 2015 (5.883121)

# In[27]:


Average_runtime


# In[28]:


plt.figure(figsize=(10,5));
Average_runtime.plot.line('year','runtime');
plt.title('Year vs runtime',size=12);
plt.xlabel('Year',size=12);
plt.ylabel('runtime',size=12);


# #### Runtime started with it's higher at 2006 from (102) min. and decreased until it reached it's lower in 2013 with (96.179331) min. and started to increase in 2014 (98.409156) min. but went back to decrease in 2015 (96.488854) min.

# In[29]:


Total_revenue


# In[30]:


round(1.651684e+10)


# In[31]:


round(2.676245e+10)


# In[32]:


plt.figure(figsize=(10,5));
Total_revenue.plot.line('year','revenue')
plt.title('Year vs revenue',size=12);
plt.xlabel('Year',size=12);
plt.ylabel('revenue',size=12);


# #### Revenue increased from 2005 (16516840000) up to reach it's peack in 2015 (26762450000)

# In[33]:


movies_number


# In[34]:


plt.figure(figsize=(10,5));
movies_number.plot.line('year','number of movies');
plt.title('Year vs number of movies',size=12);
plt.xlabel('Year',size=12);
plt.ylabel('number of movies',size=12);


# #### Number of movies increased from 2006 with (364) movies up to reaching 2014 (628) movies

# ### Research Question 3 : Which months of the year are more likely to produce more revenue?

# In[35]:


# Aggregate by month and revenue and sort by descending to get the maximum value per month

most_revenue_month=df.groupby('month')['revenue'].sum().sort_values(ascending=False).head(1)
print(most_revenue_month)


# In[36]:


# number rounded up to the next dull int.

round(6.166059e+10)


# In[37]:


months=df.groupby('month')['revenue'].sum().sort_values(ascending=False)
months.plot.bar('month','reveue',figsize=(10,5),color=colors,title='sum of revenues per months');
plt.title('Revenues per month',size=18);
plt.ylabel('Revenues',size=18);
plt.xlabel('Month',size=18);


# #### As per statistics and the bar chart , June is the most month to produce the maximum total revenue along the years with Total revenue of (61660590000)

# ### Research Question 4 : How is revenue affected by each of the following variables?

# 1. Budget
# 2. Popularity
# 3. Vote count

# In[38]:


df.head(1)


# In[39]:


plt.subplots(figsize=(10,6));
sns.regplot(x=df['budget'], y=df['revenue_adj'], color='g');
plt.title('Revenue by Budget',fontsize = 18);
plt.xlabel('Budget',fontsize = 16);
plt.ylabel("Revenue",fontsize = 16);


# #### Even though it seems that the revenue is increasing with budget on some level, it is clear that some of the most profitable movies had budgets lower than average

# In[40]:


plt.subplots(figsize=(10,6));
sns.regplot(x=df['popularity'], y=df['revenue_adj'], color='g');
plt.title('Revenue by popularity',fontsize = 18);
plt.xlabel('popularity',fontsize = 16);
plt.ylabel("Revenue",fontsize = 16);


# #### It seems that more popular movies produce more revenue. However, some popular movies are not necessarily profitable, and vice versa.

# In[41]:


plt.subplots(figsize=(10,6));
sns.regplot(x=df['vote_count'], y=df['revenue_adj'], color='g');
plt.title('Revenue by vote count',fontsize = 18);
plt.xlabel('Vote count',fontsize = 16);
plt.ylabel("Revenue",fontsize = 16);


# #### The above plot shows a strong correlation between vote count and revenue, which is intuitive. Sense more revenue means more viewers, it would mean potential voters for the movie.

# ## Conclusion
# 
# ### Findings
# 
# 1- Top 10 Directors:
# 
# 1- Woody Allen
# 2- Clint Eastwood
# 3- Martin Scorsese
# 4- Steven Spielberg
# 5- Ridley Scott
# 6- Steven Soderbergh
# 7- Ron Howard
# 8- Joel Schumacher
# 9- Brian De Palma
# 10- Barry Levinson
# 
# 2-  Popularity started at (0.628663) in 2005 and started to fluctuate along the years until it reached it's higher peak in 2015 with (1.032126).
# 
# 3- Vote avergae fluctuates over the years it increased from 2006 (5.866484) to 2010 (5.987500) to reach it's highest peack and reduced in 2012 (5.795392) to it's most decrease and it reached  stable area at 2015 (5.883121).
# 
# 4- Runtime started with it's higher at 2006 from (102) min. and decreased until it reached it's lower in 2013 with (96.179331) min. and started to increase in 2014 (98.409156) min. but went back to decrease in 2015 (96.488854) min.
# 
# 5- Revenue increased from 2005 (16516840000) up to reach it's peack in 2015 (26762450000).
# 
# 6- Number of movies increased from 2006 with (364) movies up to reaching 2014 (628) movies.
# 
# 7- As per statistics and the bar chart , June is the most month to produce the maximum total revenue along the years with Total revenue of (61660590000).
# 
# 8- Even though it seems that the revenue is increasing with budget on some level, it is clear that some of the most profitable movies had budgets lower than average.
# 
# 9- It seems that more popular movies produce more revenue. However, some popular movies are not necessarily profitable, and vice versa.
# 
# 10- The above plot shows a strong correlation between vote count and revenue, which is intuitive. Sense more revenue means more viewers, it would mean potential voters for the movie.
