# SPDX-FileCopyrightText: 2022 Alec Delaney
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
`code.py`
=========

Main code for functionality, as well as functionalities involving multiple modules

* Author: Alec Delaney
"""

import time
import asyncio
import dotenv
import board
from adafruit_datetime import timedelta
from digitalio import DigitalInOut, Direction
from support.menorah import Menorah
from support.wifi_manager import WiFi
from support.setup_helper import ConnectionStatus
from valid import setup_validation, play_piezo_warning
from settings import BURNOUT

try:
    from adafruit_datetime import datetime  # pylint: disable=ungrouped-imports
except ImportError:
    pass


def display_error() -> None:
    """Displays an error using menorah lights"""
    while True:
        menorah.light_candles(8)
        time.sleep(1)
        menorah.turn_off_candles()
        time.sleep(1)


async def display_loading(
    setup_status: ConnectionStatus, interval: float = 1.0, *, loop: bool = True
) -> None:
    """Displays loading state using menorah lights

    :param ConnectonStatus setup_status: The ConnectionStatus linking the setup methods
    :param float interval: How long to wait between lighting state changes
    :param bool loop: Whether to loop until connected, or do a single cycle regardless
    """

    while not setup_status.is_connected or not loop:
        for num_candles in range(1, 5):
            menorah.light_candles(num_candles, light_shamash=False)
            await asyncio.sleep(interval)
            menorah.turn_off_candles()
        menorah.light_candles(4, light_shamash=True)
        await asyncio.sleep(interval)
        for num_candles in range(5, 9):
            menorah.light_candles(num_candles, light_shamash=True)
            await asyncio.sleep(interval)
            menorah.turn_off_candles()
        if not loop:
            break


async def setup_connections(setup_status: ConnectionStatus) -> None:
    """Connect to WiFi network and NTP server

    :param ConnectionStatus setup_status: The ConnectionStatus linking the setup methods
    """

    try:
        await wifi.connect_to_network()
        setup_status.is_connected = True
    except Exception:  # pylint: disable=broad-except
        display_error()


async def setup_menorah() -> None:
    """Set up the menorah and display loading status"""
    loading_task = asyncio.create_task(display_loading(connection_status))
    connection_task = asyncio.create_task(setup_connections(connection_status))
    await asyncio.gather(loading_task, connection_task)


def get_datetime() -> datetime:
    """Get the current datetime, attempting to reconnect if a network
    failure occurs
    """

    while True:
        try:
            return wifi.get_datetime()
        except Exception:  # pylint: disable=broad-except
            asyncio.run(display_loading(connection_status, interval=0.25, loop=False))


# pylint: disable=too-many-branches
def main() -> None:
    """Main function"""

    # Turn off lights
    menorah.turn_off_candles()

    # Load the current year into the Wi-Fi manager
    current_year = get_datetime().year
    wifi.load_year(current_year)

    # Get candle lighting times
    lighting_times = wifi.get_candle_lighting_times()

    final_override = lighting_times[7] + timedelta(hours=24) if not BURNOUT else None

    # Past candle lighting date, no need to do anything
    holiday_end = wifi.get_menorah_off_time(lighting_times[7], override=final_override)
    if get_datetime() >= holiday_end:
        while True:
            pass

    # Compare candle lighting times to current time
    for night_index, lighting in enumerate(lighting_times):

        override = (
            lighting_times[night_index + 1]
            if (night_index != 7)
            else lighting + timedelta(hours=24)
        )
        override = override if not BURNOUT else None
        off_time = wifi.get_menorah_off_time(lighting, override=override)

        if get_datetime() < lighting and (BURNOUT or night_index == 0):
            # Manage turning the candles on at the appropriate time
            while get_datetime() < lighting:
                menorah.sleep_based_on_delta(lighting, get_datetime())

        if lighting <= get_datetime() < off_time:
            # Manage turning the candles off at the appropriate time
            menorah.light_candles(night_index + 1)
            if not menorah.is_muted:
                menorah.play_sound()
            while get_datetime() < off_time:
                menorah.sleep_based_on_delta(off_time, get_datetime())
            if BURNOUT:
                menorah.turn_off_candles()

    if not BURNOUT:
        final_off_time = lighting_times[7] + timedelta(hours=24)
        while get_datetime() < final_off_time:
            menorah.sleep_based_on_delta(final_off_time, get_datetime())
        menorah.turn_off_candles()

    if is_validation:
        play_piezo_warning(menorah.piezo_pin)

    while True:
        pass


# Initialize candles
shamash = DigitalInOut(board.A2)
shamash.direction = Direction.OUTPUT
candles_pins = [
    board.MOSI,
    board.MISO,
    board.SCK,
    board.RX,
    board.TX,
    board.SCL,
    board.SDA,
    board.A3,
]
candles_dios = []
for gpio_pin in candles_pins:
    gpio_dio = DigitalInOut(gpio_pin)
    gpio_dio.direction = Direction.OUTPUT
    candles_dios.append(gpio_dio)
piezo_pin = board.A1
mute_dio = DigitalInOut(board.A0)
mute_dio.direction = Direction.INPUT  # Has built in pull-up
menorah = Menorah(shamash, candles_dios, piezo_pin, mute_dio)

wifi = WiFi()

connection_status = ConnectionStatus()

is_validation = dotenv.get_key(".env", "TEST_SERVER")
validation_type = dotenv.get_key(".env", "TEST_TYPE")

if __name__ == "__main__":
    asyncio.run(setup_menorah())
    if is_validation:
        setup_validation(menorah, wifi, validation_type)
    main()
