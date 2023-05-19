from nicegui import ui
import pandas as pd
import folium
from folium import Tooltip

def heatmap(df): 
    #   Data Cleaning
    df_division = df[['division_assigned']].copy()
    df_division.dropna(subset = ['division_assigned'], inplace = True)
    df_division = df_division[df_division.division_assigned != '-']
    df_division = df_division.apply(lambda x: x.str.upper() if x.dtype == "object" else x)

    values_to_be_replaced = ['CAD', 'ASCOM', 'CID']
    for value in values_to_be_replaced:
        df_division = df_division.replace('.*{}.*'.format(value), value, regex=True)
    df_division = df_division.replace(['ASCOM', 'ASD', 'CID', 'TCIB', 'UMSF', 'ICB', 'APD', 'ACB', 'GOIS'], 'A')

    df_division = df_division.groupby('division_assigned').size().reset_index(name = 'No_of_cases_per_division')
    df_division = df_division.drop(index = [0,4,5,7,9,12,13,15,16,17,18,19]) #  How to replace the values/group them together as some are vv stubborn
    df_division = df_division.sort_values('No_of_cases_per_division', ascending = False)
    df_division = df_division.reset_index(drop = True)

    df_latlong = pd.DataFrame({'division_assigned': ['F', 'G', 'J', 'A', 'L', 'E', 'D', 'CAD'],
                            'latitude': ['1.3849575528196754', '1.3328211729396362', '1.3511672381459414', '1.2787649220017296', '1.4334351610154739', '1.3130793731128103', '1.3173533926882381', '1.278724700500034'],
                            'longitude': ['103.84533643093292', '103.93718201189469', '103.7023869984011', '103.8397629560721', '103.77890231189434', '103.8467156436066', '103.76671172354014', '103.8393872523757'],
                            'name': ['Ang Mo Kio Police Division HQ', 'Bedok Police Division HQ', 'Jurong Police Division HQ', 'Central Police Division HQ', 'Woodlands Police Division HQ', 'Tanglin Police Division HQ', 'Clementi Police Division HQ', 'Commercial Affairs Department']})
    df_division = pd.merge(df_division, df_latlong, on = 'division_assigned')

    lat_list = df_division['latitude'].tolist()
    long_list = df_division['longitude'].tolist()
    hq_list = df_division['name'].tolist()
    scam_count_list = df_division['No_of_cases_per_division'].tolist()

    #   Centering map
    y_map= 1.3100143093190572
    x_map= 103.93056220992818

    #   Creating Map
    mymap = folium.Map(location=[y_map, x_map], 
                        zoom_start=11,
                        tiles=None,
                        draw_control=False,
                        measure_control=False,
                        fullscreen_control=False,)
    folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(mymap)

    #   Plotting Scattermapbox
    for i in range(0, len(lat_list)):
        t = hq_list[i] + '<br>'+ str(scam_count_list[i])
        folium.Circle(
            location = [lat_list[i],long_list[i]],
            tooltip = Tooltip(t, style = 'font-size:15px'),
            radius = float(scam_count_list[i])*0.3,
            stroke = False,
            fill = True,
            fill_opacity = float(scam_count_list[i])*0.00005,
            color = "#115fd4",

            fill_color = "#115fd4"
        ).add_to(mymap)
    title_html = '''<h3 style = "text-align:center" >Heatmap</h3>'''
    mymap.get_root().html.add_child(folium.Element(title_html))

    return ui.html(mymap._repr_html_())

    