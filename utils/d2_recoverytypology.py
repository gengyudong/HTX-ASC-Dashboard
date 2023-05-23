from nicegui import ui
from utils.d2_recoverytypology_data import *

def recovery_by_typology_plot(connection):
    ###     Bar Chart
    scam_list, recovery_list = recovery_typology_data(connection)
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
                'max': 9,
                'tickLength': 0,
                'labels':{
                    'style': {
                        'color': '#CED5DF',
                              }
                },
                'scrollbar':{
                    'enabled':True,
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
                },
            },

            'tooltip':{
                'valueDecimals': 2,
                'valuePrefix': '$',
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
                            'format': '${point.y:,.2f}',
                            
            #                 'formatter':""" function () {
            #     return this.value + ' units';
            # }"""
            # cant figure out how to round this thing to M
            #might try using number formatter (formats all numbers not just data labels to millions)
                    }
                    
                    }],
        }, extras = ['stock']) 
    print(chart.options['series'])

    return chart


# from dotenv import load_dotenv
# load_dotenv(ui.env file)
# os.getenv(environmentname)