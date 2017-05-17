from math import ceil
import time
import calendar, datetime

import pandas as pd

df = pd.read_csv("data/stock_market_data/aapl.csv")
svi = pd.read_csv("data/googletrends.csv")

def month_to_num(shortMonth):
    return{
        'Jan' : "01",
        'Feb' : "02",
        'Mar' : "03",
        'Apr' : "04",
        'May' : "05",
        'Jun' : "06",
        'Jul' : "07",
        'Aug' : "08",
        'Sep' : "09",
        'Oct' : "10",
        'Nov' : "11",
        'Dec' : "12"
    }[shortMonth]

def week_of_month(dt):
    """ Returns the week of the month for the specified date.
    """

    first_day = dt.replace(day=1)

    dom = dt.day
    adjusted_dom = dom + first_day.weekday()

    return int(ceil(adjusted_dom/7.0))

def convert_to_week(x):
    day = x.split("-",1)[0]
    if len(day) == 1:
        x="0"+x
    dt = datetime.datetime.strptime(x,"%d-%b-%y")
    return week_of_month(dt)

def convert_to_week2(x):
    dt = datetime.datetime.strptime(x, "%Y-%m-%d")
    return week_of_month(dt)

def add_decade(x):
    return "20"+x

def add_zero(x):
    if(len(x) == 1):
        return "0"+x

df['Day'], df['Mon'], df['Year'] = df.iloc[:,0].str.split('-').str

df['Day'] = df['Day'].apply(add_zero)
df['Mon'] = df['Mon'].apply(month_to_num)
df['Year'] = df['Year'].apply(add_decade)
df['Week'] = df.ix[:,0].apply(convert_to_week)

df1 = df.groupby(['Year','Mon','Week']).mean().reset_index()

svi['Year'], svi['Mon'], svi['Day'] = svi.iloc[:,0].str.split('-').str
svi['Week'] = svi.ix[:,0].apply(convert_to_week2)

df2 = pd.merge(df1, svi, how='inner', on=['Year','Mon','Week'])

df2.to_csv("test.csv")
