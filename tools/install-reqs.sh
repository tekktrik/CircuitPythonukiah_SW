# SPDX-FileCopyrightText: 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

# Transform the circup requirements for GitHub Actions
while read -r line
do
    if [[ $line != "" && $line != "#"* ]]
    then
        circupreq=$(awk -F 'adafruit_' '{print $NF}' <<< $line)
        pipreq=$(tr _ - <<< "adafruit-circuitpython-$circupreq")
        pip install $pipreq
    fi
done < requirements-circup.txt
