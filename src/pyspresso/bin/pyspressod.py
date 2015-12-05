import time
from functools import partial

from ..lcd_buttons import LCDButtons
from ..pigpio import pigpio
from ..tsic306 import TSIC306
from ..relay import Relay
from ..pid import PID
from ..state import State


def main():
    relay = Relay()
    pid = PID([relay.set_duty_cycle])

    state = State([partial(setattr, pid, 'temperature_target')])
    tsic306 = TSIC306([pid.register_temperature])

    lcd_buttons = LCDButtons(
        on_up=state.temperature_change_func(0.5),
        on_down=state.temperature_change_func(-0.5),
        on_left=state.temperature_change_func(-5),
        on_right=state.temperature_change_func(5),
        on_select=state.switch_mode,
    )

    with pigpio() as pig:
        with pig.alert(13, tsic306.register_level_change):
            while True:
                lcd_buttons.update_screen(pid=pid)
                time.sleep(0.1)
