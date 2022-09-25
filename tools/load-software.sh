# SPDX-FileCopyrightText: 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

# Copy the code from microcontroller/ over to the ESP32-S2
cp -r microcontroller/. $1

# Install libraries via circup
circup install -r requirements-circup.txt

# Create secrets.py for the device
cp tools/secrets_template.py $1/
mv $1/secrets_template.py $1/secrets.py
