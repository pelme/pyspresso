import json


MODE_ESPRESSO = 'temperature_espresso'
MODE_STEAM = 'temperature_steam'


class State:
    filename = '/var/lib/pyspresso.json'
    defaults = {
        MODE_ESPRESSO: 95,
        MODE_STEAM: 140,
    }

    def __init__(self, temperature_callbacks):
        self._mode = MODE_ESPRESSO
        self._temperature_callbacks = temperature_callbacks

        try:
            with open(self.filename, 'r+', encoding='utf8') as f:
                self._data = json.load(f)
        except FileNotFoundError:
            self._data = {}

        self._notify()

    def temperature_change_func(self, change):
        def func():
            self._change_temperature(change)

        return func

    def switch_mode(self):
        self._mode = MODE_ESPRESSO if self._mode == MODE_STEAM else MODE_STEAM
        self._notify()

    def _current_temperature(self):
        return self._data.get(self._mode, self.defaults[self._mode])

    def _change_temperature(self, diff):
        new = self._current_temperature() + diff

        self._data[self._mode] = new

        with open(self.filename, 'w+', encoding='utf8') as f:
            json.dump(self._data, f)

        self._notify()

    def _notify(self):
        current = self._current_temperature()

        for func in self._temperature_callbacks:
            func(current)
