find noaawind -name '*gz' | while read infile; do 
  gzip -dc $infile | python3 parseweather.py | psql -c "\\copy weather_5min from stdin with (format CSV)"
  err=$?
  echo file $infile returns $err 
done
