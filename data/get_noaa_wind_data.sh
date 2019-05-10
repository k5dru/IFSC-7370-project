

getfile()
{
    # file, localpath, remotepath
    file=${1}
    localpath=${2}
    remotepath=${3}

    if [ -f "$localpath/${file}.gz" -o -f "$localpath/{$file}" ]; then
       return  # local file already exists
    fi

     if [ ! -d ${localpath} ]; then
        echo mkdir -p $localpath
        mkdir -p $localpath
    fi

    echo wget "${remotepath}/${file}" 
    ( cd $localpath && wget -nc "${remotepath}/${file}" )
    #  compress file(s) locally
    find "${localpath}/" -name '*dat' -ls -exec gzip -v {} \;
    echo sleeping 
    sleep 3
}


# little rock, 2019
#getfile 64010KLIT201901.dat /home/lemley/noaawind ftp://ftp.ncdc.noaa.gov/pub/data/asos-fivemin/6401-2019

for YEAR in 2009 2010 2011 2012 2013 2018 2017 2016 2015 2014; do 
for MON in 01 02 03 04 05 06 07 08 09 10 11 12; do 
for station in $(
# Station location database: http://www.weatherroanoke.com/digatmos.stn
# get from 32N to 49N, and from 105W to 94W
for lat in $(seq -w 32 49); do 
  for lon in $(seq 94 105); do 
	# get all the station calls from a geographical range
    grep "|${lat}\\.[0-9]*|-${lon}\\." asos_stations.csv | cut -f 4 -d '|' | sed 's/^/K/'
  done
done 
echo KLIT
); do
(grep $station noaastations.txt > /dev/null) && getfile 64010${station}${YEAR}${MON}.dat /home/lemley/project/noaawind ftp://ftp.ncdc.noaa.gov/pub/data/asos-fivemin/6401-${YEAR}
done
done 
done

