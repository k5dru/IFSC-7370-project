/*

SQL script to write a SQL script to widen/flatten the normalized weather data into columns for ML. 
Manually edit the output of this one into a SQL command that will pull the data into wide format.

 wind_speed_kt   | numeric(9,4)             |           |          | 
 gust_kt         | numeric(9,4)             |           |          | 
 wind_direction  | smallint                 |           |          | 
 wind_direction1 | smallint                 |           |          | 
 wind_direction2 | smallint                 |           |          | 
 temperature     | numeric(9,4)             |           |          | 


*/

select 'max(case when station_call = ''' || station_call || ''' then wind_speed_kt end) as ' || station_call || '_kt'  as a
, 'max(case when station_call = ''' || station_call || ''' then wind_direction end) as ' || station_call || '_dir'  as b
, 'max(case when station_call = ''' || station_call || ''' then temperature end) as ' || station_call || '_temp'  as c
from (select distinct station_call from weather_clean) calls

;
