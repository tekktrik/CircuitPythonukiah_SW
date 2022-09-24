# SPDX-FileCopyrightText: 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

# Copy the code from microcontroller/ over to the ESP32-S2
cp -r microcontroller/. $1

# Install libraries via circup
circup install -r requirements-circup.txt

# Create secrets.py and write the template to it
cp tools/secrets_template.py $1/
mv $1/secrets_template.py $1/secrets.py
