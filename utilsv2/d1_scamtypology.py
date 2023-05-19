from nicegui import ui
import pandas as pd
from datetime import timedelta, timezone, date, datetime

def scam_typology_plot(df):
    #   Getting data for top 10 scam types (Same code as d1_topscamtypes.py)
    df_scam_type_interim = df[['scam_type', 'amount_scammed']].copy()
    df_scam_type_interim['scam_type'] = df_scam_type_interim['scam_type'].str.lower()
    df_scam_type_interim['scam_type'] = df_scam_type_interim['scam_type'].replace('loan scan', 'loan scam')

    df_scam_type_interim = df_scam_type_interim.groupby('scam_type').agg({'scam_type': 'count', 'amount_scammed': 'sum'})
    df_scam_type_interim.columns = ['num_reports', 'total_amount_scammed']
    df_scam_type_interim = df_scam_type_interim.rename_axis('scam_type').reset_index()
    df_scam_type_interim['scam_type'] = df_scam_type_interim['scam_type'].str.title()
    df_scam_type_interim['scam_type'] = df_scam_type_interim['scam_type'].replace({
        'Bank Phishing Sms Scam': 'Bank Phishing SMS Scam',
        'Bec Scam': 'BEC Scam',
        'Cois': 'COIS',
        'Fgps': 'FGPS',
        'Gois': 'GOIS',
        'Osss': 'OSSS',
        'Non-Bank Phishing Sms Scam': 'Non-Bank Phishing SMS Scam'})
    
    df_scam_type_interim = df_scam_type_interim.sort_values(by = 'num_reports', ascending = False)
    top_scam_type_list = df_scam_type_interim.iloc[0:10]['scam_type'].values.tolist()


    #   Data Cleaning
    df_scam_type = df[['date_assigned', 'scam_type']].copy()
    df_scam_type = df_scam_type.dropna(subset=['date_assigned', 'scam_type'])
    df_scam_type['scam_type'] = df_scam_type['scam_type'].str.lower()
    df_scam_type['scam_type'] = df_scam_type['scam_type'].replace('loan scan', 'loan scam')
    df_scam_type['scam_type'] = df_scam_type['scam_type'].str.title()
    df_scam_type['scam_type'] = df_scam_type['scam_type'].replace({
        'Bank Phishing Sms Scam': 'Bank Phishing SMS Scam',
        'Bec Scam': 'BEC Scam',
        'Cois': 'COIS',
        'Fgps': 'FGPS',
        'Gois': 'GOIS',
        'Osss': 'OSSS',
        'Non-Bank Phishing Sms Scam': 'Non-Bank Phishing SMS Scam'})

    df_scam_type = df_scam_type[df_scam_type["scam_type"].isin(top_scam_type_list)].reset_index()

    #   Group data according to scam type & date
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
                         
    max_date = date.today()

    #   Populating y-axis data
    for i in range(iteration_count):
        if df_scam_type['scam_type'][i] == current_scam_name:
            
            while df_scam_type['date_assigned'][i] != current_date:
                current_date += timedelta(days = 1)
                data_list.append(0)

            data_list.append(df_scam_type['count'][i])
            current_date += timedelta(days = 1)
            
        if i == (iteration_count - 1):
            data_dict['name'] = current_scam_name
            data_dict['data'] = data_list
            series_list.append(data_dict)
                
        if df_scam_type['scam_type'][i] != current_scam_name:
            while current_date != max_date:
                data_list.append(0)   
                current_date += timedelta(days = 1)
            
                if current_date == max_date:
                    data_list.append(0)
    
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
            'zoomType': 'x',
            'backgroundColor': 'rgba(0,0,0,0)',
        },
        
        'title': {
            'text': ''
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
            'gridLineDashStyle': 'dash',
        },

        'xAxis': {
            'labels': {
                'format': '{value:%e %b}',
                'style': {'color': '#CED5DF'}
            }
        },

        'legend': {
            'enabled': True,
            'layout': 'vertical',
            'align': 'right',
            'verticalAlign': 'middle',
            'itemStyle': {
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
                'inputStyle': {
                    'color': '#CED5DF'
                },
                'selected': 0,
        },
        
        'navigator': {
            'enabled': True
        },
        
        'scrollbar': {
            'enabled': False
        },

        'tooltip': {
            'headerFormat': '<span style="font-size:10px">{point.key}</span><table>',
            'pointFormat': '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y}</b></td></tr>',
            'footerFormat': '</table>',
            'shared': True,
            'split': False,
            'useHTML': True
        },

        'plotOptions': {
            'series': {
                'dataLabels': {'enabled': True},
                'label': {'connectorAllowed': False},
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