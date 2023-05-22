import pandas as pd
from dotenv import dotenv_values
import os

def recovery_typology_data(connection):
    #Variables 
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #depends on where .env file is 
    env_path = os.path.join(parent_dir, '.env')
    env_vars = dotenv_values(env_path)
    condition = env_vars['CONDITION']
    print("CONDITION", condition)

    query = "SELECT latest_balance_seized, amount_scammed, scam_type FROM astro.scam_management_system"
    if condition not in ['None', 'SCAM_TYPE'] :
        condition_value = env_vars[condition] 
        query += f" WHERE {condition} = '{condition_value}'"
    
    print("QUERY: " + query)
    df = pd.read_sql_query(query, connection)

    ###   Data Processing
    #   settling typos
    df['scam_type'] = df['scam_type'].str.title()

    #   sum and grouping records by scam_type
    groupedDf = df.groupby('scam_type').sum()

    #   settling typos
    if 'Loan Scan' in df['scam_type']:
        groupedDf.loc['Loan Scam']+=groupedDf.loc['Loan Scan']
        groupedDf = groupedDf.drop(index = 'Loan Scan')

    groupedDf = groupedDf.rename(index={
        'Bank Phishing Sms Scam': 'Bank Phishing SMS Scam',
        'Bec Scam': 'BEC Scam',
        'Cois': 'COIS',
        'Fgps': 'FGPS',
        'Gois': 'GOIS',
        'Osss': 'OSSS',
        'Non-Bank Phishing Sms Scam': 'Non-Bank Phishing SMS Scam'})

    #   calculating recovery 
    groupedDf['recovery'] = None

    for scam in groupedDf.index:
        if groupedDf.at[scam,'latest_balance_seized'] >= groupedDf.at[scam,'amount_scammed']:
            groupedDf.at[scam, 'recovery'] = groupedDf.at[scam,'amount_scammed']
        else:
            groupedDf.at[scam, 'recovery'] = groupedDf.at[scam,'latest_balance_seized']

    groupedDf = groupedDf.sort_values(by = ['recovery'], ascending=False)  
    scam_list = groupedDf.index.to_list()
    recovery_list = groupedDf.loc[:,'recovery'].to_list()

    print('RECOVERY TYPOLOGY DATA OBTAINED')
    return scam_list, recovery_list

