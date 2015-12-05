from itertools import zip_longest
import threading

import time

from ._vendor.Adafruit_CharLCD import Adafruit_CharLCDPlate, SELECT, RIGHT, DOWN, UP, LEFT


def noop():
    pass


class LCDButtons:
    _lcd = Adafruit_CharLCDPlate()
    _io_lock = threading.Lock()

    def __init__(self, *, on_up=noop, on_down=noop, on_left=noop, on_right=noop, on_select=noop):
        # Make the equality check fail for every character during the initial update
        self._old_rows = [
            [object()] * 15,
            [object()] * 15,
        ]
        self._cursor_col = -1
        self._cursor_row = -1

        self._on_up = on_up
        self._on_down = on_down
        self._on_left = on_left
        self._on_right = on_right
        self._on_select = on_select

        self._thread = threading.Thread(target=self._button_thread_watcher,
                                        name='button poller')

        self._thread.start()

    def _render(self, *, pid):

        def fmt(temp):
            if temp is not None:
                return '{0:.1f}'.format(temp)
            else:
                return '-'

        return [
            '{current} / {target} C'.format(current=fmt(pid.temperature_current), target=fmt(pid.temperature_target)),
            '{} %'.format(int(pid.duty_cycle * 100))
        ]

    def _set_char(self, col_idx, row_idx, char):
        if (self._cursor_col, self._cursor_row) != (col_idx, row_idx):
            with self._io_lock:
                self._lcd.set_cursor(col_idx, row_idx)

        self._cursor_col = col_idx
        self._cursor_row = row_idx

        with self._io_lock:
            self._lcd.message(char)
        self._cursor_col += 1

    def _update_row(self, row_idx, old_row, new_row):
        for col_idx, (old_char, new_char) in enumerate(zip_longest(old_row, new_row, fillvalue=' ')):
            if old_char != new_char:
                self._set_char(col_idx, row_idx, new_char)

    def set_temperature_current(self, temperature):
        self.temperature_current = temperature

    def update_screen(self, **context):
        new_rows = self._render(**context)

        for row_idx, (old_row, new_row) in enumerate(zip(self._old_rows, new_rows)):
            self._update_row(row_idx, old_row, new_row)

        self._old_rows = new_rows

    def _button_thread_watcher(self):
        buttons = [
            (SELECT, self._on_select),
            (RIGHT, self._on_right),
            (DOWN, self._on_down),
            (UP, self._on_up),
            (LEFT, self._on_left),
        ]

        pressed_buttons = set()

        while True:
            for button, func in buttons:
                with self._io_lock:
                    is_pressed = self._lcd.is_pressed(button)

                if is_pressed:
                    pressed_buttons.add(button)
                elif not is_pressed and button in pressed_buttons:
                    pressed_buttons.remove(button)
                    func()

            time.sleep(0.1)