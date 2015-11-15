from cffi import FFI
from contextlib import contextmanager

_ffi = FFI()

_ffi.cdef("""
    typedef void (*gpioAlertFunc_t) (int gpio, int level, uint32_t tick);
    int gpioInitialise(void);
    int gpioTerminate(void);
    int gpioSetMode(unsigned gpio, unsigned mode);
    int gpioGetMode(unsigned gpio);
    int gpioSetAlertFunc(unsigned user_gpio, gpioAlertFunc_t f);
""")

PI_INPUT = 0

_libpigpio = _ffi.dlopen('pigpio')


class _pigpio:
    @contextmanager
    def alert(self, gpio, func):

        @_ffi.callback('gpioAlertFunc_t')
        def ffi_func(gpio, level, ticks):
            func(level, ticks)

        old_mode = _libpigpio.gpioGetMode(gpio)

        try:
            _libpigpio.gpioSetMode(gpio, PI_INPUT)
            _libpigpio.gpioSetAlertFunc(gpio, ffi_func)
            yield
        finally:
            _libpigpio.gpioSetAlertFunc(gpio, _ffi.NULL)
            _libpigpio.gpioSetMode(gpio, old_mode)


@contextmanager
def pigpio():
    ret = _libpigpio.gpioInitialise()
    assert ret > 0

    try:
        yield _pigpio()
    finally:
        _libpigpio.gpioTerminate()



