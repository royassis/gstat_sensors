import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import time
import os



def main ():
    db_name = 'sensors'
    log_tbl = 'logs'

    l = [
        ['lines',r'C:\Users\User\PycharmProjects\gstat_sensors\data\lines.xlsx'],
        ['sensor_data', r'C:\Users\User\PycharmProjects\gstat_sensors\data\sensors_out.xlsx'],
        ['sensor_desc' , r'C:\Users\User\PycharmProjects\gstat_sensors\data\sensor_desc.xlsx']
    ]


    # Push to db
    connstr = 'mssql+pyodbc://DESKTOP-TL42QJI\SQLEXPRESS/{}?driver=SQL+Server+Native+Client+11.0'.format(db_name)
    engine = create_engine(connstr)

    file_update_timestamp = os.path.getatime(r'C:\Users\User\PycharmProjects\gstat_sensors\data\sensorsOUT.xlsx')
    file_update_datetime = datetime.fromtimestamp(file_update_timestamp).replace(second =0, microsecond= 0)

    last_log_datetime = (pd.read_sql_query('SELECT MAX(logtime) FROM logs',connstr).values[0][0])

    if last_log_datetime > file_update_datetime:

        for tbl,path in l:
            log_data = pd.DataFrame([[datetime.now(), tbl]], columns = ['logtime','tablename'])
            log_data.to_sql(log_tbl, con=engine, if_exists= 'append', index= False)
            df = pd.read_excel(path)
            df.to_sql(tbl, con=engine, if_exists= 'replace', index_label= 'id', index= False)

if __name__ == '__main__':
    main()







