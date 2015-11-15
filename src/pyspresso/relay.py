from gpiozero import PWMOutputDevice


class Relay:

    def __init__(self):
        self._relay = PWMOutputDevice(pin=21, frequency=2)
        self._relay.value = 0

    def set_duty_cycle(self, duty_cycle):
        self._relay.value = duty_cycle
