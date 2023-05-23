import pandas as pd
from dotenv import dotenv_values
import os
   
def fundflow_data(df):
     ###     Data Processing 
    fundFlowDf = df[['overseas_local', 'amount_scammed', 'amount_transcated']].copy()
    fundFlowSum = fundFlowDf.groupby('overseas_local').sum().round(2)
    fundFlowCount = fundFlowDf.groupby('overseas_local').size()
    fundFlowSum = fundFlowSum['amount_scammed']+fundFlowSum['amount_transcated']

    #   data cleaning
    if 'L-l' in fundFlowSum.index:
        fundFlowSum['L-L']+=fundFlowSum['L-l']
        fundFlowSum = fundFlowSum.drop('L-l')

        fundFlowCount['L-L']+=fundFlowCount['L-l']
        fundFlowCount = fundFlowCount.drop('L-l')
    
    #   convert to list and add fullName 
    fullName = pd.Series({'L-L':'Local-Local', 'L-O':'Local-Overseas', 'O-L':'Overseas-Local', 'O-O':'Overseas-Overseas'})
    to_display_df = pd.concat([fullName, fundFlowSum, fundFlowCount], axis = 1)
    to_display_df.columns = ['name','y', 'count']
    results = to_display_df.to_dict(orient="records")

    return results