# # <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600&display=swap" rel="stylesheet">


# mapbox_access_token = 'pk.eyJ1IjoiZ2VuZ3l1ZG9uZyIsImEiOiJjbGdkcnhocXoxdzFwM2RvNnB3YmU0dm51In0.t_EXRVIhGE46Fq-3nnq_Uw'

#     #   Plotting Scattermapbox
#     heatmap = go.Figure()
#     heatmap.add_trace(go.Scattermapbox(
#         lat = lat_list,
#         lon = long_list,
#         mode = 'markers',

#         marker = go.scattermapbox.Marker(
#             autocolorscale = False,
#             cauto = True,
#             cmin = 0,
#             colorscale = [[0, "#BBD3F2"], [0.125, "#95B5DE"], [0.25, "#6E96CA"], [0.375, "#5B87C0"], [0.5, "#4777B6"], [0.625, "#3468AC"], [0.75, "#2A60A7"], [1, "#2058A2"]],    
#             color = scam_count_list,
            
#             size = scam_count_list,
#             sizeref = 3,
#             sizemode = 'area'
#         ), 
        
#         text = [hq_list[i] + '<br>' + 'Scam Cases: ' + str('{:,}'.format(scam_count_list[i])) for i in range(len(hq_list))],
#         hoverinfo = 'text',
#     )) 

#     heatmap.update_layout(
#         margin = {'l': 0, 'r': 0, 't': 0, 'b': 0},
#         autosize = True, 
#         mapbox = dict(
#             accesstoken = mapbox_access_token,
#             center = dict(
#                 lat = 1.3485143093190572,
#                 lon = 103.83056220992818,
#             ),
#             pitch = 0,
#             zoom = 10,
#             style = 'light'
#         ),
#     )

#     heatmap.update_traces(
#         hoverlabel = dict(
#             font = {'family': 'Roboto'}
#         )
#     )

#     return ui.plotly(heatmap)