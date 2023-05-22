from nicegui import app, ui, Client
import pymysql
import pandas as pd
# import logging 

# logging.basicConfig(filename = 'app.log', level = logging.DEBUG)

from utils.d2_fundrecovery import *
from utils.d2_recoverytypology import *
from utils.d2_fundflow import *
from utils.d2_bankperformance import *
from utils.d2_recoverytrend import *
from utils.d2_fundflow_data import *
from utils.d2_recoverytypology_data import *

from fastapi import HTTPException, Form


@app.post("/env")
async def write_to_file(key: str = Form(...), value: str = Form(...),):
    try:
        ### WRITE ENV FILE
        with open('.env', 'r') as file:
            lines = file.readlines()

        updated_lines = []

        #might change this to a less clunky way using python dotenv 
        for line in lines:
            if 'CONDITION' in line:
                line = f"CONDITION={key}\n"
            elif key in line:
                line = f"{key}={value}\n"
            updated_lines.append(line)

        with open('.env', 'w') as file:
            file.writelines(updated_lines)
        
        message = "Environment variable updated successfully. "

        if key =='OVERSEAS_LOCAL':
            await update_RT()
            message+= "Recovery typology chart updated"
            # add on other charts update functions

        elif key == 'SCAM_TYPE':
            await update_FFP()
            message+= "Fund Flow chart updated"
            # add on other charts update functions

        return {"message": message}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def update_RT():
    category_list, data_list = recovery_typology_data(connection)
    rt.options['series'][0]['data'] = data_list
    rt.options['xAxis']['categories'] = category_list
    rt.update()
    print("UPDATE_RT")

async def update_FFP():
    ffp.options['series'][0]['data'] = fundflow_data(connection)
    ffp.update()
    print(ffp.options)
    print("UPDATE_FFP")

@ui.refreshable
@ui.page('/')
async def d2_content(client: Client):

    app.add_static_files('/media', 'media')

    #has 16 px padding around nicegui-content class div 

    ui.add_head_html('''
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Michroma&display=swap" rel="stylesheet">
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        ''')

    bg_video = '''
        width: 100vw;
        height: 100vh;
        object-fit: cover;
        position: fixed;
        left: 0;
        right: 0;
        top: 0;
        bottom: 0;
        z-index: -1;
    '''

    div_general_style = '''
        border-style: solid; 
        border-width: 1px; 
        border-radius: 10px;
        border-color: rgba(24, 55, 99, 0.3); 
        height: 100%;

        background-color: rgba(24, 55, 99, 0.3);
        
        font-family: "Michroma"; 
        color:#CED5DF;
        text-align: center;
    '''

    label_style = '''
        color:#CED5DF;
        font-weight: bold;
        text-align: left;
        height:5%;
        margin: 10px;
    '''

    # ui.video('/media/jellyfish-121604.mp4', controls = False, autoplay=True, loop=True).style(bg_video)
    ui.image('/media/neon_background1.jpg').style(bg_video)
    
    global connection
    connection = pymysql.connect(host = '119.74.24.181', user = 'htx', password = 'Police123456', database = 'ASTRO')
    # query = f"SELECT * FROM astro.scam_management_system WHERE overseas_local = '{overseas_local}'" #improve this to put the ? 
    
    # df = pd.read_sql_query(query, connection)

    #-------------------------------------------------------------------------------------------------------------------------------------------------------------#
    
    with ui.row().style('height: 60vh; width: 100%; flex-wrap: nowrap'):
        
        
        #   Recovery by Typology Plot
        division = ui.element('div')
        with division.style(div_general_style).style('height: 100%; width: 30%'):
            global rt 
            rt = recovery_by_typology_plot(connection).style('height: 100%')
            await client.connected()
            

        """ with ui.column().style('width: 40%; height:100%; flex-wrap: nowrap; gap:0rem;').classes('items-center'):
            #   ASC Logo
            with ui.element('div').style('height: 10vh; width: 100%'):
                with ui.row().classes('items-center justify-center'): 
                    ui.image('https://www.police.gov.sg/-/media/Spf/Archived/2021-10-28/SPF200/Homepage/Large-SPF-Logo.ashx?h=296&w=314&la=en&hash=5D66E7698CEFB5D7B9028D9905C03967').style('width: 5vw')
                    ui.label('ANTI-SCAM CENTRE').style('font-family: Michroma; font-size: 1.1vw; color: #CED5DF; letter-spacing: 0.2vw; word-spacing: 0.3vw; font-weight: bold;')

            #   Fund Recovery Progress
            with ui.element('div').classes('items-center').style('align: center; height: 50vh; width: 100%'):
                fund_recovery_plot().style('position:relative; width: 100%; height: 100%')

        #   Bank's Performance
        with ui.element('div').style(div_general_style).style('width: 30%'):
            with ui.row().classes('justify-between items-center').style('flex-wrap: nowrap;'):
                ui.label("Bank's Performance").style(label_style)
                ui.select(['min', 'max', 'sum', 'mean'], value='mean', on_change = lambda x:change_stats(x.value, grid)).style('background-color: #87c6e6 !important; border-radius:5px;').classes('px-3 w-28')
            grid = bank_performance_table_dropdown(df).style('height:85%;')
                # .style('height: 50vh;') #Cant get the height correct on differnet size screens   """
            
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------#

    with ui.row().style('height: 34.5vh; width: 100%; flex-wrap: nowrap;'):
        
        #   Recovery Trend Plot
        # with ui.element('div').style(div_general_style).style('width: 70%'):
        #     recovery_trend_plot(df).style('height: 100%; width: 100%')
        
        #   Breakdown of Fund Flow Plot
        with ui.element('div').style(div_general_style).style('width: 30%'):
            global ffp
            ffp = fund_flow_plot(connection).style('height: 100%; width: 100%')
            
    ### Put Click event in all charts
    await client.connected(timeout = 15.0)
    await ui.run_javascript("""
        const FFP_chart = getElement(""" +str(ffp.id)+""").chart;
        FFP_chart.update({
            plotOptions: {
                series: {
                    point: {
                        events: {
                            click: function() {
                                alert('Clicked: '+ this.category);
                                $.ajax({
                                    type: 'POST',
                                    url: '/env', // Replace with the correct URL
                                    data: {
                                        key: "OVERSEAS_LOCAL",
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
    
        const RT_chart = getElement(""" +str(rt.id)+""").chart;
        RT_chart.update({
            plotOptions: {
                series: {
                    point: {
                        events: {
                            click: function() {
                                alert('Clicked: '+ this.category);
                                $.ajax({
                                    type: 'POST',
                                    url: '/env', // Replace with the correct URL
                                    data: {
                                        key: "SCAM_TYPE",
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
   

def update():
    d2_content.refresh()
    print("REFRESH WEBSITE")


ui.timer(20.0, update)
ui.run(port = 8082)