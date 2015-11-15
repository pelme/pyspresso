import time

from collections import deque, namedtuple

_Reading = namedtuple('_Reading', ['level', 'diff'])


def _parity(number):
    return bin(number).count('1') % 2


class BadData(Exception):
    pass


class BadParity(BadData):
    pass


class BadTemperature(BadData):
    pass


class TSIC306:
    def __init__(self, callbacks):
        self._last_ticks = 0
        self._readings = deque(maxlen=40)
        self._callbacks = callbacks

    def has_temperature_data(self):
        first_diff = self._readings[0].diff
        return len(self._readings) == 40 and max(r.diff for r in self._readings) == first_diff

    def calculate_temperature(self):
        MIN_TEMP = -50
        MAX_TEMP = 150
        SCALE_FACTOR = 1000

        result = ((MAX_TEMP - MIN_TEMP) * SCALE_FACTOR * self._raw_data() // 2047 + MIN_TEMP * SCALE_FACTOR) / 1000

        if MIN_TEMP <= result <= MAX_TEMP:
            return result
        else:
            raise BadTemperature('{} is outside of min/max'.format(result))

    def feed(self, level, ticks):
        self._readings.append(_Reading(level=level, diff=ticks - self._last_ticks))
        self._last_ticks = ticks

        if self.has_temperature_data():
            try:
                temperature = self.calculate_temperature()
            except BadData:
                pass
            else:
                for callback in self._callbacks:
                    callback(temperature)

    def _strobe_length(self):
        return (self._readings[1].diff + self._readings[2].diff) // 2

    def _bit(self, reading_idx):
        return 1 if self._readings[reading_idx].diff < self._strobe_length() else 0

    def _byte(self, start_offset):
        byte = sum(self._bit(start_offset + bit_num * 2) << (7 - bit_num) for bit_num in range(8))

        expected_parity = self._bit(start_offset + 8 * 2)
        actual_parity = _parity(byte)

        if expected_parity != actual_parity:
            raise BadParity('expected parity {expected_parity}, got {actual_parity} (byte {byte})'.format(
                expected_parity=expected_parity,
                actual_parity=actual_parity,
                byte=byte,
            ))

        return byte

    def _raw_data(self):
        high = self._byte(3)
        low = self._byte(23)

        if high & 0b11111000 != 0:
            raise BadData('bad 5 high bits')

        return high << 8 | low
