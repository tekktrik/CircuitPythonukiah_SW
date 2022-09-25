while read -r line
do
    if [[ $line != "" && $line != "#"* ]]
    then
        circupreq=$(awk -F 'adafruit_' '{print $NF}' <<< $line)
        pipreq=$(tr _ - <<< "adafruit-circuitpython-$circupreq")
        pip install $pipreq
    fi
done < requirements-circup.txt
