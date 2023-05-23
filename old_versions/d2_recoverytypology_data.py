import pandas as pd

def recovery_typology_data(df):
    #   Retrive data
    df = df[[ 'latest_balance_seized', 'amount_scammed', 'scam_type']].copy()
    
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

