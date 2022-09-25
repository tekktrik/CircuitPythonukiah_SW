# SPDX-FileCopyrightText: 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

# Check if version was suppiled, rause error if not
if [[ $1 == "" ]]
then
    echo "Please provide a version of CircuitPython to load!"
    exit 1
fi

# Get CircuitPython URL
uf2file="adafruit-circuitpython-adafruit_qtpy_esp32s2-en_US-$1.uf2"
cpyurl="https://downloads.circuitpython.org/bin/adafruit_qtpy_esp32s2/en_US/$uf2file"
archive="tools/archive"

# Get device to mount
echo "Looking for QTPYS2BOOT device..."
while read -r line
do
    if [[ $line == *"QTPYS2BOOT"* ]]
    then
        echo "Found QTPYS2BOOT device!"
        devicename=$(awk -F'/' '{print $NF}' <<< $line)
        devicepath="/dev/$devicename"
    fi 
done < <(ls -l /dev/disk/by-label)

# Raise error if device was not found
if [[ -z $devicepath ]]
then
    echo "QTPYS2BOOT device not found!"
    exit 1
fi

# Get device mount path
mountpath="/mnt/QTPYS2BOOT"

# Create mount folder if needed, and clear contents
echo "Creating mount point..."
if [[ -d $mountpath ]]
then
    rm -r $mountpath
fi
mkdir $mountpath

# Mount as USB
echo "Mounting..."
mount $devicepath $mountpath

# Create archive directory if needed
if [[ ! -d $archive ]]
then
    echo "Creating archive folder for UF2 folders"
    mdkir $archive
fi

# Download the file to the archive directory if needed
if [[ ! -f $archive/$uf2file ]]
then
    echo "Downloading new UF2 file from the internet..."
    wget -q $cpyurl -P $archive
else
    echo "UF2 previously downloaded, using file in archive."
fi

# Copy the code from microcontroller/ over to the CircuitPythonukiah
echo "Copying the UF2 file to QTPYS2BOOT..."
cp -r $archive/$uf2file $devicepath

# Unmount the CircuitPythonukiah and remove folder
echo "Removing mount point and cleaning up..."
umount $devicepath
rm -r $mountpath

# Announce completion
echo "Done loading firmware!"
