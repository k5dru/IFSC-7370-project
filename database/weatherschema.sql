-- drop table weather_5min; 

create table weather_5min ( 
  time_utc timestamptz not null,
  station_call varchar(4) not null,
  wind_speed_kt numeric(9,4),
  gust_kt numeric(9,4),
  wind_direction smallint,
  wind_direction1 smallint,
  wind_direction2 smallint, 
  temperature numeric(9,4), 
  dew_point numeric(9,4), 
  rel_humidity numeric(9,4), 
  pressure_mb numeric(9,4) 
-- , constraint pk_weather_5min primary key (time_utc, station_call) 
);

VACUUM (VERBOSE, ANALYZE); 

-- \copy weather_5min from program './pythonwind.sh' with (format CSV)

/*

2014-04-01 06:00:00+00:00,KLIT,3,,140,,,12,8,0.77,1015.6
2014-04-01 06:05:00+00:00,KLIT,0,,0,,,12,8,0.8,1015.6
2014-04-01 06:10:00+00:00,KLIT,0,,0,,,12,8,0.77,1015.6
2014-04-01 06:15:00+00:00,KLIT,0,,0,,,11,8,0.83,1015.6
2014-04-01 06:20:00+00:00,KLIT,0,,0,,,10,7,0.83,1015.9
2014-04-01 06:25:00+00:00,KLIT,0,,0,,,10,8,0.86,1015.9
2014-04-01 06:30:00+00:00,KLIT,0,,0,,,12,8,0.77,1015.9
2014-04-01 06:35:00+00:00,KLIT,0,,0,,,11,7,0.8,1015.9
2014-04-01 06:40:00+00:00,KLIT,0,,0,,,10,7,0.83,1015.9
 */ 

create table weather_clean ( 
  time_utc timestamptz not null,
  station_call varchar(4) not null,
  wind_speed_kt numeric(9,4),
  gust_kt numeric(9,4),
  wind_direction smallint,
  wind_direction1 smallint,
  wind_direction2 smallint, 
  temperature numeric(9,4), 
  dew_point numeric(9,4), 
  rel_humidity numeric(9,4), 
  pressure_mb numeric(9,4) 
 , constraint pk_weather_5min primary key (time_utc, station_call) 
);

