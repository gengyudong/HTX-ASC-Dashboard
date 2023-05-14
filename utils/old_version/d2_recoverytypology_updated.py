import pandas as pd
from nicegui import ui

# def formatter(y):
#     return str(y/1000000)+'M'

def recovery_by_typology_plot(df):
    
    #   Retrive data
    df = df[[ 'latest_balance_seized', 'amount_scammed', 'scam_type']].copy()

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
            'chart': {
                'type': 'bar',
                'backgroundColor': 'rgba(0,0,0,0)'},
            
            'title': {
                'text': 'Recovery by typology',
                'margin': 20,
                'align': 'left',
                'style': {
                    'color': '#CED5DF',
                    'fontWeight': 'bold',
                    'fontFamily': 'Michroma'
                }
            },

            'xAxis': {
                'type': 'category',
                'categories': scam_list,
                'min': 0,
                'max': 4,
                'tickLength': 0,
                'labels':{
                    'style': {'color': '#CED5DF',
                            #   'font-size':'1.5vh',
                              }
                },
                'scrollbar':{
                'enabled':True,
                # 'barBorderRadius': 1,
                # 'rifleColor': None,
                # 'trackBackgroundColor': 'rgba(0,0,0,0)',
                # 'showFull':False, 
            },
            },
            'yAxis':{
                'title': {
                'text': 'Amount Recovered',
                'style': {
                        'color': '#CED5DF'
                    },
                },
                'labels': {
                    'style': {
                    'color': '#CED5DF',
                    },
                },
                'gridLineDashStyle': 'dash',
                
            },
            
            'plotOptions': {
                'bar': {
                    'dataLabels': {
                        'enabled': 'true',
                        'style': {'color': '#CED5DF'},
                    },
                    'borderWidth':0,
                }
            },
            'legend': {
                'enabled': 'false'
            },
            'credits': {
                'enabled': 'false'
            },

            'series': [{'name': 'Recovered',
                        'data': recovery_list,
                        # 'color': 'rgba(52, 181, 213, 0.7)',
                    'dataLabels':{
                            'enabled': True,
            #                 'formatter':""" function () {
            #     return this.value + ' units';
            # }"""
            # cant figure out how to round this thing to M
            #might try using number formatter (formats all numbers not just data labels to millions)
                    }
                    
                    }],

            # 'numberFormatter':round(arguments)  
            
            'legend':{
                'enabled': False
            },

            'credits': {
                'enabled': False
            },
        }, extras = ['stock']) 

    return chart