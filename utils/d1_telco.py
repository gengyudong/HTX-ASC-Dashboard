import pandas as pd
from nicegui import ui

def telco_plot(telco_df):
    #   Data Processing
    telco_count_series = telco_df.groupby('telco').size()
    telco_name_list = telco_count_series.index.to_list()
    telco_count_list = telco_count_series.to_list()

    #   Chart
    chart = ui.chart({
            'title': {
                'text': 'Telco Line Termination',
                'margin': 50,
                'align': 'left',
                'style': {
                    'color': '#CED5DF',
                    'fontWeight': 'bold',
                    'fontFamily': 'Michroma'
                }
            },
            
            'chart': {
                'type': 'bar',
                'backgroundColor': 'rgba(0,0,0,0)',
            },
            
            'yAxis': {
                'title': {
                    'text': 'Value',
                    'style': {
                        'color': '#CED5DF',
                    }
                },
                'labels': {
                    'style': {
                        'color': '#CED5DF',
                    }
                },
                'gridLineDashStyle': 'dash',
            },
            
            'credits': { 'enabled': False },
            'xAxis': {
                'gridLineDashStyle': 'dash',
                'categories': telco_name_list,
                'labels': {
                    'style': {
                        'color': '#CED5DF',
                    }
                },
            },
            'series': [{'data': telco_count_list,
                    'dataLabels':{
                            'enabled': True
                    }
            }],
            
            'legend':{
                'enabled': False
            }
            
        }).classes('w-full h-64')

    return chart