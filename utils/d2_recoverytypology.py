from nicegui import ui

def recovery_by_typology_plot():
    chart = ui.chart({
                'chart': {
                    'type': 'bar',
                    'backgroundColor': 'rgba(0,0,0,0)',
                },
                
                'title': {
                    'text': 'Recovery by Typology (Top 10)',
                    'align': 'left',
                    'style': {
                        'color': '#CED5DF',
                        'fontWeight': 'bold',
                        'fontFamily': 'Michroma'
                    }
                },
                
                'xAxis': {
                    'categories': ['Africa', 'America', 'Asia', 'Europe', 'Oceania'],
                    'title': {
                        'text': None
                    },
                    'labels': {
                        'style': {
                            'color': '#CED5DF',
                        }
                    },
                },
                
                'yAxis': {
                    'min': 0,
                    'title': {
                        'text': 'Amount Recovered ($ Millions)',
                        'align': 'high',
                        'style': {
                            'color': '#CED5DF',
                        }
                    },
                    'labels': {
                        'overflow': 'justify',
                        'style': {
                            'color': '#CED5DF',
                        }
                    }
                },
            
                'plotOptions': {
                    'bar': {
                        'dataLabels': {
                            'enabled': True
                        }
                    }
                },
                'legend': {
                    'enabled': False
                },
                
                'credits': {
                    'enabled': False
                },
                
                'series': [{
                    'name': 'Year 1990',
                    'data': [631, 727, 3202, 721, 26],
                    'color': 'rgba(199, 205, 250, 0.9)',
                    'borderColor': 'rgba(121,136,243, 1)',
                    'tooltip': {
                        'valuePrefix': '$',
                        'valueSuffix': ' Million'
                    },     
                }]  
            })
    
    return chart