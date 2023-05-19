from nicegui import ui

def telco_plot(telco_df):
    #   Data Processing
    telco_count_series = telco_df.groupby('telco').size()
    telco_name_list = telco_count_series.index.to_list()
    telco_count_list = telco_count_series.to_list()

    #   Chart
    chart = ui.chart({
            'chart': {
                'type': 'bar',
                'zoomType': 'xy',
                'backgroundColor': 'rgba(0,0,0,0)',
            },
            
            'title': {
                'text': ''
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
                    'style': {'color': '#CED5DF'}
                },
            },
            'series': [{'data': telco_count_list,
                    'dataLabels':{
                            'enabled': True
                    },
                    'color': {
                        'linearGradient': {
                            'x1': 0,
                            'x2': 0,
                            'y1': 0,
                            'y2': 1
                        },
                        'stops': [
                            [0, '#8F3EFC'],
                            [1, '#22D1FE']
                        ]
                    }
            }],
            
            'legend':{
                'enabled': False
            }
            
        }).classes('w-full h-64')

    return chart