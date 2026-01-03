import random

from simpy import Environment

from water_system import  WaterSystemBase
from config import (
    SHOWER_TIME,
    SHOWER_WATER_PER_MIN,
    WC_PER_DAY,
    DAY_IN_MIN,
)


class Person:
    def __init__(self, name: str, env: Environment, system: WaterSystemBase):
        self.name = name
        self.env = env
        self.system = system

    def shower(self):
        # get current day time
        current_day_time = self.env.now % DAY_IN_MIN

        # shower start time range between 6 a.m. and 10 p.m.
        start_min = 6 * 60
        end_min = 22 * 60
        start_time = random.randint(start_min, end_min)

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
        yield self.env.timeout(5*60)
        for _ in range(WC_PER_DAY):
            yield self.env.timeout(random.randint(60, 180))
            self.system.wc(
                env_time=self.env.now,
                person=self.name
            )

    def laundry(self):
        # get current day time
        current_day_time = self.env.now % DAY_IN_MIN

        # laundry start time range between 8 a.m. and 8 p.m.
        start_min = 8 * 60
        end_min = 20 * 60
        start_time = random.randint(start_min, end_min)

        wait = start_time - current_day_time
        if wait > 0:
            yield self.env.timeout(wait)

        self.system.laundry(
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
        env.process(person.wc())
        if day % 7 == laundry_day:
            env.process(person.laundry())

        # wait till day end
        rest_time = DAY_IN_MIN - (env.now % DAY_IN_MIN)
        yield env.timeout(rest_time)