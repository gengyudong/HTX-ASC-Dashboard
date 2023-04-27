import pymysql
import pandas as pd
from nicegui import ui

connection = pymysql.connect(host = '119.74.24.181', user = 'htx', password = 'Police123456', database = 'ASTRO')

#   Retrive data
df = pd.read_sql_query("""SELECT latest_balance_seized, amount_scammed, scam_type
FROM scam_management_system order by scam_type asc""", connection)

###   Data Processing

#   settling typos
df['scam_type'] = df['scam_type'].str.title()

#   sum and grouping records by scam_type
groupedDf = df.groupby('scam_type').sum()

#   settling typos
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

scam_list = groupedDf.index.to_list()
recovery_list = groupedDf.loc[:,'recovery'].to_list()


###     Bar Chart
chart = ui.chart({
        'title': {
            'enabled': True,
            'text': 'Recovery by Typology',
        },
        'chart': {'type': 'bar'},

        'xAxis': {
            'type': 'category',
            'categories': scam_list,
            # 'title': {
            #     'text': 'null'
            # # },
            'min': 0,
            'max': 4,
            'scrollbar': {
                'enabled': 'true'
            },
            'tickLength': 0
        },

        'series': [{'name': 'Recovered',
                    'data': recovery_list,
                   'dataLabels':{
                        'enabled': True,
                        #how to format it to millions? 
        #                 'formatter': function(){
        #     return this.value / 1000000 + 'M';
        # }
                   }
                   
                   }],
        
            
        
        'legend':{
            'enabled': False
        }
    }, type = 'stockChart', extras = ['stock'])



ui.run()
