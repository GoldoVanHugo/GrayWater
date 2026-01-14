import random

from simpy import Environment

from water_system import  WaterSystemBase
from config import (
    SHOWER_TIME,
    SHOWER_WATER_PER_MIN,
    WC_PER_DAY,
    DAY_IN_MIN,
    SINK_PER_DAY,
)


class Person:
    def __init__(self, name: str, env: Environment, system: WaterSystemBase):
        self.name = name
        self.env = env
        self.system = system

    def shower(self):
        # shower start time range between 6 a.m. and 10 p.m.
        current_day_time = self.env.now % DAY_IN_MIN

        start_time = random.randint(6 * 60, 22 * 60)

        wait = start_time - current_day_time
        if wait > 0:
            yield self.env.timeout(wait)

        for _ in range(SHOWER_TIME):
            self.system.shower(
                amount=SHOWER_WATER_PER_MIN,
                env_time=self.env.now,
                person=self.name,
            )
            yield self.env.timeout(1)

    def wc(self):
        # wc start time range between 5 a.m. and 11 p.m.
        current_day_time = self.env.now % DAY_IN_MIN

        start_time = random.randint(5 * 60, 23 * 60)

        wait = start_time - current_day_time
        if wait > 0:
            yield self.env.timeout(wait)

        self.system.wc(
            env_time=self.env.now,
            person=self.name
        )

    def laundry(self):
        # laundry start time range between 8 a.m. and 8 p.m.
        current_day_time = self.env.now % DAY_IN_MIN

        start_time = random.randint(8 * 60, 20 * 60)

        wait = start_time - current_day_time
        if wait > 0:
            yield self.env.timeout(wait)


        self.system.laundry(
            env_time=self.env.now,
            person=self.name
        )

    def sink(self):
        # sink start time range between 6 a.m. and 23 p.m.
        current_day_time = self.env.now % DAY_IN_MIN

        start_time = random.randint(6 * 60, 23 * 60)

        wait = start_time - current_day_time
        if wait > 0:
            yield self.env.timeout(wait)

        self.system.sink(
            env_time=self.env.now,
            person=self.name
        )

def person_per_day(env: Environment, name: str, system: WaterSystemBase, days: int):
    person = Person(
        name=name,
        env=env,
        system=system
    )
    laundry_day = random.randint(0, 6)

    for day in range(days):
        env.process(person.shower())
        for _ in range(WC_PER_DAY):
            env.process(person.wc())
        if day % 7 == laundry_day:
            env.process(person.laundry())

        for _ in range(SINK_PER_DAY):
            env.process(person.sink())

        # wait till day end
        rest_time = DAY_IN_MIN - (env.now % DAY_IN_MIN)
        yield env.timeout(rest_time)