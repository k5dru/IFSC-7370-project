drop table asos_stations;

create table asos_stations ( 
NCDCID integer,
WBAN integer, 
COOPID integer, 
CALL varchar(4), 
NAME varchar(40), 
ALT_NAME varchar(40), 
COUNTRY varchar(40), 
ST varchar(3), 
COUNTY varchar(40), 
LAT numeric(9,5), 
LON numeric(9,5), 
ELEV integer, 
UTC integer, 
STNTYPE varchar(40), 
BEGDT integer, 
GHCND varchar(20), 
constraint pk_asos_stations primary key (NCDCID)
);

\copy asos_stations from program './asos_stations.sh | tail -n +3' with CSV DELIMITER '|'

/* 

NCDCID   WBAN  COOPID CALL NAME                           ALT_NAME                       COUNTRY              ST COUNTY                         LAT       LON        ELEV   UTC   STNTYPE                                            BEGDT    GHCND       
-------- ----- ------ ---- ------------------------------ ------------------------------ -------------------- -- ------------------------------ --------- ---------- ------ ----- -------------------------------------------------- -------- ----------- 
20028647 15908        YRL  RED LAKE                       RED LAKE                       CANADA               ON                                51.06667  -93.8      1230   -6    ASOS                                               20020819             
20030346 41415 914226 GUM  GUAM INTL AP                   GUAM NWSO TIYAN                GUAM                 GU GUAM                           13.48333  144.8      254    10    ASOS,COOP,PLCD,WXSVC                               20000111 GQW00041415 
20030369 41418 914855 GSN  SAIPAN INTL AP                 SAIPAN INTL AP                 NORTHERN MARIANA ISL MP SAIPAN                         15.11667  145.71667  215    10    ASOS,COOP                                          20000111 CQC00914855 
20023988 11641 668812 SJU  SAN JUAN L M MARIN AP          SAN JUAN INTL AP               PUERTO RICO          PR                                18.4325   -66.01083  9      -4    ASOS,COOP,PLCD                                     19960501 RQW00011641 
20022052 26409        MRI  ANCHORAGE MERRILL FLD          ANCHORAGE MERRILL FLD          UNITED STATES        AK ANCHORAGE BOROUGH              61.21694  -149.855   138    -9    AIRWAYS,ASOS                                       19971015 USW00026409 
20022040 26451 500280 ANC  ANCHORAGE TED STEVENS INTL AP  ANCHORAGE TED STEVENS INTL AP  UNITED STATES        AK ANCHORAGE BOROUGH              61.169    -150.0278  120    -9    AIRWAYS,ASOS,COOP,PLCD                             19980601 USW00026451 
20021784 25308 500352 ANN  ANNETTE WSO AP                 ANNETTE WSO AP                 UNITED STATES        AK PRINCE OF WALES-OUTER KETCHIKA 55.0389   -131.5787  109    -9    AIRWAYS,ASOS,COOP                                  19960901 USW00025308 
20022476 27502 500546 BRW  BARROW WSO AP                  BARROW WSO AP                  UNITED STATES        AK NORTH SLOPE BOROUGH            71.2834   -156.7815  31     -9    ASOS,COOP,PLCD                                     19980601 USW00027502 

*/ 
