import acquire
from datetime import datetime
import pandas as pd


def prep_store():
    df_sales = acquire.get_all('sales')
    df_items = acquire.get_all('items')
    df_stores =  acquire.get_all('stores')

    # Merge sales and stores
    sales_and_stores = pd.merge(df_sales, 
                            df_stores,
                            how="inner",
                            left_on="store",
                            right_on="store_id")

    # Merge sales_and_stores with itesms
    everything = pd.merge(sales_and_stores,
                        df_items,
                        how="inner",
                        left_on="item",
                        right_on="item_id")
                        
    # Change sale_date to a date time and then set as index
    everything.sale_date = pd.to_datetime(everything.sale_date, format='%a, %d %b %Y %H:%M:%S %Z')
    everything = everything.set_index('sale_date').sort_index()

    # Create a month, day, and weekday column/  create a sales_total columns
    everything['month'] = everything.index.month
    everything['day'] = everything.index.day
    everything['weekday'] = everything.index.day_name()
    everything['sales_total'] = everything.sale_amount + everything.item_price

    return everything


def prep_electricity():
    electricity_consumption = pd.read_csv("https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv")

    # format date to datetime type and set as index
    electricity_consumption.Date = pd.to_datetime(electricity_consumption.Date, format='%Y-%m-%d')
    electricity_consumption = electricity_consumption.set_index('Date').sort_index()

    # create month and year columns
    electricity_consumption['month'] = electricity_consumption.index.month
    electricity_consumption['year'] = electricity_consumption.index.year

    # fill nulls
    electricity_consumption = electricity_consumption.fillna(0)

    return electricity_consumption