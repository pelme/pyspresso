from itertools import zip_longest

from ._vendor.Adafruit_CharLCD import Adafruit_CharLCDPlate


class LCD:
    _lcd = Adafruit_CharLCDPlate()

    def __init__(self):
        self.temperature = 0

        # Make the equality check fail for every characther during the initial update
        self._old_rows = [
            [object()] * 15,
            [object()] * 15,
        ]
        self._cursor_col = -1
        self._cursor_row = -1

    def _render(self):
        if self.temperature:
            temperature = '{0:.2f} C'.format(self.temperature)
        else:
            temperature = '...'

        return [
            '  pyspresso!  ',
            '  {}'.format(temperature)
        ]

    def _set_char(self, col_idx, row_idx, char):
        if (self._cursor_col, self._cursor_row) != (col_idx, row_idx):
            self._lcd.set_cursor(col_idx, row_idx)

        self._cursor_col = col_idx
        self._cursor_row = row_idx

        self._lcd.message(char)
        self._cursor_col += 1

    def _update_row(self, row_idx, old_row, new_row):
        for col_idx, (old_char, new_char) in enumerate(zip_longest(old_row, new_row, fillvalue=' ')):
            if old_char != new_char:
                self._set_char(col_idx, row_idx, new_char)

    def update_screen(self):
        new_rows = self._render()

        for row_idx, (old_row, new_row) in enumerate(zip(self._old_rows, new_rows)):
            self._update_row(row_idx, old_row, new_row)

        self._old_rows = new_rows
