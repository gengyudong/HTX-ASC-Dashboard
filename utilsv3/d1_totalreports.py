from datetime import timedelta, date

def total_reports(df):
    df_report = df.drop_duplicates(subset=['report_number'])
    total_report = len(df_report.index)
    total_report = '{:,}'.format(total_report)
    
    return total_report


def victim_count_calculation(df, date):
    past_df = df[df.date_assigned == date]
    victim_count = len(past_df.index)
    
    return victim_count

def victim_count(df):
    today = date.today()
    today_victim_count = victim_count_calculation(df, today)
    
    #   Scam Count - Past Day 
    past_day = today - timedelta(days = 1)
    past_day_victim_count = victim_count_calculation(df, past_day)
    
    #   Scam Count - Past Week
    past_week = today - timedelta(days = 7)
    past_week_victim_count = victim_count_calculation(df, past_week)
    
    #   Scam Count - Past Month
    past_month = today - timedelta(days = 30)
    past_month_victim_count = victim_count_calculation(df, past_month)
    
    #   Scam Count - Past Year
    past_year = today - timedelta(days = 365)
    past_year_victim_count = victim_count_calculation(df, past_year)
    
    return today_victim_count, past_day_victim_count, past_week_victim_count, past_month_victim_count, past_year_victim_count
         
                
def percentage_calculation(today, past):
    if past == 0:
        return 0
    
    else:
        change = today - past
        percentage_change = abs(change / past) * 100
        percentage_change = round(percentage_change, 1)

        return percentage_change

def percentage(df):
    today_victim_count, past_day_victim_count,past_week_victim_count, past_month_victim_count, past_year_victim_count = victim_count(df)
    
    day_percentage = percentage_calculation(today_victim_count, past_day_victim_count)
    week_percentage = percentage_calculation(today_victim_count, past_week_victim_count)
    month_percentage = percentage_calculation(today_victim_count, past_month_victim_count)
    year_percentage = percentage_calculation(today_victim_count, past_year_victim_count)
    
    return day_percentage, week_percentage, month_percentage, year_percentage


def arrow_type_calculation(today_victim_count, past_victim_count):
    change = today_victim_count - past_victim_count
    if change > 0:
        return 'arrow_upward'
    
    if change < 0:
        return 'arrow_downward'
    
    else:
        return "remove"
    
def arrow_function(df):
    today_victim_count, past_day_victim_count,past_week_victim_count, past_month_victim_count, past_year_victim_count = victim_count(df)
    
    day_arrow = arrow_type_calculation(today_victim_count, past_day_victim_count)       
    week_arrow = arrow_type_calculation(today_victim_count, past_week_victim_count)
    month_arrow = arrow_type_calculation(today_victim_count, past_month_victim_count)
    year_arrow = arrow_type_calculation(today_victim_count, past_year_victim_count)
    
    return day_arrow, week_arrow, month_arrow, year_arrow