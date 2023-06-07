from nicegui import ui

def telco_plot_data(telco_df):
    #   Data Processing
    telco_count_series = telco_df.groupby('telco').size()
    telco_name_list = telco_count_series.index.to_list()
    telco_count_list = telco_count_series.to_list()
    
    return telco_name_list, telco_count_list

def telco_plot(telco_df):
    telco_name_list, telco_count_list = telco_plot_data(telco_df)
    
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
                     'color': 'rgba(52, 181, 213, 0.7)',
            }],
            
            'legend':{
                'enabled': False
            }
        }).classes('w-full h-64')

    return chart