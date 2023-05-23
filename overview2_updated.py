from nicegui import app, ui, Client
import pymysql
import pandas as pd

from utils.d2_fundrecovery import *
from utils.d2_recoverytypology import *
from utils.d2_fundflow import *
from utils.d2_bankperformance import *
from utils.d2_recoverytrend import *
from utils.filter_data import *

from fastapi import HTTPException, Form
from dotenv import set_key, dotenv_values

with open('initialise_env.txt', 'r') as initialise_f:
    original_env = initialise_f.read()
    with open('.env', 'w') as env_f:
        env_f.write(original_env)

connection = pymysql.connect(host = '119.74.24.181', user = 'htx', password = 'Police123456', database = 'ASTRO')
cursor = connection.cursor()
cursor.execute("SELECT UPDATE_TIME FROM information_schema.tables WHERE TABLE_SCHEMA = 'astro' AND TABLE_NAME = 'scam_management_system'")
result = cursor.fetchone()
initial_updated_time = result[0]

@app.post("/env")
async def write_to_file(condition: str = Form(...), value: str = Form(...),):
    try:
        #might add a CONDITION= condition, with a whole dictionary to transform SCAMTYPE to scam_type to pass in the condition
        print(condition, value)
        env_vars = dotenv_values('.env') 
        if condition == "BANK":
            #reset everything to 0
            for key in env_vars.keys():
                set_key('.env', key, '0')
            
            if value != 'None Selected':
                #set selected rows to 1
                values = value.split(',')
                for i in values:
                    i = i.replace(" ", ",")
                    set_key('.env', 'BANK_'+i, '1')
            message = "Bank Environment variable updated successfully. "

        else:   
            condition_value = condition+"_"+value.replace(" ", ",")
            print("KEY_VALUE", {condition_value})

            # Toggle 1 or 0 for that key
            if env_vars[condition_value] == '1':
                set_key('.env', condition_value, '0')
            elif env_vars[condition_value] == '0':
                set_key('.env', condition_value, '1')

            #Set other fields as 0
            for key in env_vars.keys():
                if key.startswith(condition+"_") == False:
                    set_key('.env', key, '0')
            message = "Environment variable updated successfully. "
        
        

        filtered_df = filter_data(df)
        await update_charts(filtered_df, condition)
            
        return {"message": message}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def update_charts(filtered_df, condition):
    print("UPDATE CHART START")

    #Recovery Typology Chart
    category_list, data_list = recovery_typology_data(filtered_df)
    rbt.options['series'][0]['data'] = data_list
    rbt.options['xAxis']['categories'] = category_list
    print("RBT CHART DATA DONE")

    #Fund Flow Chart
    ffp.options['series'][0]['data'] = fundflow_data(filtered_df)
    print("FFP CHART DATA DONE")

    #Fund Recovery Chart
    amount_scammed, amount_recover, amount_recover_percentage, amount_scammed_percentage = fund_recovery_data(filtered_df)
    fr.options['title']['text'] = f'Scam Amount <br> ${amount_scammed:,} <br><br><b>Fund Recovery</b><br><br> Recovered Amount <br> ${amount_recover:,}'
    fr.options['series'][0]['data'][0]['y'] = amount_recover_percentage
    fr.options['series'][0]['data'][1]['y'] = amount_scammed_percentage
    print("FR CHART DATA DONE")
    
    #Bank Performance Table 
    new_bp_df = bank_performance_data(filtered_df)
    grid.options['rowData'] = new_bp_df.to_dict('records')
    print("GRID DATA DONE")

    #Recovery Trend Chart
    amount_recovered_list = recovery_trend_data(filtered_df)[3]
    rt.options['series'][0]['data'] = amount_recovered_list
    print("RECOVERY TREND DATA DONE")

    if condition == "OVERSEASLOCAL":
        rbt.update()
        grid.update()
        print("Updated based on OVERSEASLOCAL")
    elif condition=="SCAMTYPE": 
        ffp.update()
        grid.update()
        print("Updated based on SCAMTYPE")
    elif condition=="BANK":
        ffp.update()
        rbt.update()
        print("Updated based on BANK")
    fr.update()
    rt.update()
    print("UPDATE CHART END")


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
    global df
    df= pd.read_sql_query("SELECT * FROM astro.scam_management_system", connection)
    filtered_df = filter_data(df)

    #-------------------------------------------------------------------------------------------------------------------------------------------------------------#
    
    with ui.row().style('height: 60vh; width: 100%; flex-wrap: nowrap'):
        
        
        #   Recovery by Typology Plot
        division = ui.element('div')
        with division.style(div_general_style).style('height: 100%; width: 30%'):
            global rbt 
            rbt = recovery_by_typology_plot(filtered_df).style('height: 100%')
            

        with ui.column().style('width: 40%; height:100%; flex-wrap: nowrap; gap:0rem;').classes('items-center'):
            #   ASC Logo
            with ui.element('div').style('height: 10vh; width: 100%'):
                with ui.row().classes('items-center justify-center'): 
                    ui.image('https://www.police.gov.sg/-/media/Spf/Archived/2021-10-28/SPF200/Homepage/Large-SPF-Logo.ashx?h=296&w=314&la=en&hash=5D66E7698CEFB5D7B9028D9905C03967').style('width: 5vw')
                    ui.label('ANTI-SCAM CENTRE').style('font-family: Michroma; font-size: 1.1vw; color: #CED5DF; letter-spacing: 0.2vw; word-spacing: 0.3vw; font-weight: bold;')

            #   Fund Recovery Progress
            with ui.element('div').classes('items-center').style('align: center; height: 50vh; width: 100%'):
                global fr
                fr = fund_recovery_plot(filtered_df).style('position:relative; width: 100%; height: 100%')

        #   Bank's Performance
        with ui.element('div').style(div_general_style).style('width: 30%'):
            with ui.row().classes('justify-between items-center').style('flex-wrap: nowrap;'):
                ui.label("Bank's Performance").style(label_style)
                ui.select(['min', 'max', 'sum', 'mean'], value='mean', on_change = lambda x:change_stats(x.value, grid)).style('background-color: #87c6e6 !important; border-radius:5px;').classes('px-3 w-28')
            global grid
            grid = bank_performance_table(df).style('height:85%;')
                # .style('height: 50vh;') #Cant get the height correct on differnet size screens  
            
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------#

    with ui.row().style('height: 34.5vh; width: 100%; flex-wrap: nowrap;'):
        
        #   Recovery Trend Plot
        with ui.element('div').style(div_general_style).style('width: 70%'):
            global rt
            rt = recovery_trend_plot(df).style('height: 100%; width: 100%')
        
        #   Breakdown of Fund Flow Plot
        with ui.element('div').style(div_general_style).style('width: 30%'):
            global ffp
            ffp = fund_flow_plot(filtered_df).style('height: 100%; width: 100%')
            
    ### Put Click event in all charts
    await client.connected(timeout = 15.0)
    print("Client Connected")
    await ui.run_javascript("""
        const RBT_chart = getElement(""" +str(rbt.id)+""").chart;
        RBT_chart.update({
            plotOptions: {
                series: {
                    point: {
                        events: {
                            click: function() {
                                this.select(null, true);
                                Highcharts.each(Highcharts.charts, function(chart) {
                                    if (chart !== RBT_chart && chart.getSelectedPoints().length > 0) {
                                        chart.getSelectedPoints()[0].select(false);
                                    }
                                }, this);
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

        const grid = getElement("""+str(grid.id)+""");
        grid.gridOptions.onRowClicked = function(event) {
            const selectedRows = grid.gridOptions.api.getSelectedRows();
            let selectedBanks;
            if (selectedRows.length === 0){
                selectedBanks = 'None Selected'
                console.log("if ran");
            } else {
                selectedBanks = selectedRows.map(row => row['Bank']).join(',');
                console.log("else ran");
            }
            console.log(selectedBanks);
            
            $.ajax({
                type: 'POST',
                url: '/env', 
                data: {
                    condition: "BANK",
                    value: selectedBanks,
                },
                success: function (response) {
                    console.log(response);
                },
                error: function (xhr, status, error) {
                    console.log(error);
                }
            })
        };

        const FFP_chart = getElement(""" +str(ffp.id)+""").chart;
        FFP_chart.update({
            plotOptions: {
                series: {
                    point: {
                        events: {
                            click: function() {
                                Highcharts.each(Highcharts.charts, function(chart) {
                                    if (chart !== FFP_chart && chart.getSelectedPoints().length > 0) {
                                        chart.getSelectedPoints()[0].select(false);
                                    }
                                }, this);
                                this.select(null, true);
                                $.ajax({
                                    type: 'POST',
                                    url: '/env', 
                                    data: {
                                        condition: "OVERSEASLOCAL",
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
   
def check_db_change():
    cursor.execute("SELECT UPDATE_TIME FROM information_schema.tables WHERE TABLE_SCHEMA = 'astro' AND TABLE_NAME = 'scam_management_system'")
    result = cursor.fetchone()
    latest_update_time = result[0]
    global initial_updated_time
    global df_test
    if latest_update_time != initial_updated_time:
        d2_content.refresh()
        initial_updated_time = latest_update_time

ui.timer(20.0, check_db_change)
ui.run(port = 8082)