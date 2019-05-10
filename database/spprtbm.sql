
drop table spprtbm_stg; 

create table spprtbm_stg ( 
RTBMInterval timestamp,
GMTIntervalEnd timestamp,
Settlement_Location varchar(40),
Pnode varchar(40),
LMP numeric(9,4),
MLC numeric(9,4), 
MCC numeric(9,4),
MEC numeric(9,4) 
); 


/* 
08/21/2014 20:10:00,08/22/2014 01:10:00,AEC,SOUC,41.7960,-1.3639,0.0279,43.1320
*/ 

\copy spprtbm_stg from program 'find spp_data/ -type f -exec gzip -dc {} \; | grep -e SPP....._HUB -e WIND' with CSV

