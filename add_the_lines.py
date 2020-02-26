import os
import re
import pandas as pd
import numpy as np

base = r'data/'

filename = r'sensor_joined.csv'
fullpath = base+filename
a = pd.read_csv(fullpath).rename({'id':'sensor_id'},axis = 1)

filename = r'tables_cottage_stages.csv'
fullpath = base+filename
b = pd.read_csv(fullpath).rename({'id':'read_id','batchid':'batch_id'},axis = 1)
