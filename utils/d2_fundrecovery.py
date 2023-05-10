from nicegui import ui


def fund_recovery_plot(df):
    df_amount_recovery = df[['amount_scammed', 'latest_balance_seized']].copy()
    df_amount_recovery = df_amount_recovery.fillna(0)

    amount_scammed = 0
    for i in range(len(df_amount_recovery.index)):
        amount_scammed += df_amount_recovery['amount_scammed'][i]
        
    amount_recover= 0
    for i in range(len(df_amount_recovery.index)):
        if df_amount_recovery['latest_balance_seized'][i] >= df_amount_recovery['amount_scammed'][i]:
            amount_recover += df_amount_recovery['amount_scammed'][i]
        
        else:
            amount_recover += df_amount_recovery['latest_balance_seized'][i]

    amount_recover = round(amount_recover, 2)
    amount_scammed = round(amount_scammed, 2)

    amount_recover_percentage = amount_recover / amount_scammed * 100
    amount_recover_percentage = round(amount_recover_percentage, 1)
    amount_scammed_percentage = 100.0 - amount_recover_percentage

    chart = ui.chart({
                'chart': {
                    'type': 'pie',
                    'backgroundColor': 'rgba(0,0,0,0)',
                },
                
                'title': {
                    'text': f'Scam Amount <br> ${amount_scammed:,} <br><br><b>Fund Recovery</b><br><br> Recovered Amount <br> ${amount_recover:,}',
                    'align': 'center',
                    'verticalAlign': 'middle',
                    'style': {
                        'color': '#CED5DF'
                    }
                },
                
                'credits': {'enabled': False},

                'accessibility': {
                    'announceNewData': {'enabled': True},
                    'point': {'valueSuffix': '%'}
                },

                'plotOptions': {
                    'series': {
                        'dataLabels': {
                            'enabled': True,
                            'format': '{point.name}: {point.y:.1f}%'
                        }
                    },
                    'pie': {
                        'borderColor': None,
                        'borderWidth': 8,
                        'innerSize': '98%',
                        'size': '100%',
                    },
                    
                },

                'tooltip': {
                    'headerFormat': '<span style="font-size:11px">{series.name}</span><br>',
                    'pointFormat': '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}%</b> of total<br/>'
                },

                'series': [
                    {
                        'colorByPoint': True,
                        'data': [
                            {
                                'name': 'Recovered',
                                'y': amount_recover_percentage,
                                'color': 'rgba(92, 255, 127, 0.7)',
                            },
                            {
                                'name': 'Loss',
                                'y': amount_scammed_percentage,
                                'color': 'rgba(255, 44, 104, 0.7)',
                            },
                        ],
  
                    }
                ],
            })

    return chart