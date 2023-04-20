import time
import uasyncio


class TestScene:
    def __init__(self, led1, led2, led3):
        self._led1, self._led2, self._led3 = led1, led2, led3

    def start(self):
        uasyncio.run(
            uasyncio.gather(self._led1.fade_color_async(0x0000ff),
                            self._led2.fade_color_async(0xff0000),
                            self._led3.fade_color_async(0x00cc00))
        )

        time.sleep(1)

        uasyncio.run(
            uasyncio.gather(self._led1.fade_color_async(0xff0000),
                            self._led2.fade_color_async(0x0000cc),
                            self._led3.fade_color_async(0xcc00cc))
        )

        time.sleep(1)

        uasyncio.run(
            uasyncio.gather(self._led1.fade_color_async(0xff9900),
                            self._led2.fade_color_async(0xff9900),
                            self._led3.fade_color_async(0xff9900))
        )

        time.sleep(1)

        uasyncio.run(
            uasyncio.gather(self._led1.fade_color_async(0, duration=3),
                            self._led2.fade_color_async(0, duration=5),
                            self._led3.fade_color_async(0, duration=5))
        )
