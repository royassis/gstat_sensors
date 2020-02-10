import pandas as pd

#################
# Import data
#################
path = r"C:\Users\roy\Desktop\sensors.xlsx"
out_path = r"C:\Users\roy\Desktop\sensorsOUT.xlsx"

df = pd.read_excel(path, sheet_name='working copy', index_col='id')
original = df.copy()

#################
# Conditions
#################

# Condition 1 - Sensor tagname must adhere to the following regex
regex = r'^[A-z][A-z]\d\d[A-z][A-z]\d\d.*$'
cond1 = ~df.sensor_tagname.dropna().str.match(regex, na= False)

# Condition 2 - Same כלי with multiple same name sensors
cond2 = df.duplicated(['op_area','sensor_kind','device_number'], keep = False)

# Condition 3 - Suffixes that show only once
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
writer = pd.ExcelWriter(out_path, engine = 'xlsxwriter')
original.to_excel(writer, sheet_name = 'sheet1', index_label= 'id')
df.sort_index().to_excel(writer, sheet_name = 'sheet2', index_label= 'id')
writer.save()
writer.close()