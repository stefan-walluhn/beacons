import logging
import asyncio

from random import randint


class Scenes:
    def __init__(self, led_floor, *led_leaves):
        self._scenes = (
            DaylightFlickering(led_floor, *led_leaves),
            ThunderStorm(led_floor, *led_leaves),
            JapanDaemonParade(led_floor, *led_leaves),
            Sunset(led_floor, *led_leaves),
        )
        self._current = -1

    def run_forever(self):
        self.next()

        logging.debug('starting event loop')
        asyncio.get_event_loop().run_forever()

    def next(self):
        loop = asyncio.get_event_loop()
        loop.stop()
        logging.debug('stopped event loop')
        loop.close()
        logging.debug('closed event loop')

        loop = asyncio.new_event_loop()

        self._current = (self._current + 1) % len(self._scenes)
        logging.info('creating scene '
                     f'{self._scenes[self._current].__class__.__name__}')
        loop.create_task(self._scenes[self._current].run())


class Scene:
    def __init__(self, led_floor, *led_leaves):
        self._led_floor, self._led_leaves = led_floor, led_leaves

    async def run(self):
        raise NotImplementedError('Scene must implement run coro')


class DaylightFlickering(Scene):
    async def flicker(self, led):
        while True:
            await led.fade_async(0xff9933, duration=randint(1, 5))
            await led.fade_async(0xffff33, duration=randint(1, 5))

    async def run(self):
        await self._led_floor.fade_async(0x996600, duration=5)
        await asyncio.gather(
            self._led_leaves[0].fade_async(0xff9933),
            self._led_leaves[1].fade_async(0xffff33, duration=2)
        )
        await asyncio.gather(self.flicker(self._led_leaves[0]),
                             self.flicker(self._led_leaves[1]))


class ThunderStorm(Scene):
    async def lightning(self, led):
        while True:
            await self._sleep(randint(10, 60))

            for _ in range(randint(1, 6)):
                led.set_color(0xffffff)
                await asyncio.sleep_ms(randint(10, 150))
                led.set_color(0x112200)
                await asyncio.sleep_ms(randint(100, 250))

    async def run(self):
        await asyncio.gather(
            self._led_floor.fade_async(0x112200, duration=5),
            self._led_leaves[0].fade_async(0x112200, duration=5),
            self._led_leaves[1].fade_async(0x112200, duration=5),
        )

        await asyncio.gather(self.lightning(self._led_floor),
                             self.lightning(self._led_leaves[0]),
                             self.lightning(self._led_leaves[1]))

    async def _sleep(self, t):
        # cut sleep awaitable in small chunks, loop.stop() is unable to
        # terminate running task. newly created tasks will be affected by this
        # sleep.
        for _ in range(100):
            await asyncio.sleep_ms(t * 10)


class JapanDaemonParade(Scene):
    async def flicker_leaves(self, leds):
        while True:
            duration = randint(1, 5)
            await leds[0].fade_async(0xcc9900, duration=duration)
            await leds[1].fade_async(0xff0000, duration=duration)
            duration = randint(1, 5)
            await leds[0].fade_async(0xff0000, duration=duration)
            await leds[1].fade_async(0xcc9900, duration=duration)

    async def flicker_floor(self, led):
        while True:
            await led.fade_async(0x660066, duration=randint(1, 5))
            await led.fade_async(0x3300cc, duration=randint(1, 5))

    async def run(self):
        await asyncio.gather(
            self._led_floor.fade_async(0x3300cc, duration=5),
            self._led_leaves[0].fade_async(0xff0000, duration=5),
            self._led_leaves[1].fade_async(0xcc9900, duration=5),
        )

        await asyncio.gather(self.flicker_leaves(self._led_leaves),
                             self.flicker_floor(self._led_floor))


class Sunset(Scene):
    async def sleep_forever(self):
        while True:
            await asyncio.sleep(1)

    async def run(self):
        await asyncio.gather(
            self._led_floor.fade_async(0xffff33),
            self._led_leaves[0].fade_async(0xffff33),
            self._led_leaves[1].fade_async(0xffff33)
        )

        await asyncio.gather(
            self._led_floor.fade_async(0xfb8835, duration=20),
            self._led_leaves[0].fade_async(0xfeb913, duration=10),
            self._led_leaves[1].fade_async(0xffd51a, duration=20)
        )

        await asyncio.gather(
            self._led_floor.fade_async(0x79432b, duration=30),
            self._led_leaves[0].fade_async(0xff2211, duration=30),
            self._led_leaves[1].fade_async(0x5196b7, duration=40),
        )

        await asyncio.gather(
            self._led_floor.fade_async(0x000000, duration=20),
            self._led_leaves[0].fade_async(0x000033, duration=40),
            self._led_leaves[1].fade_async(0x040033, duration=30)
        )

        await asyncio.gather(
            self._led_leaves[0].fade_async(0x000000, duration=20),
            self._led_leaves[1].fade_async(0x000000, duration=20)
        )

        # hacky workaround to not let scene finish
        # and keep async loop in action
        await self.sleep_forever()
