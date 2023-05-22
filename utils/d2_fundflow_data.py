import pandas as pd
from dotenv import dotenv_values
import os
   
def fundflow_data(connection):
    #Variables -- put in later
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #depends on where .env file is 
    env_path = os.path.join(parent_dir, '.env')
    env_vars = dotenv_values(env_path)
    condition = env_vars['CONDITION']
    
    #CREATE QUERY
    query = "SELECT overseas_local, SUM(amount_scammed), SUM(amount_transcated), COUNT(*) FROM astro.scam_management_system"

    if condition not in  ['None', 'OVERSEAS_LOCAL'] :
        condition_value = env_vars[condition] 
        query += f" WHERE {condition} = '{condition_value}'"

    query += " group by overseas_local" 

    fundFlowDf = pd.read_sql_query(query, connection) #improve this to put the ? prevent SQL injection

    ###     Data Processing 
    fundFlowDf = fundFlowDf.dropna(subset=['overseas_local']).fillna(0)
    print(fundFlowDf)
    fundFlowDf = fundFlowDf.set_index('overseas_local')
    fundFlowSum = fundFlowDf['SUM(amount_scammed)']+fundFlowDf['SUM(amount_transcated)']
    
    fundFlowCount = fundFlowDf['COUNT(*)']
    
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