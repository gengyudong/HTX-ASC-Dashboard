from nicegui import ui
import pandas as pd
   
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

def fund_flow_plot(df):
    chart = ui.chart({
            'chart': {'type': 'bar',
                      'backgroundColor': 'rgba(0,0,0,0)',
                      'zoomType': 'y',
            },
            
            'title': {
                'text': 'Breakdown of Fund Flow',
                'margin': 20,
                'align': 'left',
                'style': {
                    'color': '#CED5DF',
                    'fontWeight': 'bold',
                    'fontFamily': 'Michroma',
                }
            },
            
            'xAxis': {
                'type': 'category',
                'categories': ['L-L', 'L-O', 'O-L', 'O-O'],
                'labels':{
                    'style': {'color': '#CED5DF'},
                },
            },

            
            'yAxis':{
                'title': {
                    'text': 'Amount of Funds',
                    'style': {
                        'color': '#CED5DF'
                    },
                },
                'labels':{
                            'style': {'color': '#CED5DF'}
                        },
                'gridLineDashStyle': 'dash',
            },


            'series': [{
                'name': 'Funds',
                'data': fundflow_data(df),
                'dataLabels':{
                    'enabled': True,
                    'style': {'color': '#CED5DF'},
                    'format': '${point.y:,.2f}',
                },
                'borderWidth':0,
                'dataGrouping': False,

                    }],

            'tooltip':{
                'useHTML': True,
                'headerFormat': '<table><tr><th>{point.key}</th></tr>',
                'pointFormat': '<tr><td>Amount of Funds: {point.y}</td></tr>' +
                    '<tr><td>Number of Cases: {point.count}</td></tr>',
                'footerFormat': '</table>',
                'valueDecimals': 2,
                'valuePrefix': '$',
            },

            'plotOptions':{
                'bar': {
                    'color': '#db3eb1',
                }, 

            },

            'legend':{
                'enabled': False,
            },
            'credits': {
                'enabled': False,
            },
        }).classes('w-full h-64')
    
    return chart
