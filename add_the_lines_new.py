# Imports and options
import pandas as pd
import numpy as np
import os

pd.options.display.width = 0

# Set base dirs
mapper_base = r'resources'
base = r'data'

# ------------------------------------ read time_mapper ------------------------------------  #
filename = r'time_mapper.csv'
fullpath = os.path.join(mapper_base, filename)
time_mapper = pd.read_csv(fullpath)

# ------------------------------------ read line_mapper ------------------------------------  #
filename = r'line_mapper.csv'
fullpath = os.path.join(mapper_base, filename)
line_mapper = pd.read_csv(fullpath)
line_mapper = line_mapper.assign(device_number=line_mapper['device_number'].str.split(','))

# ------------------------------------ read and format file 1 ------------------------------------  #
# Read data
filename = r'sensor_joined.xlsx'
fullpath = os.path.join(base, filename)

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

# Coerce non numerics from columns
a['device_number'] = pd.to_numeric(a['device_number'], errors='coerce')

# Concat xx(device_kind) to op_area_name and number
cond = a['device_kind'] == 'xx'
a.loc[cond, 'device_kind'] = a['op_area_name'][cond] + a['op_area_number'][cond].astype(str) + 'xx'

# ------------------------------------ read and format file 2 ------------------------------------  #
# Read data
filename = r'tables_cottage_stages.csv'
fullpath = os.path.join(base, filename)

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
b = b.assign(device_number=pd.to_numeric(b['device_number'], errors='coerce'),
             device_kind=b['device_kind'].str.lower(),
             delta=((b['finish'] - b['start']) / np.timedelta64(1, 'h'))
             )

b = b.assign(delta_q_bins=b.groupby(['device_kind'])['delta'].transform(
    lambda x: pd.qcut(x, q=10, precision=7, labels=False, duplicates='drop'))
)

# Remove 'packing' category
# Set some dates to Null
cond1 = (b['device_kind'] != 'packing')
b.loc[:, :] = b[cond1]

cond2 = (b['start'].dt.year != 2019) \
        | (b['finish'].dt.year != 2019) \
        | (b['finish'] == pd.Timestamp('2019-02-12 12:46:00')) \
        | (b['finish'] == pd.Timestamp('2019-02-12 12:47:00')) \
        | (b['delta'] < 0) \
        | (b['delta'] > 15)

b.loc[cond2, ['finish', 'start']] = None

# Groupby in order to remove batches that have multiple device kinds
b = b.groupby(['batch_id', 'device_kind']).agg({'device_number': 'max',
                                                'start': 'max',
                                                'finish': 'max'}) \
    .reset_index()

# --------------------------------------------------------  #
# Pivot table by batch number, each line would thus contain one batch, and each column a diff device_kind + start
# and finish columns
# --------------------------------------------------------  #
xxx = b.pivot_table(index='batch_id',
                    columns='device_kind',
                    values=['start', 'finish', 'device_number'],
                    aggfunc='first')

# Flatten column multiindex
xxx.columns = ['_'.join(col).strip() for col in xxx.columns]

# Do the same for the pipes
# make an empty pipes df and concat with previous df
pipes = ['cc1xx', 'ps1xx']
pipes = ['start_' + i for i in pipes] + ['finish_' + i for i in pipes] + ['device_number_' + i for i in pipes]

pipes = pd.DataFrame(columns=pipes,
                     data=np.empty((xxx.shape[0], pipes.__len__())),
                     index=xxx.index)
pipes[:] = np.nan

xxx = pd.concat([xxx, pipes], axis=1).reset_index()

# Set the start and finish times for each pipe by the logic in the 'time_mapper' file
for _, r in time_mapper.iterrows():
    xxx[r['to']] = xxx[r['from']]

# Set line numbers for each pipe by the logic in the 'line_mapper' file
for _, r in line_mapper.iterrows():
    line_list = r['device_number']

    device_columns = r['col_a']
    line_column = r['col_b']

    cond = xxx[r['col_a']].isin(line_list)
    xxx.loc[cond, line_column] = r['line_number']

# Convert back to the long form
stubnames = ["device_number", "start", "finish"]
xxx = pd.wide_to_long(df=xxx, stubnames=stubnames, i="batch_id", j="device_kind", sep='_', suffix='.*').reset_index()

# ------------------------------------ merge files ------------------------------------  #
merged = a.merge(xxx, left_on=['device_kind', 'device_number'], right_on=['device_kind', 'device_number'])
merged = merged.sort_values(['batch_id', 'device_kind'], ascending=[True, True]).reset_index()
merged = merged.drop(['sensor_id','out_pipes','in_pipes','index'], axis = 1)

# ----------------------------------- find sensors that did not match with batch -----------------------------------  #
m2 = a.merge(xxx, how='left', left_on=['device_kind', 'device_number'], right_on=['device_kind', 'device_number'])
cond = m2['batch_id'].isna()

# m2[cond].to_clipboard()
