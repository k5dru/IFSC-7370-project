#
## Each variable-length logical record contains one station's 5-minute data values for all reported meteorological elements.  The record consists of a control word, an identification portion and a data portion.  The control word is used by the computer operating system for record length determination.  The identification portion, added at archive time, includes the station number, Icao call sign, station call sign, and observation date and time (LST).  The data portion contains the complete unedited record as received from the observation site. Each element is classified as numeric [N] or alphanumeric [A] as indicated after each element name.  Values recorded in numeric elements are right justified with unused positions zero-filled; signed numbers always begin with a "+" or a "-" in the left-most position.  Recorded values in alphanumeric elements are left-justified and unused positions are filled with blanks.
#
##Missing and unknown values of numeric elements are generally indicated by all nines; sometimes recorded as a signed number.  In instances when all nines in a numeric element could represent a value within the range of values for the element, another numeric constant (outside the range of values) will be used to indicate missing/unknown.  Missing and unknown values of alpha-
##numeric elements are recorded as all blanks.

import sys

for line in sys.stdin: 
  p=0

##WBAN NUMBER [N]
##The WBAN (Weather Bureau, Army, Navy) number is a unique five-digit number assigned by the NCDC.  
  WBAN_NUMBER = line[p:p + 5]
  p = p + 5
#ICAO CALL SIGN [A]
#The ICAO Call Sign is a location identifier, four characters in length, and may consist of letters and numbers.  Authority for assignment of numbers is coordinated with the FAA, Dept. of the Navy, Transport Canada, FCC and NWS.  Call signs are left-justified in the field.
  ICAO_CALL_SIGN = line[p:p + 4]
  p = p + 4
#
  STATION_CALL_SIGN = line[p:p + 4]
  p = p + 4
#The Call sign is a location identifier, three or four characters
#in length, and may consist of letters and numbers.  Authority for assignment of numbers is coordinated with the FAA, Dept. of the Navy, Transport Canada, FCC and NWS.  Call signs are left-justified in the field.
#

  YEAR = line[p:p + 4]
  p = p + 4
#The four-digit year of the observation with reference to Local Standard Time (LST).
#
  MONTH = line[p:p + 2]
  p = p + 2
#The month of the observation (LST).  The values range from 01 - 12.
#
  DAY = line[p:p + 2]
  p = p + 2
#The day of the observation (LST).  The values range from 01 - 31.
#
  HOUR = line[p:p + 2]
  p = p + 2
#The hour of the observation (LST).  The hour is recorded on the 24-hour clock system (e.g. 3 am is 03, 3 pm is 15, midnight is 00).  The hours are whole numbers and range from 00 to 23.
#
  MINUTE  = line[p:p + 2]
  p = p + 2
#The minute of the observation.  Observations are recorded on whole five-minute increments.  The values may be 00, 05, 10,...,50 55.
#
  RECORD_LENGTH = line[p:p + 3]
  p = p + 3
#The length of the record, with no spaces, starting at the end of this element.
#

  # from here, the fields appear to be space delimited and dependent on content. Try to suss them out.
  fl=8
  DATE = line[p:p + fl]
  p = p + fl
  #The date of the observation (LST).  The format is MM/DD/YY.
  #
  p = p + 1 # space
  fl=8
  TIME = line[p:p + fl]
  p = p + fl
  #The time of the observation (LST). the format is HH:MM:SS.
  #
  p = p + 1 # space
  fl=6
  DATA_TYPE = line[p:p + fl]
  p = p + fl
  #Always = "5-MIN".
  #
  p = p + 1 # space
  fl=4
  STATION_CALL_SIGN2 = line[p:p + fl]
  p = p + fl
  #The Call sign is a location identifier, four characters in length, and may consist of letters and numbers.  Authority for assignment of numbers is coordinated with the FAA, Dept. of the Navy, Transport Canada, FCC and NWS.  Call signs are left-justified in the field.
  #
  p = p + 1 # space
  fl=7
  DDHHMMZ = line[p:p + fl]
  p = p + fl
  #The day and time of the observation (UTC).  The format is (ddhhmmZ).

  # here is where it starts getting strange. 
  if line[p:p+3] == ' AU':
    p = p + 1 # space
    fl=4
    OBSERVATION_TYPE = line[p:p + fl]
    p = p + fl
  else:
    OBSERVATION_TYPE = ""
  p = p + 1 # space

  # get everything from here to KT in a wind characteristicts field for further parsing
  q = line.find("KT", p, len(line))
  if q >= 0:
    WIND_STUFF=line[p:q+2]
    p = q + 2
  else:
    WIND_STUFF=""

  if len(WIND_STUFF) > 3:
    WIND_DIRECTION = WIND_STUFF[0:3]
    WIND_STUFF=WIND_STUFF[3:]
  else:
    WIND_DIRECTION=""

  if len(WIND_STUFF) > 3 and WIND_STUFF[2] == 'G':
    GUST=WIND_STUFF[2:5]
    WIND_STUFF=WIND_STUFF[0:2] + WIND_STUFF[5:]
  else:
    GUST=""

  if len(line) > p+4 and line[p+4] == 'V': 
    # looks like wind variability.  
    p = p + 1 # space
    fl=7
    WVAR = line[p:p + fl]
    p = p + fl
  else: 
    WVAR = ""
  #ESTIMATED WIND [A]
  #An "E" may appear in the field to indicate that the wind speed, direction or both were estimated by an observer and edited into the record.  Otherwise, the field is blank.
  # WIND_GUST = line[p:p + fl]
  # WIND_SPEED = line[p:p + fl]
  ##Wind speed is reported in whole knots.  A zero in the field indicates calm conditions. Sensor range:  0-125 knots.  Missing/unknown values are recorded as 999.

  #WIND CHARACTER [A]
  #= line[p:p + fl]
  #p = p + fl
  #The character of the wind is indicated with a "G" for gust or a "Q" for squall.  The field is blank if there was no occurrence.

  #
  #WIND CHAR SPEED [N]
  #= line[p:p + fl]
  #p = p + fl
  #The speed associated with the wind character.  Speeds are in knots.  Missing/unknown values are recorded as 999.
  #
  #VISIBILITY [N]
  #= line[p:p + fl]
  #p = p + fl
  #Visibility measured in miles.  Reportable values are <1/4, 1/4, 1/2, 3/4, 1, 11/4, 11/2, 13/4, 2, 21/2, 3, 31/2, 4, 5, 7 and 10 or 10+.  The symbols valid for this element are:  <, /, + and digits 0-9 inclusive.
  #
  # get everything from here to M in a visibility characteristicts field for further parsing
  p = p + 1 # space
  q = line.find("M", p, len(line))
  if q >= 0:
    VISIBILITY_STUFF=line[p:q+1]
    p = q + 1
  else:
    VISIBILITY_STUFF=""

  # if WIND_STUFF is not 4 at this point, this is likely a line I can't use anyway.  Toss it. 
  if len(WIND_STUFF) != 4 or WIND_STUFF[2:] != "KT":
    WIND_SPEED_KT = ""
  else: 
    WIND_SPEED_KT = WIND_STUFF[:2]
#    continue

  #print ([WBAN_NUMBER,ICAO_CALL_SIGN,STATION_CALL_SIGN,YEAR,MONTH,DAY,HOUR,MINUTE,RECORD_LENGTH])
  # print ([DATE,TIME,DATA_TYPE,DDHHMMZ,OBSERVATION_TYPE]);
#   print ([STATION_CALL_SIGN2,WIND_DIRECTION,WIND_DIRECTION,WIND_STUFF,GUST,WVAR,VISIBILITY_STUFF])
  print ([WIND_SPEED_KT,GUST,WVAR])
 #  print ([line[p:len(line)]])
  #
  #WEATHER AND OBSTRUCTIONS [A]
  #= line[p:p + fl]
  #p = p + fl
  #The Weather and Obstruction field is a twenty character field that specifies the weather and/or obstruction occurring at the time of the observation.  The ASOS system at this writing reports precipitation (P-, R-, R, R+, ZR-, ZR, S-, S, S+) and obstructions (H or F).  Only one obstruction is reported in a single observation.  Other weather types may be edited into the record by the observer.  For a complete list of weather and obstruction types, see the documentation for the hourly data (TD3280), Environmental Information Summary C-2 (EIS C-2), NWS Observing Handbook No. 7, or the Federal Meteorological Handbook No. 1 (FMH-1). 
  #
  #SKY CONDITION [A]
  #= line[p:p + fl]
  #p = p + fl
  #The Sky Condition field is a twenty-five character field that specifies the height and amount of up to three cloud layers as determined by the ASOS ceilometer.  The layers occur up to 12,000 ft.  A ceiling designation "M" is prefixed to the lowest broken or overcast layer, "W" for indefinite ceiling, "X" for obscuration, and "V" for variable ceiling.  The observer may edit an "E" into the record when the automated sensor is inoperative and the ceiling height is estimated.
#
#Heights are given in hundredths of feet above the ground, e.g. 15 is 1500 ft. If no layers are detected below 12,000 ft. the message, "CLR BLO 120" is entered.  The layer amounts are SCT, BKN and OVC.  Valid contractions for this element are:  CLR, BLO, SCT, BKN and OVC.
#
#TEMPERATURE [Signed N]
  #= line[p:p + fl]
  #p = p + fl
#Temperature is recorded in whole degrees Fahrenheit.  Sensor range:  -80 degrees Fahrenheit to +130 degrees Fahrenheit.  Missing/unknown values are recorded as 999.
#
#DEW POINT [Signed N]
  #= line[p:p + fl]
  #p = p + fl
#Dew-point temperature is recorded in whole degrees Fahrenheit.
#Sensor range:  -30 degrees Fahrenheit to +86 degrees Fahrenheit
#Missing/unknown values are recorded as 999.
#
#ALTIMETER SETTING [N]
  ##= line[p:p + fl]
  #p = p + fl
#The pressure value to which an aircraft altimeter scale is set so that it will indicate the altitude above mean sea level of the aircraft on the ground at the location where the pressure was determined.  (The altimeter scale has a range of 28.00 to 31.00 inches.  The altimeter setting is determined by subtracting the station elevation from the pressure altitude and converting the remainder to inches of mercury.  The altimeter setting will then fall within the range of the altimeter scale.)  The altimeter setting is recorded in hundredths of an inch of mercury using the units, tenths, and hundredths digits, e.g. 015 means an altimeter setting of 30.15 inches.  Missing/unknown values are recorded as 444.
#
#SEA-LEVEL PRESSURE [N]
  #= line[p:p + fl]
  #p = p + fl
#Sea-level pressure is given in tenths of hectopascals (millibars).  The last three digits are recorded, e.g. 125 means 1012.5 hPa, 890 means 989.0 Hpa.  Sensor range:  16.9" Hg - 31.5" Hg (572.3 hPa - 1066.7 hPa) missing/unknown values are recorded as 444.
#
#PRESSURE ALTITUDE [Signed N]
  #= line[p:p + fl]
  #p = p + fl
#The height of the standard atmosphere at which the station pressure would be observed.  Pressure altitude is recorded in whole feet.  Missing/unknown values are recorded as -9999.
#
#RELATIVE HUMIDITY [N]
  #= line[p:p + fl]
  #p = p + fl
#The ratio, expressed as a percentage, of the actual vapor pressure of the air to the saturation vapor pressure.  (The amount of water vapor in the air expressed as a percentage of the amount of water vapor the air could hold at that same temperature and pressure).  Range of values:  001-100 inclusive.  Missing/unknown values are recorded as 999.
#
#DENSITY ALTITUDE [N]
  #= line[p:p + fl]
  #p = p + fl
#The pressure altitude corrected for temperature variations from the standard atmosphere.  Density altitude is reported in whole feet.  Missing/unknown values are recorded as -9999.
#
#WIND DIRECTION - MAGNETIC [N]
  #= line[p:p + fl]
  #p = p + fl
#The direction of the wind related to magnetic north.  Wind direction is recorded in tens of degrees from magnetic north.  Values range from 000 to 360, where 000 indicates calm and 360 indicates magnetic north.  Missing/unknown values are recorded as 999.
#
#WIND SPEED - MAGNETIC [N]
  #= line[p:p + fl]
  #p = p + fl
#Wind speed is reported in whole knots.  All zeros in the field indicate calm conditions.  Wind speed - magnetic is the same as wind speed associated with true north.  Missing/unknown values are recorded as 999.
#
#REMARKS [A]
#  = line[p:p + fl]
#  p = p + fl
#Remarks provide additional information about the observation, conditions in the vicinity of the station and conditions during the past 3- to 24-hour period.  Observers may manually enter remarks in accordance with FMH-1 procedures in addition to the ASOS remarks listed here.  Whenever remarks are not included, one space is recorded in this REMARKS section.
#
#*CIG: Sky condition at secondary ceilometer site (e.g. Runway 11).   e.g. CIG 10 RY11.
#
#*VSBY: Visibility at secondary sensor site (e.g. Runway 11).  e.g. VSBY 2 RY11.
#
#5appp: Pressure tendency and change reported at 3-hourly UTC times (00, 03, 06, 09, 12, 15, 18, 21).   e.g. 58033.
#
#6RRR/: Precipitation amount of .01 inch or more for the past 6 hours at 00, 06, 12, 18 UTC and for the past 3 hours at 03, 09, 15, 21 UTC.  A trace amount is recorded as 6000/.  e.g. 6008/ indicates .08 inch fell during the period.
#
#7RRRR: 24-hour UTC precipitation amount reported at 12 UTC. e.g. 70024.
#
#*1sTTT: Maximum temperature in degrees Fahrenheit for the past 6 hours recorded at 6-hourly UTC times. "s" is the sign, 0 indicates positive and 1 indicates negative. e.g. 10067.
#
#*2sTTT: Minimum temperature in degrees Fahrenheit for the past 6 hours recorded at 6-hourly UTC times. "s" is the sign, 0 indicates positive and 1 indicates negative. e.g. 21007.
#
#*4sTTTsTTT: 24-hour calendar day max and min temperature in degrees Fahrenheit recorded at midnight local standard time.  e.g. 400720043.
#
#CIG minVmax: Variable ceiling in 100's of feet.  e.g. CIG 23V30.
#
#TWR VSBY: Visibility in statute miles reported by airport tower personnel.  e.g. TWR VSBY 2.
#
#SFC VSBY: Visibility in statute miles reported by ASOS visibility sensor.  e.g. SFC VSBY 1/2.
#
#VSBY minVmax: Variable visibility in statute miles.  e.g. VSBY 1 3/4V2 1/2.
#
#_Btt_Ett: Beginning and Ending of weather in minutes past the hour.  e.g. SB07SE38RB38.
#
#PCPN rrrr:  Hourly precipitation amount in .01 inches since the last hour.  Trace is PCPN 0000. Missing is M.  e.g. PCPN 0009.
#
#WSHFT hhmm:  Time (UTC) wind shift began.  e.g. WSHFT 1715.
#
#WND ddVdd: Variable wind direction in tens of degrees.  e.g. WND 23V30.
#
#PK WND ddff/hhmm: Peak wind in tens of degrees, whole knots and time (UTC). e.g. PK WND 2032/1725.
#
#PRESRR: Pressure rising rapidly.
#
#PRESFR: Pressure falling rapidly.
#
#PRJMP pp/hhmm/hhmm: Pressure jump in .01 inches of mercury with beginning and ending times. e.g. PRJMP 13/1250/1312.
#
#PWINO: Precipitation identifier sensor not operational.
#
#ZRNO: Freezing rain sensor not operational.
#
#TNO: Thunderstorm information not available.
#
#$: Maintenance check indicator.
#
#* An asterisk indicates that at this writing the remark is not in use.  1sTTT and 2sTTT are reported according to FMH-2, Surface Synoptic Codes, paragraph 6.3.3 (0000 UTC; past 18-hour minimum, past 12-hour maximum, 0600 UTC; past 24-hour minimum, past 24-hour maximum, 1200 UTC; past 12-hour minimum, previous calendar day maximum, 1800 UTC; past 24-hour minimum, past 12-hour maximum).  A future version of ASOS software will change the definition to the previous 6-hour maximum and minimum temperatures.
#
#3.   Start Date: Data, in earlier formats, begin in September 1992 for a limited number of stations and time periods.  By June 1994, approximately 34 stations, mainly in the central U.S., were commissioned  (i.e. transmitting official observations).  Data official archived in this format begin in July 1996
# 
#4.   Stop Date: Ongoing.
#
#5.   Coverage: North America, Alaska, Hawaii, Puerto Rico
#
#      a. Southernmost Latitude     18N
#      b. Northernmost Latitude     72N
#      c. Westernmost Longitude    171W
#      d. Easternmost Longitude     65W
#
#6.   How to Order Data:
#
#     Ask NCDC's Climate Services about the cost of obtaining this data set. 
#     Phone: 828-271-4800
#     FAX: 828-271-4876
#     E-mail: NCDC.Orders@noaa.gov
#
#7.   Archiving Data Center:
#
#     National Climatic Data Center 
#     Federal Building 
#     151 Patton Avenue
#     Asheville, NC  28801-5001
#     Phone: (828) 271-4800.   
#
#8.   Technical Contact:
#
#     National Climatic Data Center 
#     Federal Building 
#     151 Patton Avenue
#     Asheville, NC  28801-5001
#     Phone: (828) 271-4800.   
#
#9.   Known Uncorrected Problems: None.
#
#10.  Quality Statement: This data receives limited quality control at the station.  A discussion of quality control for sensors may be found in the ASOS USER'S GUIDE.  No attempt to edit data or correct transmission problems has been made at the NCDC.
#
#As stated in the ASOS USER'S GUIDE, March 1998, "These data have not undergone final quality control checks.  They are primarily intended for maintenance troubleshooting purposes and should not be used as valid meteorological data without extensive evaluation.
#
#Quality Control Responsibility - Responsibility for data quality control rests with NWS electronics technicians and station managers.
#
#11.  Essential Companion Datasets: None.
#
#12.  References: No information provided with original documentation.
#National Weather Service, August 1991:  ASOS USER'S GUIDE, NOAA-NWS, Silver Spring, MD.
#
#
#
#
#:
#
#
#:
#2:
#:
#
#
#:
#10:
#:
#
#
