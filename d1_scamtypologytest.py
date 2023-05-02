from nicegui import ui
import pandas as pd
from datetime import timedelta, timezone, date, datetime
import pymysql

# connection = pymysql.connect(host = '119.74.24.181', user = 'htx', password = 'Police123456', database = 'ASTRO')
# df = pd.read_sql_query("SELECT * FROM astro.scam_management_system", connection)

def scam_typology_plot(df):
    #   Preparing data for plot
    df_scam_type = df[['date_assigned', 'scam_type']].copy()
    df_scam_type = df_scam_type.dropna(subset=['date_assigned', 'scam_type'])
    df_scam_type['scam_type'] = df_scam_type['scam_type'].str.lower()
    df_scam_type['scam_type'] = df_scam_type['scam_type'].replace('loan scan', 'loan scam')
    df_scam_type['scam_type'] = df_scam_type['scam_type'].str.title()

    #   x-min & x-max date (Default viewport for graph)                       
    max_date = date.today()
    time = datetime.min.time()
    default_max_datetime = datetime.combine(max_date, time)
    default_max_xview = round(default_max_datetime.replace(tzinfo=timezone.utc).timestamp()) * 1000

    min_date = max_date - timedelta(days = 90)
    default_min_datetime = datetime.combine(min_date, time)
    default_min_xview = round(default_min_datetime.replace(tzinfo=timezone.utc).timestamp()) * 1000

    df_scam_type['date_assigned'] = pd.to_datetime(df_scam_type['date_assigned'])
    counts = df_scam_type.groupby(['scam_type', 'date_assigned']).size()
    df_scam_type = counts.reset_index(name='count')

    current_scam_name = df_scam_type['scam_type'][0]
    current_date = df_scam_type['date_assigned'][0]
    start_date = round(current_date.replace(tzinfo=timezone.utc).timestamp()) * 1000
    iteration_count = len(df_scam_type.index)
    series_list = []
    data_dict = {}
    data_list = []

    for i in range(iteration_count):
        if df_scam_type['scam_type'][i] == current_scam_name:
            
            while df_scam_type['date_assigned'][i] != current_date:
                current_date += timedelta(days = 1)
                data_list.append(0)

            data_list.append(df_scam_type['count'][i])
            current_date += timedelta(days = 1)
            
        else:
            data_dict['name'] = current_scam_name
            data_dict['data'] = data_list
            series_list.append(data_dict)
            data_list = []
            data_dict = {}
            
            current_scam_name = df_scam_type['scam_type'][i]
            current_date = df_scam_type['date_assigned'][i]
            data_list.append((df_scam_type['count'][i]))
            current_date += timedelta(days = 1)
            
            
    chart = ui.chart({
        'chart': {
            'type': 'spline',
            'backgroundColor': 'rgba(0,0,0,0)',
        },
        
        'title': {
            'text': 'Scam Typology Trend',
            'margin': 50,
            'align': 'left',
            'style': {
                'color': '#CED5DF',
                'fontWeight': 'bold',
                'fontFamily': 'Michroma'
            }
        },

        'credits': {
            'enabled': False
        },
        
        'yAxis': {
            'title': {
                'text': '',
                'style': {
                    'color': '#CED5DF',
                }
            },
            'labels': {
                'style': {
                    'color': '#CED5DF',
                }
            },
        },

        'xAxis': {
            'labels': {
                'style': {
                    'color': '#CED5DF',
                    'fontFamily': 'Michroma'
                }
            },
            'min': default_min_xview,
            'max': default_max_xview,
        },

        'legend': {
            'layout': 'vertical',
            'align': 'right',
            'verticalAlign': 'middle',
            'itemStyle': {
                'font': 'Michroma',
                'color': '#CED5DF'
            },
        },
        
        'rangeSelector': {
            'allButtonsEnabled': True,
                'buttons': [{
                    'type': 'month',
                    'count': 3,
                    'text': 'Day',
                    'dataGrouping': {
                        'forced': True,
                        'units': [['day', [1]]]
                    }
                }, {
                    'type': 'year',
                    'count': 1,
                    'text': 'Week',
                    'dataGrouping': {
                        'forced': True,
                        'units': [['week', [1]]]
                    }
                }, {
                    'type': 'all',
                    'text': 'Month',
                    'count': 1,
                    'dataGrouping': {
                        'forced': True,
                        'units': [['month', [1]]]
                    }
                }],
                'buttonTheme': {
                    'width': 60
                },
                'selected': 0
        },

        'plotOptions': {
            'series': {
                'label': {
                    'connectorAllowed': False
                },
                'pointStart': start_date,
                'pointInterval': 24 * 3600 * 1000,
                'dataGrouping': {
                    'approximation': 'sum'
                }
            }
        },

        'series': series_list,
    }, type = 'stockChart', extras = ['stock'])

    return chart

