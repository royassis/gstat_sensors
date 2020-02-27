import pandas as pd
import numpy as np
from functions import lower_all_strings

base = r'data/'

# ------------------------------------ read file 1 ------------------------------------  #
filename = r'sensor_joined.xlsx'
fullpath = base+filename

dtypes = {'sensor_id' : np.int32,
 'lVarId' : np.int32,
 'HMI' : np.int32,
 'op_area_name' : str,
 'op_area_number' : np.int32,
 'device_kind' : str,
 'device_number' : np.int32,
 'sensor_tagname' : str,
 'sensor_name' : str,
 'sensor_name_edited' : str,
 'desc' : str,
 'out_pipes' : str,
 'in_pipes' : str}

a = pd.read_excel(io = fullpath,
                  dtypes = dtypes)\
    .rename({'id':'sensor_id'},axis = 1)

a['device_number'] = pd.to_numeric(a['device_number'], errors = 'coerce')

a = a.dropna(axis = 0 , subset = ['device_number']).astype({'device_number':np.int32})

# ------------------------------------ read file 2 ------------------------------------  #
filename = r'tables_cottage_stages.csv'
fullpath = base+filename

dtypes = {'batchid' : int,
         'stageid' : int,
         'stage' : str}
date_cols = ['start', 'finish']

b = pd.read_csv(filepath_or_buffer = fullpath,
                parse_dates = date_cols)\
    .rename({'stageid':'device_number',
             'stage': 'device_kind',
             'id':'read_id',
             'batchid':'batch_id'} ,axis = 1)

b['device_number'] = pd.to_numeric(b['device_number'], errors = 'coerce')

b = b.dropna(axis = 0 , subset = ['device_number']).astype({'device_number':np.int32})

b['device_kind'] = b['device_kind'].str.lower()

# ------------------------------------ merge files ------------------------------------  #
a.merge(b, left_on =['device_kind','device_number'],right_on =['device_kind','device_number'])


