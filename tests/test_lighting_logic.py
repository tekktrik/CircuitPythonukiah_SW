# SPDX-FileCopyrightText: 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
`test_lighting_logic`
=====================

Tests the logic of the delays for sleeping

* Author(s): Alec Delaney

"""

import sys
import os
import secrets
import requests
import adafruit_datetime


secrets.location = {
    "zipcode": None,
}

current_path = os.path.normpath(__file__)
current_path_comps = current_path.split(os.sep)
support_path = os.sep + os.path.join(*current_path_comps[:-2])
sys.path.append(support_path)

# pylint: disable=wrong-import-position

from support.menorah import Menorah
from support import wifi_manager
from support.wifi_manager import WiFi

# pylint: enable=wrong-import-position

wifi = WiFi()
wifi.requests = requests


def test_lighting_times(monkeypatch, location):
    """Test the lighting time logic"""

    secrets_location = {
        "zipcode": location,
    }
    monkeypatch.setattr(wifi_manager, "location", secrets_location)
    lighting_times = wifi.get_candle_lighting_times()

    for lighting_time in lighting_times:

        off_time = wifi.get_menorah_off_time(lighting_time)

        assertion_pairs = []

        assertion_pairs.append(
            (lighting_time, lighting_time - adafruit_datetime.timedelta(hours=12), 600)
        )
        assertion_pairs.append(
            (
                lighting_time,
                lighting_time - adafruit_datetime.timedelta(minutes=55),
                600,
            )
        )
        assertion_pairs.append(
            (lighting_time, lighting_time - adafruit_datetime.timedelta(minutes=5), 60)
        )
        assertion_pairs.append(
            (lighting_time, lighting_time - adafruit_datetime.timedelta(seconds=28), 28)
        )
        assertion_pairs.append(
            (off_time, lighting_time + adafruit_datetime.timedelta(seconds=28), 600)
        )
        assertion_pairs.append(
            (off_time, lighting_time + adafruit_datetime.timedelta(minutes=55), 600)
        )
        assertion_pairs.append(
            (off_time, lighting_time + adafruit_datetime.timedelta(hours=3), 600)
        )
        assertion_pairs.append(
            (off_time, lighting_time + adafruit_datetime.timedelta(hours=9), 600)
        )
        assertion_pairs.append(
            (
                off_time,
                lighting_time + adafruit_datetime.timedelta(hours=11, minutes=53),
                60,
            )
        )
        assertion_pairs.append(
            (
                off_time,
                lighting_time
                + adafruit_datetime.timedelta(hours=11, minutes=59, seconds=25),
                35,
            )
        )

        for event_time, mock_time, expected_sleep in assertion_pairs:
            assert (
                Menorah.get_sleep_time_based_on_delta(event_time, mock_time)
                == expected_sleep
            )
