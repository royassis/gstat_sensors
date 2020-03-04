# Imports and options
import os
import re
import pandas as pd
import numpy as np
from functions import get_col_widths

pd.set_option('mode.chained_assignment', None)

#################
# Close excel files
#################
os.system("taskkill /f /im " + 'EXCEL.exe')

#################
# Set in and out patchs
#################
base_dir = r'data'
in_file = 'sensors_in.xlsx'
in_path =  os.path.join(base_dir,in_file)

out_file = 'sensors_out.xlsx'
out_path = os.path.join(base_dir,out_file)

#################
# Read file
#################
cols = ['id', 'lVarId', 'sensor_tagname', 'HMI', 'desc']
df = pd.read_excel(in_path, sheet_name='sensors', usecols=cols, index_col='id')

df['sensor_tagname'] = df['sensor_tagname'].str.lower()
df = df.drop_duplicates("sensor_tagname").replace('^$', np.nan, regex=True)

#################
# Breakdown tag with regex to columns (op_area_name, op_area_number etc...)
#################
breakdown = df.sensor_tagname.str.extract(r"(?P<prefix>^.*?)"
                                          r"(?P<op_area_name>[A-z][A-z])"
                                          r"(?P<op_area_number>\d\d)"
                                          r"(?P<device_kind>[A-z][A-z])"
                                          r"(?P<device_number>..)"
                                          r"(?P<suffix>.*$)") \
    .apply(lambda x: x.str.lower().str.strip('_'))

df = df.merge(breakdown, right_index=True, left_index=True)

#################
# Get only elevent sensors (sensors in non relevent areas were dropped)
#################
regex_token_list = ['(CC\d\d(cd|cr|cv|wc|wd|xx))',
                    '(MR0[24])',
                    '(PS01(mp|tk|xx)\d\d)']
regex = r"|".join(regex_token_list)
cond = (df['sensor_tagname'].str.contains(regex, flags=re.IGNORECASE, na=False))

#################
# Edit sensor_name - somes small cahnges + create a generic sensor_name column
#################
# small cahnge 1
prefix = df['prefix']
prefix = prefix.replace(r'^d$', '', regex=True)

# small cahnge 2
suffix = df['suffix']
suffix = suffix.replace("\s*jdc\s*", "", regex=True)

# big cahnge - create a generic sensor_name column
df = df[cond].sort_values(['HMI', 'op_area_name', 'device_kind', 'device_number', 'suffix'])
df["sensor_name"] = (prefix + df['op_area_name'] + df['op_area_number'] + df['device_kind'] + suffix).str.upper()

# after retrospective work some sensor names where manual changed, the changes are taken from a mapper file
mapper = pd.read_csv(r'resources/sensor_name_mapper.csv', usecols = ['sensor_tagname', 'sensor_name_edited'])\
    .apply(lambda x: x.str.lower())\
    .set_index('sensor_tagname').iloc[:,0]

mapper[mapper.isna()] = mapper[mapper.isna()].index.to_list()

df["sensor_name_edited"] = df['sensor_tagname'].replace(mapper)

#################
# Output to file
#################
# Set the column order
columns = ['lVarId', 'sensor_tagname', "sensor_name", "sensor_name_edited", 'HMI', 'prefix', 'op_area_name',
           'op_area_number', 'device_kind',
           'device_number', 'suffix', 'desc']

df = df[columns]

# Set writer
writer = pd.ExcelWriter(out_path, engine='xlsxwriter')
df.to_excel(writer, index_label='id', sheet_name='data', columns=columns)

workbook = writer.book
worksheet = writer.sheets['data']

# Freeze top row
worksheet.freeze_panes(1, 0)

# Autowidth columns
for i, width in enumerate(get_col_widths(df)):
    worksheet.set_column(i, i, width * 1.1)

# Save
writer.save()

#################
# Lunch excel file
#################
full_out_path = os.path.join(os.getcwd(), out_path)
os.system(full_out_path)
