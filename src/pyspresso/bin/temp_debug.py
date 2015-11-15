import time

from ..pigpio import pigpio
from ..tsic306 import TSIC306


def main():
    def print_temperature(temperature):
        print('temperature = {}'.format(temperature))

    tsic306 = TSIC306([print_temperature])

    with pigpio() as g:
        with g.alert(20, tsic306.feed):
            while True:
                time.sleep(1000)
