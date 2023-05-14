from nicegui import ui
import pandas as pd
async def add_data():
    await ui.run_javascript(
        '''return `
			x: ${this.x}, 
			y: ${this.y}
		`
		'''
    )


def fund_flow_plot(df):
    ###     Data Processing 
    fundFlowDf = df[['overseas_local', 'amount_scammed', 'amount_transcated']].copy()
    fundFlowSum = fundFlowDf.groupby('overseas_local').sum().round(2)
    fundFlowCount = fundFlowDf.groupby('overseas_local').size()
    fundFlowSum = fundFlowSum['amount_scammed']+fundFlowSum['amount_transcated']

    #   data cleaning
    fundFlowSum['L-L']+=fundFlowSum['L-l']
    fundFlowSum = fundFlowSum.drop('L-l')

    fundFlowCount['L-L']+=fundFlowCount['L-l']
    fundFlowCount = fundFlowCount.drop('L-l')

    #   convert to list
    to_display_df = pd.concat([fundFlowSum, fundFlowCount], axis = 1)
    to_display_df.columns = ['y', 'count']
    result = to_display_df.to_json(orient="records")

    chart = ui.chart({
            'chart': {'type': 'bar',
                      'backgroundColor': 'rgba(0,0,0,0)',},
            
            'title': {
                'text': 'Breakdown of Fund Flow',
                'margin': 20,
                'align': 'left',
                'style': {
                    'color': '#CED5DF',
                    'fontWeight': 'bold',
                    'fontFamily': 'Michroma'
                }
            },
            
            'xAxis': {
                'categories': ['L-L', 'L-O', 'O-L', 'O-O'],
                      'labels':{
                            'style': {'color': '#CED5DF'}
                        }
                    },

            
            'yAxis':{
                'title': {
                    'text': 'Amount of Funds ($)',
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
                'data': result,
                        'dataLabels':{
                            'enabled': True,
                            'style': {'color': '#CED5DF'},
                        },
                        'borderWidth':0,
                    }],

            'tooltip':{
                'formatter':""" return `
                count: ${this.count}, 
                sum: ${this.y}, 
		        `"""
            },

            'legend':{
                'enabled': False
            },
            'credits': {
                'enabled': False
            },
        }).classes('w-full h-64')
    
    return chart
