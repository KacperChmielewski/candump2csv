# candump to csv

## Usage

### Collect data
Candump some data using:
```
candump any -l
```
you should see info like this:
```
Disabled standard output while logging.
Enabling Logfile 'candump-2024-10-04_145121.log'
```
if you finish, hit `Ctrl+C` to end recording. Now you have your candump log file.

### Process candump log file
To process the candump log file, use the script:
```
Usage: candump2csv.py <dbc_file> <candump_log_file>
```
Example:
```
python candump2csv.py myCar.dbc candump-2024-10-04_145121.log
```
In the `output` directory, you should have as many `.csv` files, as types of your frames declared in .dbc file. The first line will have field names, and then you can expect the data.

Example output:
```
Timestamp,gyro_x,gyro_y,gyro_z
1711651681.981097,0.0,-0.0625,0.0625
1711651681.985763,0.0625,0.0625,0.0625
1711651681.992694,0.0625,0.0625,0.0625
1711651681.998815,-0.0625,-0.125,0.0
1711651682.003955,0.125,-0.0625,0.0625
1711651682.011135,0.125,-0.0625,0.0625
1711651682.015802,0.125,0.0,0.0
1711651682.022772,0.125,0.0,0.0
```
NOTE! Every time you run the script, the output files are overwritten!
