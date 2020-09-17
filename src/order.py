import pandas as pd

from src.constants import OrderConfig

class OrderDataObject:
    '''
    Background Thinking:
    - created the function in the order that I thinking about the data that need to be displayed
    1. need to get the data into a format I could easily manipulate
    2. can see from comparing raw data to final table that sum distinct necessary
    3. found after that I need to do a uniquie count on member id column specifically 
    Realized couldn't just a a count column since not all columns have the same distinct count
    4. joined the dataframes to put data into one view and show the result
    '''

    def __init__(self):
        self.data_constants = OrderConfig()

    def get_data_to_dataframe(self,list_of_dict):
        '''
        Get data and add to dataframe a list of dictionaries
        '''
        df = pd.DataFrame.from_dict(list_of_dict)
        return df

    def groupby_sum_dataframe(self,df,groupby_list):
        '''
        Group specific data points coming from the list and sum up any float values
        '''
        df = df.groupby(by=groupby_list,as_index=False).sum()
        return df   

    def groupby_unique_dataframe(self,df,groupby_list,groupby_unique_value):
        '''
        Group specific data points coming from the list and count distint value based on a specified column
        '''
        df = df.groupby(by=groupby_list)[groupby_unique_value].nunique().reset_index()
        return df   
    
    def merge_dataframes(self, df1,df2,groupby_list):
        '''
        Merge two dataframes together
        '''
        df = df1.merge(df2, on=groupby_list)
        return df

    def rename_dataframe_columns(self, df,groupby_columns):
        '''
        Rename columns based on dictionary key value pairs
        '''
        df = df.rename(groupby_columns,axis='columns')
        return df

    def handle(self):
        '''
        Load data into dataframe and create group by to sum and count distinct certain values
        '''

        data = self.get_data_to_dataframe(self.data_constants.ORDERS)
        pivot_sum = self.groupby_sum_dataframe(data,self.data_constants.GROUPBY_LIST)
        pivot_unique = self.groupby_unique_dataframe(
            data,
            self.data_constants.GROUPBY_LIST,
            self.data_constants.GROUPBY_UNIQUE_VALUES
        )
        result = self.merge_dataframes(pivot_unique,pivot_sum,self.data_constants.GROUPBY_LIST)
        final = self.rename_dataframe_columns(result,self.data_constants.GROUPBY_COLUMNS)
        return final
   
    
    

