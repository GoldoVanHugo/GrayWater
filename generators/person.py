import random

from simpy import Environment

from water_system import  WaterSystemBase
from config import (
    SHOWER_TIME,
    SHOWER_WATER_PER_MIN,
    WC_PER_DAY,
    DAY_IN_MIN,
)


def person(env: Environment, name: str, system: WaterSystemBase, days: int):
    for day in range(days):
        # ---- Shower ----
        # --- Get random shower time between 6 a.m. and 8 p.m. ---
        yield env.timeout(random.randint(6 * 60, 9 * 60))
        print(f"Day {day}, person {name}, shower start {env.now}")
        for _ in range(SHOWER_TIME):
            system.shower(volume=SHOWER_WATER_PER_MIN)
            yield env.timeout(1)
        print(f"Day {day}, person {name}, shower stop {env.now}")

        # ---- WC ----
        for _ in range(WC_PER_DAY):
            yield env.timeout(random.randint(60, 180))
            system.wc()
            print(f"WC {name} {env.now}")

        rest_time = DAY_IN_MIN - (env.now % DAY_IN_MIN)
        yield env.timeout(rest_time)