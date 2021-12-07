#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd


# In[27]:


sales = pd.read_csv('C:\\Users\\Admin\\Desktop\\Data Wrangling Practise\\Data Wrangling Practise\\sales.csv')
prices = pd.read_csv('C:\\Users\\Admin\\Desktop\\Data Wrangling Practise\\Data Wrangling Practise\\prices.csv')
# sales.info()


# In[28]:


sales_update = sales.rename(columns ={'ordered_at':'date'})
sales_update.date = pd.to_datetime(sales_update.date)
sales_sort = sales_update.sort_values('date')
# sales_sort


# In[29]:


prices_update = prices.rename(columns ={'updated_at':'date'})
prices_update.date = pd.to_datetime(prices_update.date)
prices_sort = prices_update.sort_values('date')
# prices_sort


# In[30]:


prices_sort_old = prices_sort[['product_id','old_price','date']].rename(columns = {'old_price':'price'})
# prices_sort_old


# In[31]:


prices_sort_new = prices_sort[['product_id','new_price','date']].rename(columns = {'new_price':'price'})
# prices_sort_new


# In[32]:


sale_price = pd.merge_asof(sales_sort, prices_sort_new, on = 'date', by = 'product_id', direction = 'backward')
sale_price_new = sale_price.dropna()
# sale_price_new


# In[33]:


sale_price_na = sale_price.query('price != price')
sale_price_drop = sale_price_na.drop(columns=['price'])
# sale_price_drop


# In[34]:


sale_price_old = pd.merge_asof(sale_price_drop, prices_sort_old, on = 'date', by = 'product_id', direction = 'forward')
# sale_price_old


# In[35]:


sale_price = pd.concat([sale_price_new, sale_price_old], ignore_index = True)
sale_price['revenue'] = sale_price['quantity_ordered'] * sale_price['price']
sale_price


# In[36]:


revenue_by_product = sale_price.groupby('product_id')[['revenue']].sum().reset_index()
revenue_by_product

