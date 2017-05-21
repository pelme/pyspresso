from collections import deque

import datetime

P = 0.038
I = 0.0016
D = 4.7


class PID:
    SAMPLES = 100

    def __init__(self, duty_cycle_callbacks):
        self.temperature_target = None
        self._temperatures = deque(maxlen=self.SAMPLES)
        self._callbacks = duty_cycle_callbacks
        filename = '/var/log/pyspresso/pid-{now:%Y-%m-%d_%H%M%S}.log'.format(now=datetime.datetime.now())
        self._logfile = open(filename, 'w+', encoding='utf8')

    @property
    def temperature_current(self):
        try:
            return self._temperatures[-1]
        except IndexError:
            return None

    def register_temperature(self, temperature):
        self._temperatures.append(temperature)
        duty_cycle = self.duty_cycle

        for func in self._callbacks:
            func(duty_cycle)

    @property
    def duty_cycle(self):
        if self.temperature_target is None:
            return 0

        if len(self._temperatures) <= 10:
            return 0

        p = self.temperature_target - self.temperature_current
        i = sum(self.temperature_target - x
                for x in self._temperatures
                if x < self.temperature_target)
        d = self._temperatures[-4] - self._temperatures[-1]

        result = P * p + I * i + D * d

        result = max(min(result, 1), 0)

        values = [
            self.temperature_target,
            self.temperature_current,
            p,
            i,
            d,
            result,
        ]

        self._logfile.write('\t'.join(map(str, values)).replace('.', ',') + '\n')
        self._logfile.flush()

        return result
