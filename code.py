import board
import busio
from digitalio import DigitalInOut, Direction
from support.menorah import Menorah
from support.wifi_manager import WiFi
from support.eink_display import Screen, ScreenStorage

# TODO: INITIALIZATION HERE

# Initialize SPI
sck_pin = board.GP18
copi_pin = board.GP19
cipo_pin = board.GP16
spi = busio.SPI(sck_pin, copi_pin, cipo_pin)

# Initialize ESP32
esp32_cs = DigitalInOut(board.GP17)
esp32_ready = DigitalInOut(board.GP20)
esp32_reset = DigitalInOut(board.GP21)
esp32_gpio0 = DigitalInOut(board.GP22)
esp32 = WiFi(spi, esp32_cs, esp32_ready, esp32_reset, esp32_gpio0)

# Initialize candles
shamash = DigitalInOut(board.GP15)
shamash.direction = Direction.OUTPUT
candles = []
for gpio_num in range(14, 6, -1):
    gpio_str = "GP" + str(gpio_num)
    gpio_dio = DigitalInOut(getattr(board, gpio_str))
    gpio_dio.direction = Direction.OUTPUT
    candles.append(gpio_dio)
menorah = Menorah(shamash, candles)
    
# Initialize screen and screen storage
screen_command = board.GP6
screen_cs = board.GP5
screen_reset = board.GP4
screen_busy = board.GP3
#sram_cs = board.GP2
#sd_cs = board.GP1
screen = Screen(spi, screen_command, screen_cs, screen_reset, screen_busy)
#storage = ScreenStorage(spi, sd_cs)

def main():
    
    pass

if __name__ == "__main__":
    main()