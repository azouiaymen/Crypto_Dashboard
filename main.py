#!/usr/bin/env python
# coding: utf-8

# In[57]:


import streamlit as st
import datetime as dt
import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('sqlite:///CryptolIVE.DB')


# In[2]:


from sqlalchemy import inspect
inspector = inspect(engine)
# inspector.get_table_names()


# In[58]:


st.title('Welcome to Basic Crypto dashboard')


# In[5]:


symbols = pd.read_sql('SELECT name from sqlite_master where type = "table"',engine).name.to_list()


# In[17]:


lookback = st.selectbox('Pick the lookback in minutes', [1,15,30])


# In[28]:


def query_symb(symbol, lookback):
    now = dt.datetime.utcnow()
    before = now - dt.timedelta(minutes = lookback)
    #print(now,"*"*15,before)
    qur = f"""SELECT * from '{symbol}' WHERE time >= '{before}' """
    df = pd.read_sql(qur,engine)

    return df


# In[60]:


# query_symb('ethusdt',1)


# In[30]:


def return_calculus(sym,lookback):
    df = query_symb(sym,lookback)
    cum_ret = (df.PRICE.pct_change() + 1).prod() - 1
    return cum_ret


# In[31]:


return_calculus('ethusdt',10)


# In[32]:


def all_returned():
    returns = []
    for symb in symbols:
        returns.append(return_calculus(symb,lookback))
    return returns


# In[ ]:


if st.button('Update'):
    all_returned()


# In[41]:


all_return = pd.DataFrame(all_returned(),index=symbols,columns=['CHANGE'])


# In[53]:


top = all_return.CHANGE.nlargest(10)
bottom = all_return.CHANGE.nsmallest(10)

cols = st.columns(2)

cols[0].title('Top Performers')
cols[0].dataframe(top)
cols[1].title('Worst Performers')
cols[1].dataframe(bottom)
# st.write(top)
# st.write(bottom)

