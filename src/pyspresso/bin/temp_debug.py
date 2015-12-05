import time

from ..pigpio import pigpio
from ..tsic306 import TSIC306


def main():
    last_time = time.time()
    last_temperature = 0

    def print_temperature(temperature):
        nonlocal last_time, last_temperature
        now = time.time()

        print('temperature={} time={:d} ms diff={:.4f}'.format(
            temperature,
            int((now - last_time) * 1000),
            temperature - last_temperature
        ))

        last_time = now
        last_temperature = temperature

    tsic306 = TSIC306([print_temperature])

    with pigpio() as g:
        with g.alert(13, tsic306.feed):
            while True:
                time.sleep(1000)
