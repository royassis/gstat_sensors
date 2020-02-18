import pandas as pd
from sqlalchemy import create_engine

db_name = 'sensors'
tbl_name = 'olap'

sensors_path = r'C:\Users\User\PycharmProjects\gstat_sensors\data\sensors_base.xlsx'
sensors_desc_path = r'C:\Users\User\PycharmProjects\gstat_sensors\data\sensor_desc.xlsx'
sensors_lines_path = r'C:\Users\User\PycharmProjects\gstat_sensors\data\lines.xlsxr'

###################
## ETL from excel
###################

# Extact - read excel files
customers = pd.read_excel(r'C:\Users\User\PycharmProjects\myETL\cutomers.xlsx').rename({"id":"cust_id"},axis = 1)
transactions = pd.read_excel(r'C:\Users\User\PycharmProjects\myETL\transactions.xlsx').rename({"id":"tran_id"},axis = 1)

# Transform - join and groupby + Other transformations
customers["full_name"] = customers["first_name"] +' '+ customers["last_name"]
joined = customers.merge(transactions, left_on = "cust_id", right_on = "cust_id" )\
                  .groupby("cust_id").agg({'amount':'sum','date':'max','full_name':pd.Series.mode})\
                  .reset_index()


# Load - push to db
connstr = 'mssql+pyodbc://DESKTOP-TL42QJI\SQLEXPRESS/{}?driver=SQL+Server+Native+Client+11.0'.format(db_name)
engine = create_engine(connstr)
joined.to_sql(tbl_name, con=engine, if_exists= 'append')

