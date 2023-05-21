from nicegui import Client, ui
# import asyncio

@ui.page('/')
async def page(client: Client):
    chart = ui.chart({
        'xAxis': {
            'categories': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        },
        'plotOptions': {
            'series': {
                'cursor': 'pointer',
            }
        },
        'series': [{
            'data': [29.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4]
        }]
    })
    await client.connected()
    await ui.run_javascript('''
        const chart = getElement(''' + str(chart.id) + ''').chart;
        chart.update({
            plotOptions: {
                series: {
                    point: {
                        events: {
                            click: function() {
                               alert('Category: ' + this.category + ', value: ' + this.y);
                            }
                        }
                    }
                }
            }
        });
        ''', respond=False)
    
# ui.link('visit page', page)
ui.run()