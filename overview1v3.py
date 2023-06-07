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
SCAMTYPE_Friend.Impersonation.Scam='0'
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
        print(condition_value)

        #   Toggle 1 or 0 for that key
        if env_vars[condition_value] == '1':
            set_key('.env', condition_value, '0')
        elif env_vars[condition_value] == '0':
            set_key('.env', condition_value, '1')

        #   Set other fields as 0
        for key in env_vars.keys():
            if key.startswith(condition + "_") == False:
                set_key('.env', key, '0')
        
        print("Environment variable updated successfully\n")

        filtered_df = filter_data(df)
        await update_charts(filtered_df, condition)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def update_charts(filtered_df, condition):
    print("UPDATE CHART START")
    #   Total Report - Data Update
    total_report_value = total_reports(filtered_df)
    total_report_font_size = 4 - (len(str(total_report_value)) - 7)//2
    
    day_percentage, week_percentage, month_percentage, year_percentage = percentage(df)
    
    today_victim_count, past_day_victim_count,past_week_victim_count, past_month_victim_count, past_year_victim_count = victim_count(filtered_df)
    dod_background_color, dod_text_color = change_calculation(today_victim_count, past_day_victim_count)
    wow_background_color, wow_text_color = change_calculation(today_victim_count, past_week_victim_count)
    mom_background_color, mom_text_color = change_calculation(today_victim_count, past_month_victim_count)
    yoy_background_color, yoy_text_color = change_calculation(today_victim_count, past_year_victim_count)     
    
    #   Top Scam Typology Chart - Data Update
    top_scam_type_list, top_scam_type_num_report, top_scam_total_amount_scammed_per_type = top_scam_types_data(filtered_df)
    top_scam_typology.options['xAxis']['categories'] = top_scam_type_list
    top_scam_typology.options['series'][0]['data'] = top_scam_type_num_report
    top_scam_typology.options['series'][1]['data'] = top_scam_total_amount_scammed_per_type

    #   Scam Typology Chart - Data Update
    start_date, series_list = scam_typology_plot_data(filtered_df)
    scam_typology.options['plotOptions']['series']['pointStart'] = start_date
    scam_typology.options['series'].clear()
    scam_typology.options['series'].extend(series_list)

    #   Telco Chart - Data Update
    telco_chart_df = filtered_df.dropna(subset=['telco'])
    telco_name_list, telco_count_list = telco_plot_data(telco_chart_df)
    telco.options['xAxis']['categories'] = telco_name_list
    telco.options['series'][0]['data'] = telco_count_list
    
    
    #   Update other charts when "Telco Chart" is selected
    if condition == "TELCO":
        top_scam_typology.update()
        print("Top Scam Typology Chart Update DONE")
        scam_typology.update()  
        print("Scam Typology Chart Update DONE")
        total_report.set_text(total_report_value).style(f'font-size: {total_report_font_size}vw')
        print("Total Report Update DONE")
        
    #   Update other charts when "Scam Typology Chart" is selected
    elif condition=="SCAMTYPE":
        # print("SCAM TYPOLOGY OPTIONS", scam_typology.options['series'])
        scam_typology.update()
        print("Scam Typology Chart Update DONE")
        telco.update()
        print("Telco Chart Update DONE")
        total_report.set_text(total_report_value).style(f'font-size: {total_report_font_size}vw')
        print("Total Report Update DONE")
    
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
        padding: 0.4vw;
        
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
    telco_df = pd.read_sql_query("SELECT * FROM astro.telcos", connection)
    
    df['date_assigned'] = pd.to_datetime(df['date_assigned'])
    df = pd.merge(df, telco_df[['report_reference', 'telco']], left_on='telco_report_number', right_on='report_reference', how='left')
    df = df.drop('report_reference', axis=1)
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
                total_report_value = total_reports(filtered_df)
                total_report_font_size = 4 - (len(str(total_report_value)) - 7)//2
                
                #   Determining percentage values
                day_percentage, week_percentage, month_percentage, year_percentage = percentage(df)
                
                #   Determining percentages' background & text colours
                today_victim_count, past_day_victim_count,past_week_victim_count, past_month_victim_count, past_year_victim_count = victim_count(filtered_df)
                dod_background_color, dod_text_color = change_calculation(today_victim_count, past_day_victim_count)
                wow_background_color, wow_text_color = change_calculation(today_victim_count, past_week_victim_count)
                mom_background_color, mom_text_color = change_calculation(today_victim_count, past_month_victim_count)
                yoy_background_color, yoy_text_color = change_calculation(today_victim_count, past_year_victim_count)
                
                global total_report, dod_label, wow_label, mom_label, yoy_label
                
                with ui.element('div').style('margin: auto'):
                    ui.label('Total Reports').style('font-size: 2vw; font-weight: 500; color: #E6EAEF; letter-spacing: 0.15vw; margin-top: -6vh; margin-bottom: 2vh')
                    total_report = ui.label(total_report_value).style(f'font-size: {total_report_font_size}vw; color: #E6EAEF; margin-bottom: 2vh')
                    
                    with ui.row():
                        with ui.element('div').style(percentage_style).style(f'background-color: {dod_background_color}; border-color: {dod_background_color}'):
                            dod_label = ui.label(f'{day_percentage}% DoD').style(f'color: {dod_text_color}; letter-spacing: 0.2vw')
                        with ui.element('div').style(percentage_style).style(f'background-color: {wow_background_color}; border-color: {wow_background_color}'):
                            wow_label = ui.label(f'{week_percentage}% WoW').style(f'color: {wow_text_color}; letter-spacing: 0.2vw')
                    
                    with ui.row().style('margin-top: 2vh'):
                        with ui.element('div').style(percentage_style).style(f'background-color: {mom_background_color}; border-color: {mom_background_color}'):
                            mom_label = ui.label(f'{month_percentage}% MoM').style(f'color: {mom_text_color}; letter-spacing: 0.2vw')
                        with ui.element('div').style(percentage_style).style(f'background-color: {yoy_background_color}; border-color: {yoy_background_color}'):
                            yoy_label = ui.label(f'{year_percentage}% YoY').style(f'color: {yoy_text_color}; letter-spacing: 0.2vw')

                    
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
                telco_chart_df = filtered_df.dropna(subset=['telco'])
                global telco
                telco = telco_plot(telco_chart_df).style('width: 100%; height: 100%')

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