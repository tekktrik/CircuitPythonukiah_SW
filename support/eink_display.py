import json
import time
from adafruit_ssd1681 import SSD1681
import displayio
from adafruit_sdcard import SDCard
import storage

try:
    from typing import List
    from busio import SPI
    from microcontroller import Pin
except ImportError:
    pass


class Screen(SSD1681):
    """Class for representing the E-Ink screen on the menorah
    
    :param SPI spi: The SPI bus object for the board
    :param Pin command_pin: The command pin for the e-ink screen
    :param Pin cs_pin: The chip select pin for the e-ink screen
    :param Pin reset_pin: The RESET pin for the e-ink screen
    :param Pin busy_pin: The BUSY pin for the e-ink screen
    :param int baudrate: The baudrate for the e-ink screen
    """
    
    def __init__(
        self,
        spi: SPI,
        command_pin: Pin,
        cs_pin: Pin,
        reset_pin: Pin,
        busy_pin: Pin,
        baudrate: int = 1000000,
    ):
        display_bus = displayio.FourWire(
            spi,
            command=command_pin,
            chip_select=cs_pin,
            reset=reset_pin,
            baudrate=baudrate,
        )
        super().__init__(
            display_bus,
            width=200,
            height=200,
            busy_pin=busy_pin,
            highlight_color=0xFF0000,
            rotation=180,
        )


class ScreenStorage(storage.VfsFat):
    """Class for representing the storage on the e-ink breakout
    
    :param SPI spi: The SPI busio object for the board
    :param Pin cs_pin: The chip select pin for the screen storage
    """
    
    def __init__(self, spi: SPI, cs_pin: Pin):
        self.sd_card = SDCard(spi, cs_pin)
        super().__init__(self.sd_card)
        storage.mount(self, "/sd")

    @staticmethod
    def save_lightings(datetimes: List[str]):
        with open(
            "/sd/candle_lighting_times.json", mode="w", encoding="utf-8"
        ) as jsonfile:
            json.dump(datetimes, jsonfile)

    @staticmethod
    def get_lightings():
        with open(
            "/sd/candle_lighting_times.json", mode="r", encoding="utf-8"
        ) as jsonfile:
            return json.load(jsonfile)
