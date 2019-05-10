import sys
import re
import datetime as dt 
import pytz
import csv
from collections import OrderedDict

# regexp pattern for odict['temperature'] and humidity in the line.  could look like " 999/999" or " 27/M01" where "M" means minus.
td_pattern=re.compile('[M ][0-9][0-9]/M*[0-9][0-9] ')
# the pressure string appear like A2986 1900 25 4300.  I don't know how to decode it just yet, but lets try to match it:
#   in Little Rock it appear like A3023 -20 45 -1500.  
pressure_pattern=re.compile(' A[0-9]+ [0-9-]+ [0-9]+ [0-9-]+')

processed_count = 0
bad_data_count = 0
odict = OrderedDict([
  ('time_utc', ""),
  ('station_call', ""),
  ('wind_speed_kt', None ), 
  ('gust_kt', None ), 
  ('wind_direction', None ) ,
  ('wind_direction1', None ), 
  ('wind_direction2', None ), 
  ('temperature', None ), 
  ('dew_point', None ), 
  ('rel_humidity', None ), 
  ('pressure_mb', None ) 
])

w = csv.writer(sys.stdout)

for line in sys.stdin: 
  

  odict['wind_direction'] = None;
  odict['wind_speed_kt'] = None;
  odict['gust_kt'] = None;
  odict['wind_direction1'] = None;
  odict['wind_direction2'] = None;
  odict['temperature'] = None;
  odict['dew_point'] = None;
  odict['pressure_mb'] = None;
  odict['rel_humidity'] = None;

  processed_count = processed_count + 1
  p=0
  wban_number = line[p:p + 5]
  p = p + 5
  icao_call_sign = line[p:p + 4]
  p = p + 4
  station_call_sign = line[p:p + 4]
  p = p + 4
  year = line[p:p + 4]
  p = p + 4
  month = line[p:p + 2]
  p = p + 2
  day = line[p:p + 2]
  p = p + 2
  hour = line[p:p + 2]
  p = p + 2
  minute  = line[p:p + 2]
  p = p + 2
  record_length = line[p:p + 3]
  p = p + 3
  # from here, the fields appear to be space delimited and dependent on content. try to suss them out.
  fl=8
  date = line[p:p + fl]
  p = p + fl
  p = p + 1 # space
  fl=8
  time = line[p:p + fl]
  p = p + fl
  p = p + 1 # space
  fl=6
  data_type = line[p:p + fl]
  p = p + fl
  p = p + 1 # space
  fl=4
  station_call_sign2 = line[p:p + fl]
  p = p + fl
  p = p + 1 # space
  fl=7
  ddhhmmz = line[p:p + fl]
  p = p + fl
  #the day and time of the observation (utc).  the format is (ddhhmmz).

  # here is where it starts getting strange. 
  if line[p:p+3] == ' AU' or line[p:p+3] == ' AQ':  # there are some AQTO in the data.
    p = p + 1 # space
    fl=4
    observation_type = line[p:p + fl]
    p = p + fl
  else:
    observation_type = ""
  p = p + 1 # space

  # get everything from here to kt in a wind characteristicts field for further parsing
  q = line.find("KT", p, len(line))
  if q >= 0:
    wind_stuff=line[p:q+2]
    p = q + 2
  else:
    wind_stuff=""

  if len(wind_stuff) > 3:
    wind_direction = wind_stuff[0:3]
    wind_stuff=wind_stuff[3:]
  else:
    wind_direction=""

  if len(wind_stuff) > 3 and wind_stuff[2] == 'G':
    gust=wind_stuff[2:5]
    wind_stuff=wind_stuff[0:2] + wind_stuff[5:]
  else:
    gust=""

  if len(line) > p+4 and line[p+4] == 'V': 
    # looks like wind variability.  
    p = p + 1 # space
    fl=7
    wvar = line[p:p + fl]
    p = p + fl
  else: 
    wvar = ""
  #
  # get everything from here to m in a visibility characteristicts field for further parsing
  p = p + 1 # space
  q = line.find("M", p, len(line))
  if q >= 0:
    visibility_stuff=line[p:q+1]
    p = q + 1
  else:
    visibility_stuff=""

  # if wind_stuff is not 4 at this point, this is likely a line i can't use anyway.  toss it. 
  if len(wind_stuff) != 4 or wind_stuff[2:] != "KT":
    wind_speed_kt = ""
  else: 
    wind_speed_kt = wind_stuff[:2]

  # ok what is left: 

  td_match=td_pattern.search(line[p:])
  try:
    odict['temperature']=td_match.group(0)
    if odict['temperature'][3] == '/': 
      dew_point=odict['temperature'][4:]
      odict['temperature']=odict['temperature'][1:3]
    if odict['temperature'][0] == 'M':
      odict['temperature']="-" + odict['temperature'][1:]
    if dew_point[0] == "M":
      dew_point = "-" + dew_point[1:]
    odict['temperature'] = int(odict['temperature'])
    odict['dew_point'] = int(dew_point)
  except:
    pass 

  pressure_match=pressure_pattern.search(line[p:])
  try:
    pressure=pressure_match.group(0)
    if pressure[1] == "A":
      pressure = pressure[2:]
      ps = pressure.split(' ')
      odict['pressure_mb'] = round(float(ps[0]) / 100.0 * 33.8639, 1)  # inches hg to millibars
      odict['rel_humidity'] = float(ps[2]) / 100.0 # i think
  except:
    pass

  try: # to clean the data a bit
  # fix up an observation timestamp
  # date is local time in mm/dd/yy format (did these guys not Y2K?)
  # ['KLIT', '02/28/14', '22:00:31', '010400Z', '070', '04', '', '', '07', '04 ', '3000', '79']
    localyear=int('20' + date[6:])
    localmon=int(date[:2])
    localday=int(date[3:5])
    localhour=int(time[0:2])
    localminute=int(time[3:5])
    localsecond=int(time[6:8])
    gmtyear = localyear
    gmtmon = localmon
    gmtday=int(ddhhmmz[0:2])
    gmthour=int(ddhhmmz[2:4])
    gmtminute=int(ddhhmmz[4:6])
   
    if gmtday < localday: # in the west, rolled over on the end of the month 
      gmtmon=localmon + 1
      if (gmtmon > 12):   # in the west, rolled over at the end of the year
        gmtmon = 1
        gmtyear = localyear + 1
  
    odict['time_utc'] = str(dt.datetime(gmtyear, gmtmon, gmtday, gmthour, gmtminute, 0, 0, pytz.UTC))  
    odict['station_call'] = station_call_sign2
    
    try:
      odict['wind_direction'] = int(wind_direction)
    except: 
      pass

    try:
      odict['wind_speed_kt'] = int(wind_speed_kt)
    except: 
      pass

    try:
      odict['gust_kt'] = int(gust[1:])
    except: 
      pass

    try:
      odict['wind_direction1'] = int(wvar[0:3])
      odict['wind_direction2'] = int(wvar[4:7])
    except: 
      pass 
      

   # ['2014-02-01 20:25:00+00:00', 'KLIT', '210', '11', '', '180V240', '17', '12 ', '2985', '69']
   # ['2014-02-03 21:20:00+00:00', 'KLIT', 'VRB', '06', '', '', '03', '-04 ', '3027', '59']
  #  ['2014-02-04 16:10:00+00:00', 'KLIT', '090', '09', 'G17', '', '01', '-02 ', '3005', '92']


  except:
    bad_data_count = bad_data_count + 1
    print(str(processed_count) + " rows processed; " + str(bad_data_count) + " discarded due to bad data" , file=sys.stderr)
    if bad_data_count > (processed_count / 1000.0):
      print("bad data exceed 0.1% of observations. blowing chow.")
      sys.exit(1)
    continue

  #print ([wban_number,icao_call_sign,station_call_sign,year,month,day,hour,minute,record_length])
  # print ([date,time,data_type,ddhhmmz,observation_type]);
#   print ([station_call_sign2,wind_direction,wind_direction,wind_stuff,gust,wvar,visibility_stuff])
#   print ([wind_speed_kt,gust,wvar])
  if processed_count == 1 and '-h' in sys.argv:
    w.writerow(odict.keys())
  w.writerow(odict.values())


