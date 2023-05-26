from nicegui import ui, Client

category_list = ["a", "b", "c", "d", "e"]
data_list = [1,2,3,4,5]
chart = ui.chart({
            'chart': {
                'type': 'bar',
                'backgroundColor': 'rgba(0,0,0,0)'},
            
            'title': {
                'text': 'Recovery by typology',
                'margin': 20,
                'align': 'left',
                'style': {
                    'color': '#CED5DF',
                    'fontWeight': 'bold',
                    'fontFamily': 'Michroma'
                }
            },

            'xAxis': {
                'type': 'category',
                'categories': category_list,
                'min': 0,
                'max': 9,
                'tickLength': 0,
                'labels':{
                    'style': {
                        'color': '#CED5DF',
                              }
                },
                'scrollbar':{
                    'enabled':True,
                },
            },
            'yAxis':{
                'title': {
                'text': 'Amount Recovered',
                'style': {
                        'color': '#CED5DF'
                    },
                },
                'labels': {
                    'style': {
                    'color': '#CED5DF',
                    },
                },
                'gridLineDashStyle': 'dash',
                
            },
            
            'plotOptions': {
                'bar': {
                    'dataLabels': {
                        'enabled': 'true',
                        'style': {'color': '#CED5DF'},
                    },
                    'borderWidth':0,
                },
            },

            'tooltip':{
                'valueDecimals': 2,
                'valuePrefix': '$',
            },

            'legend': {
                'enabled': 'false'
            },
            'credits': {
                'enabled': 'false'
            },

            'series': [{'name': 'Recovered',
                        'data': data_list,
                        # 'color': 'rgba(52, 181, 213, 0.7)',
                    'dataLabels':{
                            'enabled': True,
                            'format': '${point.y:,.2f}',
                            
            #                 'formatter':""" function () {
            #     return this.value + ' units';
            # }"""
            # cant figure out how to round this thing to M
            #might try using number formatter (formats all numbers not just data labels to millions)
                    }
                    
                    }],
        }, extras = ['stock']) 
chartB = ui.chart({
            'chart': {'type': 'bar',
                      'backgroundColor': 'rgba(0,0,0,0)',
                      'zoomType': 'y',
            },
            
            'title': {
                'text': 'Breakdown of Fund Flow',
                'margin': 20,
                'align': 'left',
                'style': {
                    'color': '#CED5DF',
                    'fontWeight': 'bold',
                    'fontFamily': 'Michroma',
                }
            },
            
            'xAxis': {
                'type': 'category',
                'categories': category_list,
                'labels':{
                    'style': {'color': '#CED5DF'},
                },
            },

            
            'yAxis':{
                'title': {
                    'text': 'Amount of Funds',
                    'style': {
                        'color': '#CED5DF'
                    },
                },
                'labels':{
                            'style': {'color': '#CED5DF'}
                        },
                'gridLineDashStyle': 'dash',
            },


            'series': [{
                'name': 'Funds',
                'data': data_list,
                'dataLabels':{
                    'enabled': True,
                    'style': {'color': '#CED5DF'},
                    'format': '${point.y:,.2f}',
                },
                'borderWidth':0,
                'dataGrouping': False,

                    }],

            'tooltip':{
                'useHTML': True,
                'headerFormat': '<table><tr><th>{point.key}</th></tr>',
                'pointFormat': '<tr><td>Amount of Funds: {point.y}</td></tr>' +
                    '<tr><td>Number of Cases: {point.count}</td></tr>',
                'footerFormat': '</table>',
                'valueDecimals': 2,
                'valuePrefix': '$',
            },

            'plotOptions':{
                'bar': {
                    'color': '#db3eb1',
                }, 

            },

            'legend':{
                'enabled': False,
            },
            'credits': {
                'enabled': False,
            },
        }).classes('w-full h-64')

ui.run()