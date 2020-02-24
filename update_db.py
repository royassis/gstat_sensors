import pandas as pd
from sqlalchemy import create_engine



def main ():
    db_name = 'sensors'
    log_tbl = 'logs'

    l = [
        ['lines',r'C:\Users\User\PycharmProjects\gstat_sensors\data\lines.xlsx'],
        ['sensor_data', r'C:\Users\User\PycharmProjects\gstat_sensors\data\sensors_base.xlsx'],
        ['sensor_desc' , r'C:\Users\User\PycharmProjects\gstat_sensors\data\sensor_desc.xlsx']
    ]


    # Push to db
    connstr = 'mssql+pyodbc://DESKTOP-TL42QJI\SQLEXPRESS/{}?driver=SQL+Server+Native+Client+11.0'.format(db_name)
    engine = create_engine(connstr)

    for tbl,path in l:
        df = pd.read_excel(path)
        df.to_sql(tbl, con=engine, if_exists= 'replace', index_label= 'id', index= False)



if __name__ == '__main__':
    main()







