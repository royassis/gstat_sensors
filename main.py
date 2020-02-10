import pandas as pd

#################
# Import data
#################
path = r"C:\Users\roy\Desktop\sensors.xlsx"
out_path = r"C:\Users\roy\Desktop\sensorsOUT.xlsx"

df = pd.read_excel(path, sheet_name='working copy', index_col='id')

#################
# Conditions
#################

# Condition 1 - Sensor tagname must adhere to the following regex
cond1 = ~df.sensor_tagname.dropna().str.match(r'^[A-z][A-z]\d\d[A-z][A-z]\d\d.*$', na= False)

# Condition 2 - Same כלי with multiple same name sensors
cond2 = df.duplicated(['sensor_kind','מספר כלי'])

# Condition 3 - Suffix that show only once in אזור
some_other_stuff = df.groupby(['sensor_suffix','אזור'])['sensor_suffix'].count()
lonly_index = some_other_stuff[some_other_stuff == 1].index
a,b = lonly_index.get_level_values(0), lonly_index.get_level_values(1)
cond3 = ((df['sensor_suffix'] == 'a') & (df['אזור'] == 'b'))

pvt = df.pivot_table(values ='sensor_tagname' , index = ['סוג כלי'], columns ='sensor_suffix' , aggfunc = 'count', fill_value= 0)
unstacked = pvt.unstack().reset_index().rename({0:"count_all"},axis = 1)
only_one = unstacked[unstacked.count_all == 1]

## Self-Join suffixe/אזור/מספר כלי on  אזור,suffix
## suffixe == suffixe and אזור == אזור and מספר כלי != מספר כלי

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
