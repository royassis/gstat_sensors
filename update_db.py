import pandas as pd
from sqlalchemy import create_engine

db_name = 'sensors'

l = [
    ['lines',r'C:\Users\User\PycharmProjects\gstat_sensors\data\lines.xlsx'],
    ['sensor_data', r'C:\Users\User\PycharmProjects\gstat_sensors\data\sensors_base.xlsx'],
    ['sensor_desc' , r'C:\Users\User\PycharmProjects\gstat_sensors\data\sensor_desc.xlsx']
]


# Push to db
connstr = 'mssql+pyodbc://DESKTOP-TL42QJI\SQLEXPRESS/{}?driver=SQL+Server+Native+Client+11.0'.format(db_name)
engine = create_engine(connstr)

for d in l:
    df = pd.read_excel(d[1])
    df.to_sql(d[0], con=engine, if_exists= 'replace')

