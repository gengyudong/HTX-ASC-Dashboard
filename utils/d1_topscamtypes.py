from nicegui import ui

def top_scam_types_plot(df):  
    #   Data Cleaning
    df_scam_type = df[['scam_type', 'amount_scammed']].copy()
    df_scam_type['scam_type'] = df_scam_type['scam_type'].str.lower()
    df_scam_type['scam_type'] = df_scam_type['scam_type'].replace('loan scan', 'loan scam')

    #   Group data according to scam type & the amount scammed for the respective scam types
    df_scam_type = df_scam_type.groupby('scam_type').agg({'scam_type': 'count', 'amount_scammed': 'sum'})
    df_scam_type.columns = ['num_reports', 'total_amount_scammed']
    df_scam_type = df_scam_type.rename_axis('scam_type').reset_index()
    df_scam_type['scam_type'] = df_scam_type['scam_type'].str.title()
    df_scam_type = df_scam_type.rename(index = {
        'Bank Phishing Sms Scam': 'Bank Phishing SMS Scam',
        'Bec Scam': 'BEC Scam',
        'Cois': 'COIS',
        'Fgps': 'FGPS',
        'Gois': 'GOIS',
        'Osss': 'OSSS',
        'Non-Bank Phishing Sms Scam': 'Non-Bank Phishing SMS Scam'})

    #   Sort the scam types according to their no. of reports, in descending order
    df_scam_type = df_scam_type.sort_values(by = 'num_reports', ascending = False)

    df_scam_type['total_amount_scammed'] = df_scam_type['total_amount_scammed'] / 1000000

    #   Converting the top 10 scam types to a list 
    top_scam_type_list = df_scam_type.iloc[0:10]['scam_type'].values.tolist()
    top_scam_type_num_report = df_scam_type.iloc[0:10]['num_reports'].values.tolist()
    top_scam_total_amount_scammed_per_type = df_scam_type.iloc[0:10]['total_amount_scammed'].values.tolist()
    for i in range(len(top_scam_total_amount_scammed_per_type)):
        top_scam_total_amount_scammed_per_type[i] = round(top_scam_total_amount_scammed_per_type[i], 1)


    top_scam_types_plot = ui.chart({
        'chart': {
            'zoomType': 'xy',
            'backgroundColor': 'rgba(0,0,0,0)',
        },
        
        'title': {
            'text': 'Scam Typologies (Top 10)',
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
            'categories': top_scam_type_list,
            'crosshair': True,
            'labels': {
                'style': {
                    'color': '#CED5DF',
                    'autoRotationLimit': 40, 
                }
            },
        },
        
        'yAxis': [
            { # Primary yAxis
            'labels': {
                'format': '{value}',
                'style': {
                    'color': '#CED5DF',
                }
            },
            'title': {
                'text': 'Count of Scam Type',
                'style': {
                    'color': '#CED5DF',
                }
            },
            'gridLineDashStyle': 'dash'

        }, { # Secondary yAxis
            'title': {
                'text': 'Amount Scammed ($ Million)',
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
            'opposite': True,
            'gridLineColor': '#8397AF',
            'gridLineDashStyle': 'dash'
        }],
        
        'tooltip': {
            'shared': True
        },
        
        'legend': {
            'align': 'right',
            
            'verticalAlign': 'top',
            
            'floating': True,
            'itemStyle': {
                'font': 'Michroma',
                'color': '#CED5DF'
            },
            'backgroundColor': 'rgba(0,0,0,0)'
        },
        
        'series': [{
            'name': 'Count of Scam Type',
            'type': 'column',
            'data': top_scam_type_num_report,
            'color': 'rgba(52, 181, 213, 0.7)',
            'dataLabels': {'enabled': True},

        }, {
            'name': 'Amount Scammed',
            'type': 'spline',
            'data': top_scam_total_amount_scammed_per_type,
            'color': 'rgba(210, 177, 201, 1.0)',
            'yAxis': 1,
            'tooltip': {
                'valuePrefix': '$',
                'valueSuffix': ' Million'
            },
        }],
    })
    
    return top_scam_types_plot
