#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib


# In[2]:


df1 = pd.read_csv('temp_datalab_records_social_facebook.csv')


# In[3]:


df1.head(3)


# Change time to pandas date time format

# In[4]:


df1['date_updated_dt'] = pd.to_datetime(df1.date_updated)
df1['time_dt'] = pd.to_datetime(df1.time)


# In[5]:


df1.columns


# In[6]:


df1.shape


# Now looking at the username and facebook_id, because number of facebook_id is less than the number of username

# In[7]:


usernames_unique = df1.username.unique()
usernames_unique.shape


# In[8]:


usernames_unique[:10]


# In[9]:


facebook_ids_unique = df1.facebook_id.unique()
facebook_ids_unique.shape


# get the usernames that has the same facebook_id, it turns out that some companies use more than two username, so when grouping we should use facebook_id other than username

# In[10]:


df1_group_level1 = df1[['username', 'facebook_id']].groupby(['username', 'facebook_id']).count().reset_index(drop=False)
df1_group_level2 = df1_group_level1.groupby(['facebook_id']).count()


# In[11]:


df1_group_level2[df1_group_level2['username'] >= 2].index


# Insanity check: none of the companies used more than two different facebook_id

# In[12]:


df1_group_level2_reverse = df1_group_level1.groupby(['username']).count()


# In[13]:


df1_group_level2_reverse[df1_group_level2_reverse['facebook_id'] >= 2].index


# In[14]:


df1_group_level1[df1_group_level1['facebook_id'] == df1_group_level2[df1_group_level2['username'] >= 2].index[334]]


# column 'has_added_app' is useless, because it's the same value through and through

# In[15]:


df1.has_added_app.unique()


# the columns 'entity_id', 'cusip', 'isin' are empty columns

# In[16]:


df1[['entity_id']].dropna()


# In[17]:


df1[['cusip']].dropna()


# In[18]:


df1[['isin']].dropna()


# The useful columns are checkins, were_here_count, likes, talking_about_count

# In[19]:


fig, axes = plt.subplots(1, 4, figsize=(15, 3))

comp_name = 'GSK'
axes[0].plot(df1[df1['username'] == comp_name].reset_index(drop=True).checkins)
axes[0].set_title('checkins')
axes[1].plot(df1[df1['username'] == comp_name].reset_index(drop=True).were_here_count)
axes[0].set_title('were_here_count')
axes[2].plot(df1[df1['username'] == comp_name].reset_index(drop=True).likes)
axes[0].set_title('likes')
axes[3].plot(df1[df1['username'] == comp_name].reset_index(drop=True).talking_about_count)
axes[0].set_title('talking_about_count')


# # Analysis of likes

# In[20]:


df1_likes_grouped = df1[['facebook_id', 'likes']].groupby(['facebook_id']).agg(lambda x: x.max() - x.min()).reset_index()


# In[21]:


df1_likes_grouped.sort_values(by='likes', ascending=False).head(10)


# In[22]:


# get top ten liked facebook id
top_10_facebookids = df1_likes_grouped.sort_values(by='likes', ascending=False).head(10).facebook_id
top_10_facebookids


# In[23]:


top_10_likes_complex = df1_group_level1[df1_group_level1['facebook_id'].isin(top_10_facebookids)]     .merge(df1_likes_grouped, 
           how='left', on='facebook_id') \
    .sort_values(by='likes', ascending=False).reset_index(drop=True)
top_10_likes_complex


# In[24]:


df1.loc[df1['facebook_id'] == top_10_likes_complex.loc[0, 'facebook_id']].head(1)


# In[25]:


df1.loc[df1['facebook_id'] == top_10_likes_complex.loc[0, 'facebook_id'], ['talking_about_count', 'date_updated']].plot(x='date_updated', y='talking_about_count')
plt.xticks(rotation=45)


# ## Facebook Analysis

# In[26]:


ranking = 0
df1.loc[df1['facebook_id'] == top_10_likes_complex.loc[ranking, 'facebook_id'],
        ['talking_about_count', 'date_updated_dt']]\
    .groupby(pd.Grouper(key='date_updated_dt', freq='D')).mean().plot()
plt.legend(loc='upper right')
plt.title(top_10_likes_complex.loc[ranking, 'username'])


# In[27]:


fb_averaged = df1.loc[df1['facebook_id'] == top_10_likes_complex.loc[ranking, 'facebook_id'],
        ['talking_about_count', 'date_updated_dt']]\
    .groupby(pd.Grouper(key='date_updated_dt', freq='D')).mean().reset_index()


# In[28]:


start_date = pd.to_datetime('2017-06-01 00:00:00+00')
end_date = pd.to_datetime('2017-07-01 00:00:00+00')
fb_averaged[(fb_averaged['date_updated_dt'] > start_date) 
            & (fb_averaged['date_updated_dt'] <= end_date)]\
    .plot(x='date_updated_dt', y='talking_about_count')


# In[29]:


start_date = pd.to_datetime('2017-06-15 00:00:00+00')
end_date = pd.to_datetime('2017-06-25 00:00:00+00')
fb_averaged[(fb_averaged['date_updated_dt'] > start_date) & (fb_averaged['date_updated_dt'] <= end_date)]


# In[30]:


start_date = pd.to_datetime('2017-06-12 00:00:00+00')
end_date = pd.to_datetime('2017-06-25 00:00:00+00')
fb_averaged[(fb_averaged['date_updated_dt'] > start_date) 
            & (fb_averaged['date_updated_dt'] <= end_date)]\
    .plot(x='date_updated_dt', y='talking_about_count')


# In[31]:


start_date = pd.to_datetime('2017-12-15 00:00:00+00')
end_date = pd.to_datetime('2018-01-25 00:00:00+00')
fb_averaged[(fb_averaged['date_updated_dt'] > start_date) 
            & (fb_averaged['date_updated_dt'] <= end_date)]\
    .plot(x='date_updated_dt', y='talking_about_count')


# In[32]:


start_date = pd.to_datetime('2017-12-28 00:00:00+00')
end_date = pd.to_datetime('2018-01-08 00:00:00+00')
fb_averaged[(fb_averaged['date_updated_dt'] > start_date) 
            & (fb_averaged['date_updated_dt'] <= end_date)]\
    .plot(x='date_updated_dt', y='talking_about_count')


# In[33]:


fig, axes = plt.subplots(3, 1, figsize=(8, 10))
fig.suptitle('Facebook Talking About Counts', fontsize=24)

ranking = 0
t1 = df1.loc[df1['facebook_id'] == top_10_likes_complex.loc[ranking, 'facebook_id'],
        ['talking_about_count', 'date_updated_dt']]\
    .groupby(pd.Grouper(key='date_updated_dt', freq='D')).mean().reset_index()
axes[0].plot(t1['date_updated_dt'], t1['talking_about_count'])
axes[0].plot([pd.to_datetime('2017-06-22 00:00:00+00'), pd.to_datetime('2017-06-22 00:00:00+00')], [0, 2200000], '-.')
axes[0].plot([pd.to_datetime('2018-01-02 00:00:00+00'), pd.to_datetime('2018-01-02 00:00:00+00')], [0, 2200000], '-.')

start_date = pd.to_datetime('2017-06-01 00:00:00+00')
end_date = pd.to_datetime('2017-07-01 00:00:00+00')
t2 = fb_averaged[(fb_averaged['date_updated_dt'] > start_date) 
                 & (fb_averaged['date_updated_dt'] <= end_date)]
axes[1].plot(t2['date_updated_dt'], t2['talking_about_count'])
axes[1].text(pd.to_datetime('2017-06-22 00:00:00+00'), 1900000, 'First-ever Facebook \nCommunities Summit\nOn June 22nd')
axes[1].plot([pd.to_datetime('2017-06-22 00:00:00+00'), pd.to_datetime('2017-06-22 00:00:00+00')], [0, 2200000], '-.')
plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=15)

start_date = pd.to_datetime('2017-12-28 00:00:00+00')
end_date = pd.to_datetime('2018-01-08 00:00:00+00')
t3 = fb_averaged[(fb_averaged['date_updated_dt'] > start_date) 
                 & (fb_averaged['date_updated_dt'] <= end_date)]
axes[2].plot(t3['date_updated_dt'], t3['talking_about_count'])
axes[2].text(pd.to_datetime('2018-01-02 00:00:00+00'), 1500000, 'Announce Fourth Quarter\n and Full Year 2017 Results\nOn Jan 2nd')
axes[2].plot([pd.to_datetime('2018-01-02 00:00:00+00'), pd.to_datetime('2018-01-02 00:00:00+00')], [0, 2200000], '-.g')
plt.setp(axes[2].xaxis.get_majorticklabels(), rotation=15)


# ## Netflix Analysis

# In[34]:


ranking = 1
df1.loc[df1['facebook_id'] == top_10_likes_complex.loc[ranking, 'facebook_id'],
        ['talking_about_count', 'date_updated_dt']]\
    .groupby(pd.Grouper(key='date_updated_dt', freq='D')).mean().plot()
plt.legend(loc='upper right')
plt.title(top_10_likes_complex.loc[ranking, 'username'])


# ## Orange Analysis

# In[35]:


ranking = 2
df1.loc[df1['facebook_id'] == top_10_likes_complex.loc[ranking, 'facebook_id'],
        ['talking_about_count', 'date_updated_dt']]\
    .groupby(pd.Grouper(key='date_updated_dt', freq='D')).mean().plot()
plt.legend(loc='upper right')
plt.title(top_10_likes_complex.loc[ranking, 'username'])


# ## McDonalds Analysis

# In[36]:


ranking = 3
df1.loc[df1['facebook_id'] == top_10_likes_complex.loc[ranking, 'facebook_id'],
        ['talking_about_count', 'date_updated_dt']]\
    .groupby(pd.Grouper(key='date_updated_dt', freq='D')).mean().plot()
plt.legend(loc='upper right')
plt.title(top_10_likes_complex.loc[ranking, 'username'])


# In[37]:


ranking = 4
df1.loc[df1['facebook_id'] == top_10_likes_complex.loc[ranking, 'facebook_id'],
        ['talking_about_count', 'date_updated_dt']]\
    .groupby(pd.Grouper(key='date_updated_dt', freq='D')).mean().plot()
plt.legend(loc='upper right')
plt.title(top_10_likes_complex.loc[ranking, 'username'])


# # Checkins analysis

# In[38]:


df1_checkins_grouped = df1[['facebook_id', 'checkins']].groupby(['facebook_id']).agg(lambda x: x.max() - x.min()).reset_index()


# In[39]:


df1_checkins_grouped.sort_values(by='checkins', ascending=False).head(10)


# In[40]:


# top 20 checked in companies
top_10_checkedin_facebookids = df1_checkins_grouped.sort_values(by='checkins', ascending=False).head(20).facebook_id
top_10_checkedin_facebookids


# In[41]:


top_20_checkins_complex = df1_group_level1[df1_group_level1['facebook_id'].isin(top_10_checkedin_facebookids)]     .merge(df1_checkins_grouped, 
           how='inner', on='facebook_id') \
    .sort_values(by='checkins', ascending=False).reset_index(drop=True)\
    .drop_duplicates(subset ="facebook_id").reset_index(drop=True)
top_20_checkins_complex


# In[42]:


fig, ax = plt.subplots(1, 1, figsize=(15, 5))
color = ['blue' for i in range(20)]
for i in [0, 5, 13]:
    color[i] = 'cyan'
ax.bar(top_20_checkins_complex['username'], top_20_checkins_complex['checkins'], color=color)
plt.xticks(rotation=90, fontsize=15)
plt.yticks(fontsize=15)
plt.title('Top 20 Companies to Attract Tourists to Physical Locations', fontsize=20)
plt.text(10, 2500000, 'Disney has 3 sites in top 20 tourist sites', fontsize=15)


# In[ ]:




