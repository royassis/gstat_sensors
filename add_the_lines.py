import pandas as pd
from functions import lower_all_strings

base = r'data/'

filename = r'sensor_joined.csv'
fullpath = base+filename
a = pd.read_csv(fullpath)\
    .rename({'id':'sensor_id'},axis = 1)

filename = r'tables_cottage_stages.csv'
fullpath = base+filename
b = pd.read_csv(fullpath)\
    .rename({'id':'read_id','batchid':'batch_id'},axis = 1)\
    .dropna(axis =0, how = 'any', subset = ['device_number'])\
    .astype({'device_number':int})
b['device_kind'] = b['device_kind'].str.lower()

a.merge(b, left_on =['device_kind','device_number'],right_on =['device_kind','device_number'])