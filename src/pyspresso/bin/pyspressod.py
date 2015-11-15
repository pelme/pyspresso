import time

from ..lcd import LCD
from ..pigpio import pigpio
from ..tsic306 import TSIC306
from ..relay import Relay


def main():

    def update_lcd_temperature(temperature):
        lcd.temperature = temperature

    lcd = LCD()
    tsic306 = TSIC306([update_lcd_temperature])

    with pigpio() as pig:
        with pig.alert(20, tsic306.feed):
            while True:
                lcd.update_screen()
                time.sleep(0.3)
