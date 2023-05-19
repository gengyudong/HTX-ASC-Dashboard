from nicegui import app, ui
import pymysql
import pandas as pd
import js2py

from utils.d2_fundrecovery import *
from utils.d2_recoverytypology import *
from utils.d2_fundflow import *
from utils.d2_bankperformance import *
from utils.d2_recoverytrend import *

# @ui.page('/dashboard2')
@ui.refreshable
def d2_content():
    app.add_static_files('/media', 'media')
    #has 16 px padding around nicegui-content class div 

    ui.add_head_html('''
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Michroma&display=swap" rel="stylesheet">
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
    
    connection = pymysql.connect(host = '119.74.24.181', user = 'htx', password = 'Police123456', database = 'ASTRO')
    df = pd.read_sql_query("SELECT * FROM astro.scam_management_system", connection)
    
    # connection2 = pymysql.connect(host = 'localhost', user = 'root', password = 'X-rayisharmful01', database = 'sys')
    # df = pd.read_sql_query("SELECT * FROM sys.scam_management_system", connection2)

    #-------------------------------------------------------------------------------------------------------------------------------------------------------------#

    with ui.row().style('height: 60vh; width: 100%; flex-wrap: nowrap'):
        
        
        #   Recovery by Typology Plot
        division = ui.element('div')
        with division.style(div_general_style).style('height: 100%; width: 30%'):
            recovery_by_typology_plot(df).style('height: 100%')
            # ui.add_body_html("""
            # <script>document.addEventListener('DOMContentLoaded', function () {
            # const chart = Highcharts.chart('"""+str(division.id)+ "', {" + recovery_by_typology_plot(df))

        with ui.column().style('width: 40%; height:100%; flex-wrap: nowrap; gap:0rem;').classes('items-center'):
            #   ASC Logo
            with ui.element('div').style('height: 10vh; width: 100%'):
                with ui.row().classes('items-center justify-center'): 
                    ui.image('https://www.police.gov.sg/-/media/Spf/Archived/2021-10-28/SPF200/Homepage/Large-SPF-Logo.ashx?h=296&w=314&la=en&hash=5D66E7698CEFB5D7B9028D9905C03967').style('width: 5vw')
                    ui.label('ANTI-SCAM CENTRE').style('font-family: Michroma; font-size: 1.1vw; color: #CED5DF; letter-spacing: 0.2vw; word-spacing: 0.3vw; font-weight: bold;')

            #   Fund Recovery Progress
            with ui.element('div').classes('items-center').style('align: center; height: 50vh; width: 100%'):
                fund_recovery_plot(df).style('position:relative; width: 100%; height: 100%')

        #   Bank's Performance
        with ui.element('div').style(div_general_style).style('width: 30%'):
            with ui.row().classes('justify-between items-center').style('flex-wrap: nowrap;'):
                ui.label("Bank's Performance").style(label_style)
                ui.select(['min', 'max', 'sum', 'mean'], value='mean', on_change = lambda x:change_stats(x.value, grid)).style('background-color: #87c6e6 !important; border-radius:5px;').classes('px-3 w-28')
            grid = bank_performance_table_dropdown(df).style('height:85%;')
                # .style('height: 50vh;') #Cant get the height correct on differnet size screens  
            
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------#

    with ui.row().style('height: 34.5vh; width: 100%; flex-wrap: nowrap;'):
        
        #   Recovery Trend Plot
        with ui.element('div').style(div_general_style).style('width: 70%'):
            recovery_trend_plot(df).style('height: 100%; width: 100%')
        
        #   Breakdown of Fund Flow Plot
        with ui.element('div').style(div_general_style).style('width: 30%'):
            ffp = fund_flow_plot(df).style('height: 100%; width: 100%')
            # .on('click', lambda: ui.notify('Not sure how '))
    
    # async def handleBarClick():
    #     await 

    print(type(division.id))

    

d2_content()
           

def update():
    d2_content.refresh()

# ui.timer(20.0, update)
ui.run()