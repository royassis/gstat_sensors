#### Data
1. sensors_in.xlsx -<br> 
File that contains semi-row data about sensor names

2. sensors_out.xlsx -<br> 
File that contains cleaned data from <b><u>`sensors_in.xlsx`</u></b>

3. sensors_desc.xlsx -<br> 
File that contains description of the sensors - was created manually

4. tables_cottage_stages.csv -<br> 
File that contains batch data

#### Code

1. main.py -<br>
Creates <b><u>`sensors_out.xlsx`</u></b>

2. join_files.py -<br> 
Reads <b><u>`sensors_out.xlsx`</u></b> 
and <b><u>`sensors_desc.xlsx`</u></b>, joins them
and creates <b><u>`sensors_out.xlsx`</u></b>

5. add_the_lines_new.py -<br> 
Reads <b><u>`sensors_joined.xlsx`</u></b> and
Reads <b><u>`tables_cottage_stages.csv`</u></b> 

4. add_the_lines.py -<br> 
Old file - replaced with <b><u>`add_the_lines_new.py`</u></b>



