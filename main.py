import pandas as pd
from . import functions

#################
# Import data
#################
path = r"C:\Users\roy\Desktop\sensors.xlsx"
out_path = r"C:\Users\roy\Desktop\sensorsOUT.xlsx"

cols = ['id','lVarId', 'sensor_tagname', 'device', 'device_kind', 'device_number',
       'op_area','HMI', 'description','prod_line','sensor_kind', 'sensor_suffix']
df = pd.read_excel(path, sheet_name='working copy', usecols = cols ,index_col='id')

#################
# Relevent sensors conditions
#################
op_area_values = ['CC01','CC02','CC03','CC04']
device_kind_values = ['CD','CR','CV','WC','WD']
cond0 = (df['op_area'].isin(op_area_values)) & (df['device_kind'].isin(device_kind_values))

df = df[cond0].sort_values(['op_area','device_kind','device_number','sensor_suffix'])

#################
# Is ok Conditions
#################

# Condition 1 - Sensor tagname must adhere to the following regex
regex = r'^[A-z][A-z]\d\d[A-z][A-z]\d\d.*$'
cond1 = ~ df.sensor_tagname.dropna().str.match(regex, na= False)

# Condition 2 - Same כלי with multiple same name sensors
cond2 = df.duplicated(['op_area','sensor_kind','device_kind','device_number'], keep = False)

# Condition 3 - Suffixes that show only for one device
result = df.groupby(["sensor_suffix"])["sensor_suffix"].count()
suspicious_suffixes = result[result == 1].index
cond3= df["sensor_suffix"].isin(suspicious_suffixes)

conds = cond1 | cond2 | cond3

#################
# Apply masks
#################
df["bad regex"] = 0
df["redundent suffix"] = 0
df["lonly suffix"] = 0

df["bad regex"][cond1] = 1
df["redundent suffix"][cond2] = 1
df["lonly suffix"][cond3] = 1


#################
# Output to file
#################
writer = pd.ExcelWriter(out_path, engine='xlsxwriter')
df.to_excel(writer, index_label= 'id', sheet_name='Sheet1')

workbook  = writer.book
worksheet = writer.sheets['Sheet1']

format1 = workbook.add_format({'bg_color': '#FFC7CE',
                               'font_color': '#9C0006'})

range = 'M2:O3000'
worksheet.conditional_format(range, {'type': 'cell',
                                         'criteria': '=',
                                         'value': 1,
                                         'format': format1})

worksheet.freeze_panes(1, 0)


for i, width in enumerate(functions.get_col_widths(df)):
    worksheet.set_column(i, i, width)

writer.save()