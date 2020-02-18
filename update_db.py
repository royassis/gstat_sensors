import pandas as pd
from sqlalchemy import create_engine

db_name = 'sensors'

dict = {
    'lines' : r'C:\Users\User\PycharmProjects\gstat_sensors\data\lines.xlsx',
    'sensor_data' : r'C:\Users\User\PycharmProjects\gstat_sensors\data\sensors_base.xlsx',
    'sensor_desc' : r'C:\Users\User\PycharmProjects\gstat_sensors\data\sensor_desc.xlsx'
}


sensors =       pd.read_excel(sensors_path)
sensors_desc =  pd.read_excel(sensors_desc_path)
sensors_lines = pd.read_excel(sensors_lines_path)

# Push to db
connstr = 'mssql+pyodbc://DESKTOP-TL42QJI\SQLEXPRESS/{}?driver=SQL+Server+Native+Client+11.0'.format(db_name)
engine = create_engine(connstr)

for tbl in tbl_names:
    sensors.to_sql(tbl, con=engine, if_exists= 'replace')

