from nicegui import app, ui, Client
import pymysql
import pandas as pd

from utils.d2_fundrecovery import *
from utils.d2_recoverytypology import *
from utils.d2_fundflow import *
from utils.d2_bankperformance import *
from utils.d2_recoverytrend import *
from utils.filter_data import *

from fastapi import Form

@app.post("/env")
async def write_to_file(condition: str = Form(...), value: str = Form(...),):
    print(condition, value )
    await add_grid_event()
    

@ui.refreshable
@ui.page('/')
async def d2_content(client: Client):
    #has 16 px padding around nicegui-content class div 

    ui.add_head_html('''
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Michroma&display=swap" rel="stylesheet">
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        ''')

    connection = pymysql.connect(host = '119.74.24.181', user = 'htx', password = 'Police123456', database = 'ASTRO')
    global df
    df= pd.read_sql_query("SELECT * FROM astro.scam_management_system", connection)
    filtered_df = filter_data(df)

    #-------------------------------------------------------------------------------------------------------------------------------------------------------------#
    
    with ui.row().style('height: 60vh; width: 100%; flex-wrap: nowrap'):
        
        
        #   Recovery by Typology Plot
        with ui.element('div'):
            global rbt 
            rbt = recovery_by_typology_plot(filtered_df).style('height: 100%')
            
            #   Fund Recovery Progress

        #   Bank's Performance
        with ui.element('div'):
            with ui.row():
                ui.label("Bank's Performance")
                ui.select(['min', 'max', 'sum', 'mean'], value='mean', on_change=change_stats).style('background-color: #87c6e6 !important; border-radius:5px;').classes('px-3 w-28')
            global table
            table = bank_performance_table(df).style('height:85%;')
                # .style('height: 50vh;') #Cant get the height correct on differnet size screens  
            
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------#
            
    ### Put Click event in all charts
    await client.connected(timeout = 15.0)
    await ui.run_javascript("""
        const RBT_chart = getElement(""" +str(rbt.id)+""").chart;
        RBT_chart.update({
            plotOptions: {
                series: {
                    point: {
                        events: {
                            click: function() {
                                this.select(null, true);
                                $.ajax({
                                    type: 'POST',
                                    url: '/env', 
                                    data: {
                                        condition: "SCAMTYPE",
                                        value: this.category,
                                    },
                                    success: function (response) {
                                        console.log(response);
                                    },
                                    error: function (xhr, status, error) {
                                        console.log(error);
                                    }
                                });
                                
                            }
                        }
                    }
                }
            }
        });
    """, respond=False)
    await add_grid_event()
   



ui.run(port = 8082)