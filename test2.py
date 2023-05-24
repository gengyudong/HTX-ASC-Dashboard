from nicegui import ui
import pymysql
import pandas as pd

def chart(df_test):
    df_test2 = df_test['variable'].value_counts().reset_index()

    # rename columns
    df_test2.columns = ['variable', 'count']
    x_axis = df_test2['variable'].tolist()
    y_axis = df_test2['count'].tolist()
    
    chart = ui.chart({
        'chart': {
            'type': 'bar'
        },
        
        'xAxis': {
            'categories': x_axis,
            'title': {
                'text': 'null'
            },
            'gridLineWidth': 1,
            'lineWidth': 0
        },
        'yAxis': {
            'min': 0,
            'title': {
                'text': 'Population (millions)',
                'align': 'high'
            },
            'labels': {
                'overflow': 'justify'
            },
            'gridLineWidth': 0
        },
        'tooltip': {
            'valueSuffix': ' millions'
        },
        'plotOptions': {
            'bar': {
                'dataLabels': {
                    'enabled': 'true'
                },
                'groupPadding': 0.1
            }
        },
        'legend': {
            'layout': 'vertical',
            'align': 'right',
            'verticalAlign': 'top',
            'x': -40,
            'y': 80,
            'borderWidth': 1,
        },
        
        'series': [{
            'name': 'Year 1990',
            'data': y_axis
        }]
    })
    
    return chart