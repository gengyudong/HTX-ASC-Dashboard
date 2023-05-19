from nicegui import ui

ui.add_head_html('''            
        <script src="https://code.highcharts.com/highcharts.js"></script>   
        ''')

with ui.row().style('flex-wrap: nowrap'):
    ui.label('hi')
    with ui.element('div'):
        ui.add_body_html (
            '''
            <div id="container" style="width:50%; height:50vh;"></div>    
                <script>
                document.addEventListener('DOMContentLoaded', function () {
                    const chart = Highcharts.chart('container', {
                        chart: {
                            type: 'bar'
                        },
                        title: {
                            text: 'Fruit Consumption'
                        },
                        xAxis: {
                            categories: ['Apples', 'Bananas', 'Oranges']
                        },
                        yAxis: {
                            title: {
                                text: 'Fruit eaten'
                            }
                        },
                        plotOptions: {
                            series: {
                                cursor: 'pointer',
                                point: {
                                    events: {
                                        click: function () {
                                            alert('Category: ' + this.category + ', value: ' + this.y);
                                        }
                                    }
                                }
                            }
                        },
                        series: [{
                            name: 'Jane',
                            data: [1, 0, 4]
                        }, {
                            name: 'John',
                            data: [5, 7, 3]
                        }]
                    });
                });
                </script>
            ''')
    with ui.element('div'):
        ui.add_body_html (
            '''
            <div id="container2" style="width:50%; height:50vh;"></div>    
                <script>
                document.addEventListener('DOMContentLoaded', function () {
                    const chart = Highcharts.chart('container2', {
                        chart: {
                            type: 'bar'
                        },
                        title: {
                            text: 'Fruit Consumption'
                        },
                        xAxis: {
                            categories: ['Apples', 'Bananas', 'Oranges']
                        },
                        yAxis: {
                            title: {
                                text: 'Fruit eaten'
                            }
                        },
                        plotOptions: {
                            series: {
                                cursor: 'pointer',
                                point: {
                                    events: {
                                        click: function () {
                                            alert('Category: ' + this.category + ', value: ' + this.y);
                                        }
                                    }
                                }
                            }
                        },
                        series: [{
                            name: 'Jane',
                            data: [1, 0, 4]
                        }, {
                            name: 'John',
                            data: [5, 7, 3]
                        }]
                    });
                });
                </script>
            
            ''')
ui.run()
