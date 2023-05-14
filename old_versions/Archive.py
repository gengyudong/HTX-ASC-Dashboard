
##  Getting x & y data ready
        # today = date.today()
        # dates_temp = []
        # dates = []
        # no_of_cases = []

        # for i in range(30):
        #     previous_date = today - timedelta(days = i)
        #     previous_date = previous_date
        #     dates_temp.append(previous_date)

        # dates_temp.reverse()

        # for date in dates_temp:
        #     df_for_this_date = df[df.date_assigned == date]
        #     no_of_cases_on_this_date = len(df_for_this_date.index)
        #     no_of_cases.append(no_of_cases_on_this_date)

        # for date in dates_temp:
        #         date = date.strftime("%#Y-%#m-%d")
        #         dates.append(date)
      



        # for i in range(len(df_day.index)):
        #     day = df_day['date'][i]
        #     day = day.strftime("%Y-%m-%d")
        #     days.append(day)
            
        #     cases = df_day['no_of_cases'][i]
        #     no_of_cases.append(cases)


#---------------------------------------------------------------------------------------------------------------------------------------------------------


# colorscale = [[0, "#fff5f0"], [0.125, "#fee0d2"], [0.25, "#fcbba1"], [0.375, "#fc9272"], [0.5, "#fb6a4a"], [0.625, "#ef3b2c"], [0.75, "#cb181d"], [1, "#67000d"]],



#---------------------------------------------------------------------------------------------------------------------------------------------------------



# from nicegui import ui

# with ui.input('Date') as date:
#     with date.add_slot('append'):
#         ui.icon('edit_calendar').on('click', lambda: menu.open()).classes('cursor-pointer')
#     with ui.menu() as menu:
#         ui.date(on_change=menu.close).bind_value(date)
        
# ui.run(port = 8082)