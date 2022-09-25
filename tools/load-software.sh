# SPDX-FileCopyrightText: 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

# Get username and device path
username="$(whoami)"
devicepath="/run/media/$username/CIRCUITPY"

# Copy the code from microcontroller/ over to the ESP32-S2
cp -r microcontroller/. $devicepath

# Install libraries via circup
circup install -r requirements-circup.txt

# Create secrets.py for the device
cp tools/secrets_template.py $devicepath
mv $devicepath/secrets_template.py $devicepath/secrets.py
