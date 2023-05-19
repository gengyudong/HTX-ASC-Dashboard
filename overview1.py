from nicegui import app, ui
import pymysql
import pandas as pd
from datetime import date, timedelta

from overview2 import d2_content
from utils.d1_telco import *
from utils.d1_topscamtypes import *
from utils.d1_heatmap import *
from utils.d1_scamtypology import *

#   Initiating Connection with DB
connection = pymysql.connect(host = '119.74.24.181', user = 'htx', password = 'Police123456', database = 'ASTRO')
cursor = connection.cursor()
cursor.execute("SELECT UPDATE_TIME FROM information_schema.tables WHERE TABLE_SCHEMA = 'sys' AND TABLE_NAME = 'sys_config'")
result = cursor.fetchone()
initial_updated_time = result[0]

@ui.refreshable
def d1_content():
    app.add_static_files('/media', 'media') 

    ui.add_head_html('''            
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Michroma&display=swap" rel="stylesheet">
        ''')

    general_style = '''
        border-style: solid; 
        border-width: 1px; 
        border-radius: 10px;
        border-color: rgba(28, 27, 66, 0.2); 
        
        background-color: rgba(28, 27, 66, 0.2);
        
        font-family: "Michroma"; 
        color: #CED5DF;
    '''

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

    scam_count_box_style =  '''
        display: flex; 
        align-items: center;
        text-align: center;
        
        font-family: "Michroma"; 
        color: #CED5DF;
    '''

    percentage_style = ('''
        min-width: 7vw;
        height: 3vh;
        
        border-style: solid; 
        border-width: 1px; 
        border-radius: 20px;
        
        margin: auto;
        
        font-size: 0.5vw;
        font-weight: 600;
    ''')

    #   Background
    ui.video('/media/jellyfish-121604.mp4', controls = False, autoplay=True, loop=True).style(bg_video)
        
    #   Initialising connection with db & Fetching data from MySQL database to a Pandas df
    connection = pymysql.connect(host = '119.74.24.181', user = 'htx', password = 'Police123456', database = 'ASTRO')
    df = pd.read_sql_query("SELECT * FROM astro.scam_management_system", connection)

    #-------------------------------------------------------------------------------------------------------------------------------------------------------------#

    with ui.row().style('height: 48vh; width: 100%; flex-wrap: nowrap'):
        
        with ui.column().style('height: 48vh; width: 30%; flex-wrap: nowrap'):
            
            #   Box 1: ASC Logo
            with ui.element('div').style('height: 10vh; width: 100%'):
                with ui.row().classes('items-center justify-center'): 
                    ui.image('https://www.police.gov.sg/-/media/Spf/Archived/2021-10-28/SPF200/Homepage/Large-SPF-Logo.ashx?h=296&w=314&la=en&hash=5D66E7698CEFB5D7B9028D9905C03967').style('width: 5vw')
                    ui.label('ANTI-SCAM CENTRE').style('font-family: Michroma; font-size: 1.1vw; color: #CED5DF; letter-spacing: 0.2vw; word-spacing: 0.3vw; font-weight: bold')
                
    # -------------------------------------------------------------------------------------------------------------------------------------------------------------#
        
            #   Box 2: Scam Count Figure
            with ui.element('div').style('height: 38vh; width: 100%').style(scam_count_box_style):
                
                ##   Determining figure for Scam Count
                df_report = df.drop_duplicates(subset=['report_number'])
                total_report = len(df_report.index)
                total_report = '{:,}'.format(total_report)
                total_report_font_size = 4 - (len(str(total_report)) - 7)//2
                
                
                ##  Determining figures for 4 percentages
                def victim_count(date):
                    past_df = df[df.date_assigned == date]
                    victim_count = len(past_df.index)
                    
                    return victim_count
                
                def percentage(today, past):
                    if past == 0:
                        return 0
                    
                    else:
                        change = today - past
                        percentage_change = abs(change / past) * 100
                        percentage_change = round(percentage_change, 1)

                        return percentage_change

                def arrow_type(today, past):
                    change = today - past
                    if change > 0:
                        return 'arrow_upward'
                    if change < 0:
                        return 'arrow_downward'
                    else:
                        return "remove"
                    
                
                ### Scam Count - Today  
                today = date.today()
                today_victim_count = victim_count(today)
                
                ### Scam Count - Past Day 
                past_day = today - timedelta(days = 1)
                past_day_victim_count = victim_count(past_day)
                
                ### Scam Count - Past Week
                past_week = today - timedelta(days = 7)
                past_week_victim_count = victim_count(past_week)
                
                ### Scam Count - Past Month
                past_month = today - timedelta(days = 30)
                past_month_victim_count = victim_count(past_month)
                
                ### Scam Count - Past Year
                past_year = today - timedelta(days = 365)
                past_year_victim_count = victim_count(past_year)
                
                ### Percentage (vs Last Day)
                day_percentage = percentage(today_victim_count, past_day_victim_count)
                day_arrow = arrow_type(today_victim_count, past_day_victim_count)
                
                ### Percentage (vs Last Week)
                week_percentage = percentage(today_victim_count, past_week_victim_count)
                week_arrow = arrow_type(today_victim_count, past_week_victim_count)

                ### Percentage (vs Last Month)
                month_percentage = percentage(today_victim_count, past_month_victim_count)
                month_arrow = arrow_type(today_victim_count, past_month_victim_count)

                ### Percentage (vs Last Year)
                year_percentage = percentage(today_victim_count, past_year_victim_count)
                year_arrow = arrow_type(today_victim_count, past_year_victim_count)
                
                with ui.element('div').style('margin: auto'):
                    
                    ui.label('Total Reports').style('font-size: 2vw; font-weight: 500; color: #E6EAEF; letter-spacing: 0.15vw; margin-top: -6vh; margin-bottom: 2vh')
                    
                    ui.label(total_report).style(f'font-size: {total_report_font_size}vw; color: #E6EAEF; margin-bottom: 2vh')
                    
                    with ui.row().style('margin-top: 1vh'):
                        for i in range(2):
                            arrow_array = [day_arrow, week_arrow]
                            percentage_array = [day_percentage, week_percentage]
                            word_array = ['DoD', 'WoW']
                            
                            arrow = arrow_array[i]
                            percentage_num = percentage_array[i]
                            word = word_array[i]
                            
                            if arrow == 'arrow_upward':
                                with ui.row().classes('items-center').style(percentage_style).style('background-color: #3D1915; border-color: #3D1915'):
                                    with ui.element('div').style('margin: auto'):
                                        with ui.row():
                                            ui.icon(arrow).style('margin-left: 0.4vw; margin-right: -0.5vw; margin-top: 0.4vh; color: #C14A78; font-weight: 600')
                                            ui.label(f'{percentage_num}% {word}').style('color: #C14A78; letter-spacing: 0.1vw')
                                    
                            elif arrow == 'arrow_downward':
                                with ui.row().classes('items-center').style(percentage_style).style('background-color: #117E73; border-color: #117E73'):
                                    with ui.element('div').style('margin: auto'):
                                        with ui.row():
                                            ui.icon(arrow).style('margin-left: 0.4vw; margin-right: -0.5vw; margin-top: 0.4vh; color: #28E2CF; font-weight: 600')
                                            ui.label(f'{percentage_num}% {word}').style('color: #28E2CF; letter-spacing: 0.1vw')
                            
                            elif arrow == 'remove':
                                with ui.row().classes('items-center').style(percentage_style).style('background-color: #404F63; border-color: #404F63'):
                                    with ui.element('div').style('margin: auto'):
                                        with ui.row():
                                            ui.icon(arrow).style('margin-left: 0.4vw; margin-right: -0.2vw; margin-top: 0.4vh; color: #CED5DF; font-weight: 600')
                                            ui.label(f'0% {word}').style('color: #CED5DF; letter-spacing: 0.2vw')
                    
                    with ui.row().style('margin-top: 2vh'):
                        for i in range(2):
                            arrow_array = [month_arrow, year_arrow]
                            percentage_array = [month_percentage, year_percentage]
                            word_array = ['MoM', 'YoY']
                            
                            arrow = arrow_array[i]
                            percentage_num = percentage_array[i]
                            word = word_array[i]
                            
                            if arrow == 'arrow_upward':
                                with ui.row().classes('items-center').style(percentage_style).style('background-color: #3D1915; border-color: #3D1915'):
                                    with ui.element('div').style('margin: auto'):
                                        with ui.row():
                                            ui.icon(arrow).style('margin-left: 0.4vw; margin-right: -0.5vw; margin-top: 0.4vh; color: #C14A78; font-weight: 600')
                                            ui.label(f'{percentage_num}% {word}').style('color: #C14A78; letter-spacing: 0.1vw')
                            
                            elif arrow == 'arrow_downward':
                                with ui.row().classes('items-center').style(percentage_style).style('background-color: #117E73; border-color: #117E73'):
                                    with ui.element('div').style('margin: auto'):
                                        with ui.row():
                                            ui.icon(arrow).style('margin-left: 0.4vw; margin-right: -0.5vw; margin-top: 0.4vh; color: #28E2CF; font-weight: 600')
                                            ui.label(f'{percentage_num}% {word}').style('color: #28E2CF; letter-spacing: 0.1vw')
                            
                            elif arrow == 'remove':
                                with ui.row().classes('items-center').style(percentage_style).style('background-color: #404F63; border-color: #404F63'):
                                    with ui.element('div').style('margin: auto'):
                                        with ui.row():
                                            ui.icon(arrow).style('margin-left: 0.4vw; margin-right: -0.2vw; margin-top: 0.4vh; color: #CED5DF; font-weight: 600')
                                            ui.label(f'0% {word}').style('color: #CED5DF; letter-spacing: 0.2vw')

    #-------------------------------------------------------------------------------------------------------------------------------------------------------------#

        #   Box 3: Top Scam Typologies
        with ui.column().style('height: 48vh; width: 35%'):
            with ui.element('div').style('height: 5%; width: 100%'):
                ui.label('Scam Typologies').style('font-family: Michroma; font-size: 1vw; font-weight: bold; color: #E6EAEF')
            with ui.element('div').style(general_style).style('height: 90%; width: 100%'):
                top_scam_types_plot(df).style('width: 100%; height: 100%')
                
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------#
        #   Box 4: Heatmap
        with ui.column().style('height: 48vh; width: 35%'):
            with ui.element('div').style('height: 5%; width: 100%'):
                ui.label('Divisional Heatmap').style('font-family: Michroma; font-size: 1vw; font-weight: bold; color: #E6EAEF')
            with ui.element('div').style(general_style).style('height: 90%; width: 100%; overflow: hidden'):
                heatmap(df).style('height: 100%; width: 150%; margin: auto')
                
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------#

    with ui.row().style('height: 46.5vh; width: 100%; flex-wrap: nowrap'):
        
        #   Box 7: Scam Typology Trend
        with ui.column().style('height: 48vh; width: 65%'):
            with ui.element('div').style('height: 5%; width: 100%'):
                ui.label('Scam Typology Trend (Top 10)').style('font-family: Michroma; font-size: 1vw; font-weight: bold; color: #E6EAEF')
            with ui.element('div').style(general_style).style('height: 90%; width: 100%'):
                scam_typology_plot(df).style('height: 100%; width: 100%')
    
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------#
            
        #   Box 3: Telco-Line Termination Chart
        with ui.column().style('height: 48vh; width: 35%'):
            with ui.element('div').style('height: 5%; width: 100%'):
                ui.label('Telco Line Termination').style('font-family: Michroma; font-size: 1vw; font-weight: bold; color: #E6EAEF')
            with ui.element('div').style(general_style).style('height: 90%; width: 100%'):
                telco_df = pd.read_sql_query("""select telco from scam_management_system 
                join telcos on scam_management_system.telco_report_number = telcos.report_reference""", connection)
                telco_plot(telco_df).style('width: 100%; height: 100%')

# @ui.page('/dashboard1')
d1_content()

#   Updating of UI
def check_db_change():
    cursor.execute("SELECT UPDATE_TIME FROM information_schema.tables WHERE TABLE_SCHEMA = 'sys' AND TABLE_NAME = 'sys_config'")
    result = cursor.fetchone()
    latest_update_time = result[0]
    global initial_updated_time
    global df_test
    if latest_update_time != initial_updated_time:
        d1_content.refresh()
        initial_updated_time = latest_update_time
    

ui.timer(10.0, check_db_change)
        
ui.run()