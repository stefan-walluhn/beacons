import time

from machine import Pin
from micropython import schedule

from beacon.led import get_led
from beacon.scenes import TestScene


def handle_irq(pin):
    def _bouncing():
        for i in range(14):
            if pin.value() == 1:
                return True
            time.sleep_ms(i)

        return False

    pin.irq(handler=None)
    if not _bouncing():
        print('trigger')
    pin.irq(handler=handle_irq)


if __name__ == '__main__':
    pin = Pin(23, Pin.IN, Pin.PULL_UP)
    pin.irq(trigger=Pin.IRQ_FALLING, handler=handle_irq)

    scene = TestScene(get_led(18, 19, 4),
                      get_led(13, 27, 26),
                      get_led(33, 25, 32))

    scene.start()
