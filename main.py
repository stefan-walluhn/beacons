import logging
import time

from machine import Pin
from micropython import schedule

from beacon.led import get_led
from beacon.scenes import Scenes


scenes = Scenes(get_led(18, 19, 4),
                get_led(13, 27, 26),
                get_led(33, 25, 32))


def toggle_scenes():
    logging.info('toggle scenes')
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
        logging.info('button triggered')
        toggle_scenes()
    pin.irq(handler=handle_irq)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    logging.info('setup trigger pin')
    pin = Pin(23, Pin.IN, Pin.PULL_UP)
    pin.irq(trigger=Pin.IRQ_FALLING, handler=handle_irq)

    while True:
        scenes.run_forever()
        logging.warning('event loop drained')
