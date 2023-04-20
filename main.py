import time

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


if __name__ == '__main__':
    pin = Pin(23, Pin.IN, Pin.PULL_UP)
    pin.irq(trigger=Pin.IRQ_FALLING, handler=handle_irq)

    scene = TestScene(get_led(18, 19, 4),
                      get_led(13, 27, 26),
                      get_led(33, 25, 32))

    scene.start()
