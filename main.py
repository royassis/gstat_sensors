import pandas as pd

#################
# Import data
#################
path = r"C:\Users\roy\Desktop\sensors.xlsx"
out_path = r"C:\Users\roy\Desktop\sensorsOUT.xlsx"

cols = ['id','lVarId', 'sensor_tagname', 'device', 'device_kind', 'device_number',
       'op_area','HMI', 'description','prod_line','sensor_kind', 'sensor_suffix']
df = pd.read_excel(path, sheet_name='working copy', usecols = cols ,index_col='id')

prod_line_values = ['CC01','CC02','CC03','CC04']
cond0 = (df['prod_line'].isin(prod_line_values)) & ()
#################
# Conditions
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
df["nogood"] = 0
df["nogood"][conds] = 1

#################
# Output to file
#################
df.sort_index().to_excel(out_path, index_label= 'id')