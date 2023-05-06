from nicegui import ui
from datetime import timedelta, datetime, timezone, date

def recovery_trend_plot(df):
    df_recovery_trend = df[['date_assigned', 'amount_scammed', 'latest_balance_seized']].copy()
    df_recovery_trend = df_recovery_trend.fillna(0)

    iteration_count = len(df_recovery_trend.index)
    dates = []
    amount_recovered_list = []
    amount_recovered_interim = 0

    start_date = df_recovery_trend['date_assigned'][0]
    time = datetime.min.time()
    start_datetime = datetime.combine(start_date, time)
    start_datetime = round(start_datetime.replace(tzinfo=timezone.utc).timestamp()) * 1000
    current_date = start_date
    end_date = df_recovery_trend['date_assigned'][iteration_count-1]

    max_date = date.today()
    time = datetime.min.time()
    default_max_datetime = datetime.combine(max_date, time)
    default_max_xview = round(default_max_datetime.replace(tzinfo=timezone.utc).timestamp()) * 1000

    min_date = max_date - timedelta(days = 90)
    default_min_datetime = datetime.combine(min_date, time)
    default_min_xview = round(default_min_datetime.replace(tzinfo=timezone.utc).timestamp()) * 1000

    while current_date != end_date:
        dates.append(current_date)
        current_date += timedelta(days = 1)
    dates.append(current_date)

    for x in dates:
        x = x.strftime('%Y-%m-%d')

    current_date = start_date

    for i in range(iteration_count):
        if df_recovery_trend['date_assigned'][i] == current_date:
            if df_recovery_trend['latest_balance_seized'][i] >= df_recovery_trend['amount_scammed'][i]:
                amount_recovered_interim += df_recovery_trend['amount_scammed'][i]
            else:
                amount_recovered_interim += df_recovery_trend['latest_balance_seized'][i]

        else:
            amount_recovered_interim /= 1000000
            amount_recovered_interim = round(amount_recovered_interim, 2)
            amount_recovered_list.append(amount_recovered_interim)
            amount_recovered_interim = 0
            current_date += timedelta(days = 1)
            
            while df_recovery_trend['date_assigned'][i] != current_date:
                amount_recovered_list.append(0)   
                current_date += timedelta(days = 1)
                
            if df_recovery_trend['latest_balance_seized'][i] >= df_recovery_trend['amount_scammed'][i]:
                amount_recovered_interim += df_recovery_trend['amount_scammed'][i]
            else:
                amount_recovered_interim += df_recovery_trend['latest_balance_seized'][i]
                
    amount_recovered_interim /= 1000000
    amount_recovered_interim = round(amount_recovered_interim, 2)
    amount_recovered_list.append(amount_recovered_interim)

    while current_date != max_date:
        amount_recovered_list.append(0)   
        current_date += timedelta(days = 1)
        
    amount_recovered_list.append(0)

    chart = ui.chart({
        'chart': {
            'type': 'column',
            'backgroundColor': 'rgba(0,0,0,0)',
        },
        
        'title': {
            'text': None,
            'margin': 20,
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
        
        'xAxis': {
            'crosshair': True,
            'min': default_min_xview,
            'max': default_max_xview,
            'labels': {
                'format': '{value:%e %b}',
                'style': {'color': '#CED5DF'}
            },
        },
        'yAxis': {
            'min': 0,
            'title': {
                'text': 'Amount Recovered ($ Million)',
                'style': {
                        'color': '#CED5DF'
                }
            },
            'labels': {
                'format': '${value}',
                'style': {
                'color': '#CED5DF'
                }
            },
            'gridLineDashStyle': 'dash'
        },
        
        'tooltip': {
            'headerFormat': '<span style="font-size:10px">{point.key}</span><table>',
            'pointFormat': '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>${point.y:.2f} Million</b></td></tr>',
            'footerFormat': '</table>',
            'shared': True,
            'useHTML': True
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
            'selected': 0
        },
        
        'navigator': {
            'enabled': False
        },
        
        'scrollbar': {
            'enabled': False
        },
        
        'plotOptions': {
            'series': {
                'dataLabels': {
                    'enabled': True,
                    'format': '{y:.2f}',
                    'style': {'color': '#CED5DF'}
                },
                'label': {
                    'connectorAllowed': False
                },
                'pointStart': start_datetime,
                'pointInterval': 24 * 3600 * 1000,
                'dataGrouping': {
                    'approximation': 'sum'
                }
            }
        },
        
        'series': [{
            'name': 'Amount Recovered', 
            'data': amount_recovered_list,
            'color': 'rgba(52, 181, 213, 0.7)'}] 
    }, type = 'stockChart', extras = ['stock'])

    return chart