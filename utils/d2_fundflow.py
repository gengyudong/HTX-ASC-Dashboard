from nicegui import ui
from utils.d2_fundflow_data import * 

def fund_flow_plot(connection):
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
                'data': fundflow_data(connection),
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
                'series':{
                    'bar': {
                        'color': '#db3eb1',
                    },
                    'allowPointSelect':True,   
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
