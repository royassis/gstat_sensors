import pandas as pd
import os

base_folder = 'data'
# ----------------------------- Read sensor descriptions file ----------------------------- #
in_file = r"sensor_desc.xlsx"
in_path = os.path.join(base_folder,in_file)

sensor_desc = pd.read_excel(in_path)
sensor_desc = sensor_desc.drop_duplicates('sensor_name_edited')

cols = ['sensor_name_edited','desc']
sensor_desc = sensor_desc[cols]

# ----------------------------- Read sensor names file ----------------------------- #
in_file = r"sensors_out.xlsx"
in_path = os.path.join(base_folder,in_file)

sensors = pd.read_excel(in_path)
sensors = sensors.drop('desc',axis = 1)

# ----------------------------- merge files and output to csv ----------------------------- #
merged = sensors.merge(sensor_desc, how = 'left', left_on = 'sensor_name_edited', right_on = 'sensor_name_edited')
cols = ['id','lVarId','HMI','op_area_name','op_area_number','device_kind','device_number','sensor_tagname','sensor_name','sensor_name_edited','desc']

out_file = r"sensor_joined.csv"
out_path = os.path.join(base_folder,in_file)
merged[cols].to_csv(out_path)