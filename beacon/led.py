import asyncio
import logging

from machine import Pin, PWM

from beacon import utils


def get_led(r, g, b):
    return RGB_LED(Pin(r), Pin(g), Pin(b))


class RGB_LED:
    # heads up: to many fade steps lead to improper timings, because of short
    # async sleep windows. see also
    # https://github.com/peterhinch/micropython-async/blob/master/v3/docs/TUTORIAL.md#23-delays
    FADE_STEPS = 100

    def __init__(self, red_pin, green_pin, blue_pin):
        self._rgb_pwm = tuple(
            PWM(p, freq=1000, duty_u16=65535) for p in [red_pin,
                                                        green_pin,
                                                        blue_pin]
        )

    @property
    def color_rgb(self):
        return tuple(
            utils.uduty16_to_uint8(
                self._rgb_pwm[c].duty_u16()
            ) for c in range(3)
        )

    @property
    def color(self):
        return utils.rgb_to_color(self.color_rgb)

    def set_color(self, color):
        rgb = utils.color_to_rgb(color)

        for c in range(3):
            self._rgb_pwm[c].duty_u16(
                utils.uint8_to_uduty16(rgb[c])
            )

    def fade(self, color, duration=1):
        asyncio.run(self.fade_async(color, duration))

    async def fade_async(self, color, duration=1):
        logging.debug(f'fading {self} to {color:#08x}')

        _step_ms = duration * 1000 // RGB_LED.FADE_STEPS
        _start_color_rgb = self.color_rgb
        _target_color_rgb = utils.color_to_rgb(color)
        _distance_rgb = tuple(
            _target_color_rgb[c] - _start_color_rgb[c] for c in range(3)
        )

        for i in range(RGB_LED.FADE_STEPS):
            _step_rgb = tuple(
                map(
                    lambda c: (
                        _distance_rgb[c] * (i + 1) // RGB_LED.FADE_STEPS +
                        _start_color_rgb[c]
                    ),
                    range(3))
            )
            self.set_color(utils.rgb_to_color(_step_rgb))
            await asyncio.sleep_ms(_step_ms)
        logging.debug(f'faded {self} to {color:#08x}')
