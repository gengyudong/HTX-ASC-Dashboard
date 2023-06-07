from nicegui import app, ui, Client
import pymysql
import pandas as pd
from datetime import date, timedelta

from utilsv3.d1_totalreports import *
from utilsv3.d1_telco import *
from utilsv3.d1_topscamtypes import *
from utilsv3.d1_heatmap import *
from utilsv3.d1_scamtypology import *
from utilsv3.filter_data import *

from fastapi import HTTPException, Form
from dotenv import set_key, dotenv_values


with open('.env', 'w') as f:
    f.write("""
SCAMTYPE_Job.Scam=0
SCAMTYPE_Investment.Scam=0
SCAMTYPE_E-Commerce.Scam=0
SCAMTYPE_Other.Scam=0
SCAMTYPE_Rental.Scam=0
SCAMTYPE_GOIS=0
SCAMTYPE_Loan.Scam=0
SCAMTYPE_Love/Parcel.Scam=0
SCAMTYPE_S/M.Impersonation.Scam=0
SCAMTYPE_Friend.Fake.Buyer.Scam=0
SCAMTYPE_Non.Scam=0
SCAMTYPE_OSSS.Scam=0
SCAMTYPE_Bank.Phishing.SMS.Scam=0
SCAMTYPE_FGPS.Scam=0
SCAMTYPE_COIS.Scam=0
SCAMTYPE_Love/Investment.Scam=0
SCAMTYPE_Tech.Support.Scam=0
SCAMTYPE_BEC.Scam=0
SCAMTYPE_Non-Bank.Phishing.SMS.Scam=0
SCAMTYPE_Phishing.Scam=0
SCAMTYPE_Lucky.Draw.Scam=0
SCAMTYPE_Sugar.Mummy.Scam=0
SCAMTYPE_Inheritance.Scam=0
SCAMTYPE_Lottery.Scam=0
SCAMTYPE_Investment.(Traditional).Scam=0
SCAMTYPE_Remittance.Scam=0
SCAMTYPE_Force/Trial.Scam=0
SCAMTYPE_Time.Share.Scam=0
SCAMTYPE_Whatsapp.Takeover.Scam=0

TELCO_M1=0
TELCO_MyRepublic=0
TELCO_Singtel=0
TELCO_Starhub=0
    """)

@app.post("/env")
async def write_to_file(condition: str = Form(...), value: str = Form(...),):
    try:
        #might add a CONDITION= condition, with a whole dictionary to transform SCAMTYPE to scam_type to pass in the condition
        print('\n', condition, value, '\n')
        env_vars = dotenv_values('.env') 
        condition_value = condition + "_" + value.replace(" ", ".")

        #   Toggle 1 or 0 for that key
        if env_vars[condition_value] == '1':
            set_key('.env', condition_value, '0')
        elif env_vars[condition_value] == '0':
            set_key('.env', condition_value, '1')

        #   Set other fields as 0
        for key in env_vars.keys():
            if key.startswith(condition + "_") == False:
                set_key('.env', key, '0')
        
        message = "Environment variable updated successfully. "

        global filtered_df
        filtered_df = filter_data(df)
        await update_charts(condition)
            
        return {"message": message}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def update_charts(condition):
    print("UPDATE CHART START")
    
    if condition == "TELCO":
        top_scam_typology.update()
        print("Top Scam Typology Chart Data DONE")
        scam_typology.update()  
        print("Scam Typology Chart Data DONE")
        
        
    elif condition=="SCAMTYPE":
        scam_typology.update()
        print("SCAM TYPOLOGY OPTIONS", scam_typology.options)
        print("Scam Typology Chart Data DONE")
        telco.update()
    
    print("UPDATE CHART END\n")

#   Initiating Connection with DB
connection = pymysql.connect(host = '119.74.24.181', user = 'htx', password = 'Police123456', database = 'ASTRO')
cursor = connection.cursor()
cursor.execute("SELECT UPDATE_TIME FROM information_schema.tables WHERE TABLE_SCHEMA = 'astro' AND TABLE_NAME = 'scam_management_system'")
result = cursor.fetchone()
initial_updated_time = result[0]

@ui.refreshable
@ui.page('/')
async def d1_content(client: Client):
    app.add_static_files('/media', 'media') 

    ui.add_head_html('''            
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Michroma&display=swap" rel="stylesheet">
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
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
    global connection
    connection = pymysql.connect(host = '119.74.24.181', user = 'htx', password = 'Police123456', database = 'ASTRO')
    global df
    df = pd.read_sql_query("SELECT * FROM astro.scam_management_system", connection)
    filtered_df = filter_data(df)

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
                total_report = total_reports(df)
                total_report_font_size = 4 - (len(str(total_report)) - 7)//2
                
                #   Determining percentage values & arrow types
                day_percentage, week_percentage, month_percentage, year_percentage = percentage(df)
                day_arrow, week_arrow, month_arrow, year_arrow = arrow_function(df)
                
                global list_labels
                
                with ui.element('div').style('margin: auto'):
                    ui.label('Total Reports').style('font-size: 2vw; font-weight: 500; color: #E6EAEF; letter-spacing: 0.15vw; margin-top: -6vh; margin-bottom: 2vh')
                    ui.label(total_report).style(f'font-size: {total_report_font_size}vw; color: #E6EAEF; margin-bottom: 2vh')
                    
                    for i in range(2):
                        arrow_array = [[day_arrow, week_arrow], [month_arrow, year_arrow]]
                        percentage_array = [[day_percentage, week_percentage], [month_percentage, year_percentage]]
                        word_array = [['DoD', 'WoW'], ['MoM', 'YoY']]
                        
                        with ui.row().style('margin-top: 2vh'):
                            for j in range(2):
                                arrow = arrow_array[i][j]
                                percentage_num = percentage_array[i][j]
                                word = word_array[i][j]
                                
                                if arrow == 'arrow_upward':
                                    with ui.row().classes('items-center').style(percentage_style).style('background-color: #3D1915; border-color: #3D1915'):
                                        with ui.elemyoent('div').style('margin: auto'):
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
                global top_scam_typology
                top_scam_typology = top_scam_types_plot(filtered_df).style('width: 100%; height: 100%')
                
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
                global scam_typology
                scam_typology = scam_typology_plot(filtered_df).style('height: 100%; width: 100%')
    
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------#
            
        #   Box 3: Telco-Line Termination Chart
        with ui.column().style('height: 48vh; width: 35%'):
            with ui.element('div').style('height: 5%; width: 100%'):
                ui.label('Telco Line Termination').style('font-family: Michroma; font-size: 1vw; font-weight: bold; color: #E6EAEF')
            with ui.element('div').style(general_style).style('height: 90%; width: 100%'):
                telco_df = pd.read_sql_query("""select telco from scam_management_system join telcos on scam_management_system.telco_report_number = telcos.report_reference""", connection)
                global telco
                telco = telco_plot(telco_df).style('width: 100%; height: 100%')

     #  Put click event in all charts
    await client.connected(timeout = 15.0)
    await ui.run_javascript("""
        const top_scam_typology_chart = getElement(""" +str(top_scam_typology.id)+""").chart;
        top_scam_typology_chart.update({
            plotOptions: {
                series: {
                    point: {
                        events: {
                            click: function() {
                                Highcharts.each(Highcharts.charts, function(chart) {
                                    if (chart !== top_scam_typology_chart && chart.getSelectedPoints().length > 0) {
                                        chart.getSelectedPoints()[0].select(false);
                                    }
                                }, this);
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
        const telco_chart = getElement(""" +str(telco.id)+""").chart;
        telco_chart.update({
            plotOptions: {
                series: {
                    point: {
                        events: {
                            click: function() {
                                Highcharts.each(Highcharts.charts, function(chart) {
                                    if (chart !== telco_chart && chart.getSelectedPoints().length > 0) {
                                        chart.getSelectedPoints()[0].select(false);
                                    }
                                }, this);
                                this.select(null, true);
                                $.ajax({
                                    type: 'POST',
                                    url: '/env', 
                                    data: {
                                        condition: "TELCO",
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

# d1_content()

#   Updating of UI
def check_db_change():
    cursor.execute("SELECT UPDATE_TIME FROM information_schema.tables WHERE TABLE_SCHEMA = 'astro' AND TABLE_NAME = 'scam_management_system'")
    result = cursor.fetchone()
    latest_update_time = result[0]
    global initial_updated_time
    global df_test
    if latest_update_time != initial_updated_time:
        d1_content.refresh()
        initial_updated_time = latest_update_time
    

ui.timer(10.0, check_db_change)
        
ui.run(port = 8081)