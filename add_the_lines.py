import pandas as pd
import numpy as np

# We do not know if the 'start' and 'finish' time include the time that the batch have gone in the pipe

base = r'data/'
# ------------------------------------ read and format file 1 ------------------------------------  #
filename = r'sensor_joined.xlsx'
fullpath = base + filename

dtypes = {'sensor_id': np.int32,
          'lVarId': np.int32,
          'HMI': np.int32,
          'op_area_name': str,
          'op_area_number': np.int32,
          'device_kind': str,
          'device_number': np.int32,
          'sensor_tagname': str,
          'sensor_name': str,
          'sensor_name_edited': str,
          'desc': str,
          'out_pipes': str,
          'in_pipes': str}

a = pd.read_excel(io=fullpath,
                  dtypes=dtypes) \
    .rename({'id': 'sensor_id'}, axis=1)

a['device_number'] = pd.to_numeric(a['device_number'], errors='coerce')


# ------------------------------------ read and format file 2 ------------------------------------  #
# Read data
filename = r'tables_cottage_stages.csv'
fullpath = base + filename

dtypes = {'batchid': int,
          'stageid': int,
          'stage': str}

date_cols = ['start', 'finish']

b = pd.read_csv(filepath_or_buffer=fullpath,
                parse_dates=date_cols) \
    .rename({'stageid': 'device_number',
             'stage': 'device_kind',
             'id': 'read_id',
             'batchid': 'batch_id'}, axis=1)

#  Convert device_number non numeric to Null
#  Lower strings
b.assign(device_number = pd.to_numeric(b['device_number'], errors='coerce'),
         devic2_number = b['device_kind'].str.lower()
         )


# Remove 'packing' category
# Set some dates to Null
cond1 = (b['device_kind'] != 'packing')
b = b[cond1]

cond2 = (b['start'].dt.year != b['finish'].dt.year) \
        | (b['start'].dt.year == '2001') \
        | (b['finish'] == pd.Timestamp('2019-02-12 12:46:00')) \
        | (b['finish'] < b['start']) \
        | (b['finish'] - b['start'] > pd.Timedelta('0 days 03:00:00'))
b[cond2]['finish', 'start'] = None


# Groupby inorder remove batches that have multiple device kinds
b = b.groupby(['batch_id', 'device_kind']).agg({'device_number': 'max',
                                                'start': 'max',
                                                'finish': 'max'}) \
                                          .reset_index()

# Reorder device kinds
device_order = ['tk', 'mp', 'cv', 'wd', 'wc', 'cd', 'cr']

b['device_kind'] = b['device_kind'].astype('category')
b['device_kind'] = b['device_kind'].cat.set_categories(device_order).cat.reorder_categories(device_order, ordered=True)

b = b.sort_values(['batch_id', 'device_kind'], ascending=[True, True]).reset_index()

# Shift times up or down in order to find time of batch in pipes
in_start = b.groupby(['batch_id'])['finish'].shift(1).rename('start')
in_finish = b['start'].rename('finish')
time_for_inpipes = pd.concat([in_start, in_finish], axis=1)

out_start = b['finish'].rename('start')
out_finish = b.groupby(['batch_id'])['start'].shift(-1).rename('finish')
time_for_outpipes = pd.concat([out_start, out_finish], axis=1)



# ------------------------------------ merge files ------------------------------------  #
merged = a.merge(b, left_on=['device_kind', 'device_number'], right_on=['device_kind', 'device_number'])

merged = merged.sort_values(['batch_id', 'device_kind'], ascending=[True, True]).reset_index()

# test = pd.DataFrame([[1,2],
#                      [3,4],
#                      [5,6],
#                      [7,8]], columns = ['start','finish'])
#
# pd.concat([test.finish.shift(1),test.start], axis = 1)
