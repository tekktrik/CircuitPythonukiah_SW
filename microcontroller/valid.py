# SPDX-FileCopyrightText: 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
`valid.py`
=========-

Validation testing code used for testing code

* Author: Alec Delaney

"""

import time
import dotenv
from pwmio import PWMOut
from settings import BURNOUT
from support import wifi_manager, menorah

try:
    import typing  # pylint: disable=unused-import
    from microcontroller import Pin  # pylint: disable=ungrouped-imports
    from support.menorah import Menorah
    from support.wifi_manager import WiFi
except ImportError:
    pass

TEST_SERVER = dotenv.get_key(".env", "TEST_SERVER")

if not TEST_SERVER:
    raise ConnectionError("Server address needed as TEST_SERVER in .env file")


def play_piezo_warning(piezo_pin: Pin, num_buzzes: int = 3) -> None:
    """Play the piezo buzzer as a warning that this is validation mode

    :param Pin piezo_pin: The pin connected to the piezo buzzer
    :param int num_buzzes: The number of buzzes to play
    """

    piezo_pwm = PWMOut(piezo_pin, frequency=256, duty_cycle=0)
    for _ in range(num_buzzes):
        piezo_pwm.duty_cycle = 65535 // 2
        time.sleep(1)
        piezo_pwm.duty_cycle = 0
        time.sleep(1)
    piezo_pwm.deinit()


def setup_validation(menorah_obj: Menorah, wifi_obj: WiFi, test_type: str) -> None:
    """Test function for validation testing

    :param Menorah menorah_obj: The Menorah object
    :param WiFi wifi_obj: The WiFi object
    """

    # Make sure test type is lowercase
    test_type = test_type.lower()

    # Play the piezo warning
    play_piezo_warning(menorah_obj.piezo_pin)

    # Setup up the test server
    wifi_obj.requests.post("http://" + TEST_SERVER + "/setup")

    for candle_time in wifi_obj.get_candle_lighting_times():
        wifi_obj.requests.patch(
            "http://" + TEST_SERVER + "/setup/time/" + candle_time.isoformat()
        )

    wifi_obj.requests.patch(
        "http://" + TEST_SERVER + "/setup/burnout/" + str(int(BURNOUT))
    )
    wifi_obj.requests.patch("http://" + TEST_SERVER + "/setup/test-type/" + test_type)
    wifi_obj.requests.patch("http://" + TEST_SERVER + "/setup/finalize")

    wifi_manager.TIME_URL = "http://" + TEST_SERVER + "/time"

    if test_type == "fast":
        menorah.SOUND_FILE = "support/test.rtttl"
