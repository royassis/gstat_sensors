import os
import re
import pandas as pd
from functions import get_col_widths
pd.set_option('mode.chained_assignment', None)

#################
# Close excel files
#################
os.system("taskkill /f /im " + 'EXCEL.exe')


#################
# Import data
#################
path = r"data/sensorsIN.xlsx"
out_path = r"data/sensorsOUT.xlsx"

cols = ['id', 'lVarId', 'sensor_tagname', 'HMI']
df = pd.read_excel(path, sheet_name='sensors', usecols=cols, index_col = 'id')

#################
# Breakdown tag with regex
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
# Get only elevent sensors
#################
regex_token_list = ['(CC\d\d(cd|cr|cv|wc|wd|xx))',
                   '(MR\d\dTK)',
                   '(PS01MP)']
regex = r"|".join(regex_token_list)
cond = (df['sensor_tagname'].str.contains(regex,flags = re.IGNORECASE, na=False))


#################
# Prepare for output
#################
df = df[cond].sort_values(['HMI', 'op_area_name', 'device_kind', 'device_number', 'suffix'])
df["sensor_name"] = (df['prefix'] + df['op_area_name'] + df['op_area_number'] + df['device_kind'] + df['suffix']).str.upper()
df["sensor_name_edited"] = df["sensor_name"]
df = df.drop_duplicates('sensor_tagname')

#################
# Output to file
#################
# Set the column order
columns = ['lVarId', 'sensor_tagname',"sensor_name","sensor_name_edited", 'HMI','prefix', 'op_area_name', 'op_area_number', 'device_kind',
       'device_number', 'suffix']

df = df[columns]

# Set writer
writer = pd.ExcelWriter(out_path, engine='xlsxwriter')
df.to_excel(writer, index_label='id', sheet_name='data', columns = columns)

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
full_out_path = os.path.join(os.getcwd(),out_path )
os.system(full_out_path)

