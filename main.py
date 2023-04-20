import time
import uasyncio

from machine import Pin
from micropython import schedule

from beacon.led import get_led
from beacon.scenes import TestScene


def handle_irq(pin):
    def _bouncing(pin):
        for _ in range(10):
            if pin.value() == 1:
                return True
            time.sleep_ms(10)

        return False

    if not _bouncing(pin):
        print('trigger')


def run(led1, led2, led3):
    uasyncio.run(uasyncio.gather(led1.fade_color_async(0x0000ff),
                                 led2.fade_color_async(0xff0000),
                                 led3.fade_color_async(0x00cc00)))
    time.sleep(1)
    uasyncio.run(uasyncio.gather(led1.fade_color_async(0xff0000),
                                 led2.fade_color_async(0x0000cc),
                                 led3.fade_color_async(0xcc00cc)))
    time.sleep(1)
    uasyncio.run(uasyncio.gather(led1.fade_color_async(0xff9900),
                                 led2.fade_color_async(0xff9900),
                                 led3.fade_color_async(0xff9900)))
    time.sleep(1)
    uasyncio.run(uasyncio.gather(led1.fade_color_async(0, duration=3),
                                 led2.fade_color_async(0, duration=5),
                                 led3.fade_color_async(0, duration=5)))


def nee_naw(led1, led2):
    while True:
        for _ in range(20):
            led1.set_color(0xff0000)
            led2.set_color(0x0000ff)
            time.sleep_ms(150)
            led2.set_color(0xff0000)
            led1.set_color(0x0000ff)
            time.sleep_ms(150)

        for _ in range(3):
            uasyncio.run(uasyncio.gather(led1.fade_color_async(0xff0000),
                                         led2.fade_color_async(0x0000ff)))
            uasyncio.run(uasyncio.gather(led2.fade_color_async(0xff0000),
                                         led1.fade_color_async(0x0000ff)))


if __name__ == '__main__':
    pin = Pin(23, Pin.IN, Pin.PULL_UP)
    pin.irq(trigger=Pin.IRQ_FALLING, handler=handle_irq)

    scene = TestScene(get_led(18, 19, 4),
                      get_led(13, 27, 26),
                      get_led(33, 25, 32))

    scene.start()
