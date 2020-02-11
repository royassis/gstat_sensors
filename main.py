#################
# Imports and Settings
#################
import pandas as pd
from functions import get_col_widths, get_range
import os
import psutil

pd.set_option('mode.chained_assignment', None)

#################
# Import data
#################
path = r"data/sensors.xlsx"
out_path = r"data/sensorsOUT.xlsx"

cols = ['id', 'lVarId', 'sensor_tagname', 'HMI', 'description', 'prod_line']
df = pd.read_excel(path, sheet_name='working copy', usecols=cols)

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

# Add sensorname column
df["sensor_name"] = (df['op_area_name'] + df['op_area_number'] + df['device_kind'] + df['suffix']).str.upper()

#################
# Get only elevent sensors
#################
op_area_values = ['cc']
device_kind_values = ['cd', 'cr', 'cv', 'wc', 'wd']
cond = (df['op_area_name'].isin(op_area_values)) & (df['device_kind'].isin(device_kind_values)) | \
       (df['sensor_tagname'].str.contains(r'MR02', na=False)) | \
       (df['sensor_tagname'].str.contains(r'MR04TK', na=False)) | \
       (df['sensor_tagname'].str.contains(r'PS01MP', na=False))

df = df[cond].sort_values(['HMI', 'op_area_name', 'device_kind', 'device_number', 'suffix'])

#################
# Is ok Conditions
#################
## Condition 1 - Sensor tagname must adhere to the following regex
# regex = r'^[A-z][A-z]\d\d[A-z][A-z]\d\d.*$'
# cond1 = ~ df.sensor_tagname.dropna().str.match(regex, na=False)

# Condition 2 - Same כלי with multiple same name sensors
cond2 = df.duplicated(['op_area_name', 'op_area_number', 'device_kind', 'device_number', 'suffix'], keep=False)

# Condition 3 - Suffixes that show only for one device
result = df.groupby(["suffix"])["suffix"].count()
suspicious_suffixes = result[result == 1].index
cond3 = df["suffix"].isin(suspicious_suffixes)

conds = cond2 | cond3

#################
# Apply conditions
#################
df["redundent suffix"] = 0
df["lonly suffix"] = 0
df["problem"] = 0

df["redundent suffix"][cond2] = 1
df["lonly suffix"][cond3] = 1
df["problem"][conds] = 1

#################
# Output to file and format excel
#################
# Set the column order
columns = ['id', 'lVarId', 'sensor_tagname',"sensor_name", 'HMI','prefix', 'op_area_name', 'op_area_number', 'device_kind',
       'device_number', 'suffix','description', 'prod_line', 'redundent suffix', 'lonly suffix','problem']

# Set writer
writer = pd.ExcelWriter(out_path, engine='xlsxwriter')
df.to_excel(writer, index_label='id', sheet_name='Sheet1', columns = columns)

workbook = writer.book
worksheet = writer.sheets['Sheet1']

# Set cell format
format1 = workbook.add_format({'bg_color': '#FFC7CE',
                               'font_color': '#9C0006'})

# Set cell range
a, b, c, d = len(df.columns) - 1, 2, \
             len(df.columns) + 1, len(df) + 2

range = get_range(a, b, c, d)

# Apply format to range
worksheet.conditional_format(range, {'type': 'cell',
                                     'criteria': '=',
                                     'value': 1,
                                     'format': format1})

# Freeze top row
worksheet.freeze_panes(1, 0)

# Autowidth columns
for i, width in enumerate(get_col_widths(df)):
    worksheet.set_column(i, i, width * 1.1)

# Save
writer.save()


#################
# Close excel files
#################
if "EXCEL.EXE" in (p.name() for p in psutil.process_iter()):
    os.system("taskkill /f /im " + 'EXCEL.exe')


#################
# Lunch excel file
#################
full_out_path = os.path.join(os.getcwd(),out_path )
os.system(full_out_path)


