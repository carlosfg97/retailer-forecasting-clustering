import pandas as pd
import numpy as np


# ## Preparing the dataset for running the clustering model

# We need to run a clystering model in order to cluster similar stores together. The similarity will be based:
# 
# Number of Transactions of each store
# 
# % Sales generated by each store for each family of products


# Importing the datasets- Train, which contains the information of transactions for each store and item, and items, which
# contains the information of the items sold in all stores across Ecuador
# The train dataset contains 217 million rows, therefore it will take sometime to import the dataset

def dataprep():
        
    print('Starting Dataprep')

    df = pd.read_csv('docker_data/data/train.csv', nrows= 30_000_000) 

    # colnames = ['id','date','store_nbr','item_nbr','unit_sales','onpromotion']
    # df1 =  pd.read_csv('https://favorita-8d838.s3.amazonaws.com/train_2015-06-01_onwards.csv', header = None, names =colnames )
    # df2 =  pd.read_csv('https://favorita-8d838.s3.amazonaws.com/train_upto_2015-05-31.csv', header = None, names = colnames)
    # df = pd.concat( [df1, df2 ])
    
    items = pd.read_csv('docker_data/data/items.csv') 

    # items = pd.read_csv('https://favorita-8d838.s3.amazonaws.com/items.csv',
    #  names=['item_nbr', 'family', 'class', 'perishable'])

    df_with_items = pd.merge(df, items, on= 'item_nbr', how = 'inner')


    df_with_items['date']= pd.to_datetime(df_with_items['date'])

    # Calculating the total number of items sold for each store
    items_sold = df_with_items[df_with_items['unit_sales'] > 0].groupby('store_nbr')['unit_sales'].sum()
    # Resetting the index, which is the store number, as a column of the dataframe
    items_sold = items_sold.reset_index()
    # Renaming the unit_sales column to total_sales
    items_sold = items_sold.rename(columns = {'unit_sales':'total_sales'})

    # Calculating the total items sold for each store by family
    items_sold_by_family = df_with_items[df_with_items['unit_sales'] > 0].groupby(['store_nbr', 'family'])['unit_sales'].sum()
    # Resetting the columns in items_sold_by_family
    items_sold_by_family = items_sold_by_family.reset_index(level= ['store_nbr', 'family'])
    # Changing the name of unit_sales column to total_sales
    items_sold_by_family = items_sold_by_family.rename(columns= {'unit_sales': 'total_sales_family'})


    # Merging items_sold and items_sold_by_family in order to get all the information into a single dataframe and compute
    # the percentage share of each family in each store

    share_of_sales_by_fam = pd.merge(items_sold_by_family, 
                                    items_sold, 
                                    on= 'store_nbr', 
                                    how= 'inner')


    # Now calculating the share of sales of each family for each store
    share_of_sales_by_fam['sales_share_family'] = (
        share_of_sales_by_fam['total_sales_family'] / share_of_sales_by_fam['total_sales'])*100


    # Sorting the values in the above dataframe
    share_of_sales_by_fam = share_of_sales_by_fam.sort_values(['store_nbr', 'sales_share_family'], ascending= [True, False])


    # Grouping Grocery I and Grovery II as GROCERIES
    share_of_sales_by_fam.loc[
        (share_of_sales_by_fam['family'] == 'GROCERY I') | 
        (share_of_sales_by_fam['family'] == 'GROCERY II'), 'family'] = 'GROCERIES'


    # In[1186]:


    # Grouping Home and Kitchen I and Home and Kitchen II as HOME AND KITCHEN
    share_of_sales_by_fam.loc[
        (share_of_sales_by_fam['family'] == 'HOME AND KITCHEN I') | 
        (share_of_sales_by_fam['family'] == 'HOME AND KITCHEN II'), 'family'] = 'HOME AND KITCHEN'


    # In[1187]:


    # Calculating the sum of sales_share_family for each family
    total_family_share = share_of_sales_by_fam.groupby('family')['sales_share_family'].sum().sort_values(ascending= False)
    total_family_share = total_family_share.reset_index()


    # In[1188]:


    # Joining share_of_sales_by_fam and total_family_share
    share_of_sales_by_fam = pd.merge(share_of_sales_by_fam, 
                                    total_family_share, 
                                    on = 'family', 
                                    how = 'inner')


    # In[1189]:


    share_of_sales_by_fam = share_of_sales_by_fam.rename(
        columns = {'sales_share_family_x': 'sales_share_family', 
                'sales_share_family_y': 'total_family_share_across_stores'})


    # In[1190]:


    # Categorizing those families as 'Other' where the total_family_share_across_stores < 40%
    list_of_families = list(
        share_of_sales_by_fam[share_of_sales_by_fam['total_family_share_across_stores'] < 40]['family'].unique())

    # In[1191]:


    # In[1192]:


    # Removing the following families as they aren't sold at all stores, so if we include these 'OTHER' category would not be
    # representative for all the stores

    #list_of_families.remove('LADIESWEAR')
    #list_of_families.remove('LAWN AND GARDEN')
    #list_of_families.remove('BOOKS')
    #list_of_families.remove('BABY CARE')


    # In[1193]:


    # Adding 'EGGS' under 'OTHER' too, as the clustering model gives better results when we add 'EGGS' family to 'OTHER'
    list_of_families.append('EGGS')



    share_of_sales_by_fam.loc[share_of_sales_by_fam['family'].isin(list_of_families), 'family'] = 'OTHER'




    # Creating the final dataframe that will be used for clustering
    final_df = pd.pivot_table(share_of_sales_by_fam, 
                            values= 'sales_share_family', 
                            index= 'store_nbr', 
                            columns= ['family'], aggfunc = np.sum)
    # Resetting the index in order to add the store_nbr as column instead of having it as index
    final_df = final_df.reset_index()



    # Replacing the missing values with 0, as the missing values mean that those items are not sold in those stores
    final_df = final_df.fillna(0)

    final_df = pd.merge(final_df, items_sold, on = 'store_nbr', how = 'inner')
    final_df.to_csv('docker_data/data/clustering_df.csv')

    return None

if __name__ == '__main__':
    dataprep()