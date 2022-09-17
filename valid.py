# SPDX-FileCopyrightText: 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

import time
import dotenv
from pwmio import PWMOut
from settings import BURNOUT

try:
    import typing  # pylint: disable=unused-import
    from microcontroller import Pin
    from support.menorah import Menorah
    from support.wifi_manager import WiFi
except ImportError:
    pass

TEST_SERVER = dotenv.get_key("TEST_SERVER")

if not TEST_SERVER:
    raise ConnectionError("Server address needed as TEST_SERVER in .env file")

def play_piezo_warning(piezo_pin: Pin, num_buzzes: int = 5) -> None:
    """Play the piezo buzzer as a warning that this is
    validation mode
    """

    piezo_pwm = PWMOut(piezo_pin, frequency=256, duty_cycle=0)
    for _ in range(num_buzzes):
        piezo_pwm.duty_cycle = 65535 // 2
        time.sleep(1)
        piezo_pwm.duty_cycle = 0
        time.sleep(1)
    piezo_pwm.deinit()

def setup_validation(menorah: Menorah, wifi: WiFi) -> None:
    """Test function for validation testing"""

    # Play the piezo warning
    play_piezo_warning(menorah.piezo_pin)

    # Setup up the test server
    candle_lighting_times = wifi.get_candle_lighting_times()
    payload = {
        "times": candle_lighting_times,
        "burnout": BURNOUT,
    }
    wifi.requests.post(TEST_SERVER+"/time/setup", data=payload)

    # Monkeypatch a new get_time() method for testing
    def get_time(self) -> str:
        """Validation version of the time getting method"""
        response = self.requests.get(TEST_SERVER + "/time")
        return response.text
    wifi.get_time = get_time

    # Monkeypatch a new play_sound() method for testing
    def play_sound(self, filename: str) -> None:
        """Play a single tone instead of a song"""
        piezo_pwm = PWMOut(self.piezo_pin, frequency=512, duty_cycle=0)
        piezo_pwm.duty_cycle = 65535 // 2
        time.sleep(1)
        piezo_pwm.duty_cycle = 0
        piezo_pwm.deinit()
    menorah.play_sound = play_sound
