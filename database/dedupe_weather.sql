
insert into weather_clean

with station_dupes as ( 
  select time_utc, station_call from weather_5min group by 1,2 having count(*) > 1 
)

select k.time_utc, k.station_call, k. wind_speed_kt, k.gust_kt, k.wind_direction, k.wind_direction1, k.wind_direction2, k.temperature, k.dew_point, k.rel_humidity, k.pressure_mb
from (
  select w.time_utc, w.station_call, w. wind_speed_kt, w.gust_kt, w.wind_direction, w.wind_direction1, w.wind_direction2, w.temperature, w.dew_point, w.rel_humidity, w.pressure_mb
  , row_number() over (partition by w.time_utc, w.station_call order by w.wind_speed_kt, w.wind_direction, w.temperature, w.dew_point, w.rel_humidity, w.pressure_mb) as keep_this_one 
  from weather_5min w
  join station_dupes d 
  on (w.time_utc = d.time_utc and w.station_call = d.station_call)
) k
where keep_this_one = 1
union all 
select w.time_utc, w.station_call, w. wind_speed_kt, w.gust_kt, w.wind_direction, w.wind_direction1, w.wind_direction2, w.temperature, w.dew_point, w.rel_humidity, w.pressure_mb
from weather_5min w
left join station_dupes d 
on (w.time_utc = d.time_utc and w.station_call = d.station_call)
where d.time_utc IS NULL
;

vacuum analyze; 

