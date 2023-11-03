import asyncio
import logging

from machine import Pin, PWM

from beacon import utils


def get_led(r, g, b):
    return RGB_LED(Pin(r), Pin(g), Pin(b))


class RGB_LED:
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
        asyncio.run(self.fade_color_async(color, duration))

    async def fade_async(self, color, duration=1):
        logging.debug(f'fading {self} to {color:#08x}')

        _step_ms = duration  # duration / 1000 (steps) * 1000 (ms)
        _start_color_rgb = self.color_rgb
        _target_color_rgb = utils.color_to_rgb(color)
        _distance_rgb = tuple(
            _target_color_rgb[c] - _start_color_rgb[c] for c in range(3)
        )

        for i in range(1000):
            _step_rgb = tuple(
                _start_color_rgb[c] + int(_distance_rgb[c] * (i + 1) / 1000) for c in range(3)
            )
            self.set_color(utils.rgb_to_color(_step_rgb))
            await asyncio.sleep_ms(_step_ms)
        logging.debug(f'faded {self} to {color:#08x}')
