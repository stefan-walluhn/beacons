import time

from machine import Pin
from micropython import schedule

from beacon.led import get_led
from beacon.scenes import Scenes


scenes = Scenes(get_led(18, 19, 4),
                get_led(13, 27, 26),
                get_led(33, 25, 32))


def toggle_scenes(_):
    scenes.next()


def handle_irq(pin):
    def _bouncing():
        for i in range(14):
            if pin.value() == 1:
                return True
            time.sleep_ms(i)

        return False

    pin.irq(handler=None)
    if not _bouncing():
        schedule(toggle_scenes, None)
    pin.irq(handler=handle_irq)


if __name__ == '__main__':
    pin = Pin(23, Pin.IN, Pin.PULL_UP)
    pin.irq(trigger=Pin.IRQ_FALLING, handler=handle_irq)

    while True:
        scenes.run_forever()
        print('drained')
