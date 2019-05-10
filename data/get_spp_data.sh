# script to retrieve 36780 data files from SPP

getfile()
{
    # file, localpath, remotepath
    file=${1}
    localpath=${2}
    remotepath=${3}

    if [ -f "${localpath}/${file}" -o -f "${localpath}/${file}.gz" -o -f "${localpath}/${file}.7z" ]; then
       return  # local file already exists
    fi

     if [ ! -d ${localpath} ]; then
        echo mkdir -p $localpath
        mkdir -p $localpath
    fi

    echo wget "${remotepath}/${file}" 
    ( cd $localpath && wget -nc --timeout=60 "${remotepath}/${file}" )
    #  compress file(s) locally
    find "${localpath}/" -name '*csv' -ls -exec gzip -v {} \;
    echo sleeping
    sleep 11
}

PrevYMD=""

for Y in 2014 2015 2016; do
  for M in 01 02 03 04 05 06 07 08 09 10 11 12; do
     if [ $Y == "2014" -a $M == "01" ]; then continue; fi
     if [ $Y == "2014" -a $M == "02" ]; then continue; fi
     if [ $Y == "2016" -a $M -gt 7 ]; then 
	       break
     fi
     for D in $(seq -w 01 31); do
       if [ $Y == "2016" -a $M == "07" -a $D == "16" ]; then 
	       break
       fi
       if [ $M == "02" -a $D == "29" -a ! $Y == "2016" ]; then continue; fi  # remember 2016 leap year
       if [ $M == "02" -a $D == "30" ]; then continue; fi
       if [ $M == "02" -a $D == "31" ]; then continue; fi
       if [ $M == "04" -a $D == "31" ]; then continue; fi
       if [ $M == "06" -a $D == "31" ]; then continue; fi
       if [ $M == "09" -a $D == "31" ]; then continue; fi
       if [ $M == "11" -a $D == "31" ]; then continue; fi
#         for H in 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23; do
#            for MM in 00 05 10 15 20 25 30 35 40 45 50 55; do
#                file="RTBM-LMP-SL-$Y$M$D$H$MM.csv"
#                YMD="$Y/$M/$D"
#                if [ $H == "00" -a $MM == "00" ]; then
#                    if [ -z "$PrevYMD" ]; then
#                        continue
#                    fi
#                    YMD=$PrevYMD
#                fi
#                localpath="/home/lemley/spp_data/$YMD"
#                remotepath="ftp://pubftp.spp.org/Markets/RTBM/LMP_By_SETTLEMENT_LOC/$YMD"
#                getfile ${file} ${localpath} ${remotepath}
#                PrevYMD=$YMD
#            done
#         done
       YMD="$Y/$M/$D"
       file="*"
       remotepath="ftp://pubftp.spp.org/Markets/RTBM/LMP_By_SETTLEMENT_LOC/$YMD"
       localpath="/home/lemley/spp_data/$YMD"
       localfiles=$(find $localpath -type f 2>/dev/null | wc -l )
       if [ ! -z "$localfiles" -a $localfiles -gt 100 ]; then 
          echo $localpath appears full already 
          continue
       fi
      getfile "${file}" "${localpath}" "${remotepath}"
    done
  done
done

for Y in 2016 2017 2018; do
  for M in 01 02 03 04 05 06 07 08 09 10 11 12; do
     if [ $Y == "2016" -a $M == "01" ]; then continue; fi
     if [ $Y == "2016" -a $M == "02" ]; then continue; fi
     if [ $Y == "2016" -a $M == "03" ]; then continue; fi
     if [ $Y == "2016" -a $M == "04" ]; then continue; fi
     if [ $Y == "2016" -a $M == "05" ]; then continue; fi
     if [ $Y == "2016" -a $M == "06" ]; then continue; fi
     for D in $(seq -w 01 31); do
       if [ $Y == "2016" -a $M == "07" -a $D -lt 16 ]; then continue; fi
       if [ $M == "02" -a $D == "29" -a ! $Y == "2016" ]; then continue; fi  # remember 2016 leap year
       if [ $M == "02" -a $D == "30" ]; then continue; fi
       if [ $M == "02" -a $D == "31" ]; then continue; fi
       if [ $M == "04" -a $D == "31" ]; then continue; fi
       if [ $M == "06" -a $D == "31" ]; then continue; fi
       if [ $M == "09" -a $D == "31" ]; then continue; fi
       if [ $M == "11" -a $D == "31" ]; then continue; fi
            file="RTBM-LMP-DAILY-SL-$Y$M$D.csv"
            localpath="/home/lemley/spp_data/$Y/$M/By_Day"
            remotepath="ftp://pubftp.spp.org/Markets/RTBM/LMP_By_SETTLEMENT_LOC/$Y/$M/By_Day"
            getfile "${file}" "${localpath}" "${remotepath}"
     done
   done
done


