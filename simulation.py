import os
import simpy
import random

from matplotlib import pyplot as plt

from water_system import (
    WaterSystemBase,
    GrayWaterSystem,
    NormalWaterSystem,
)
from logger import EventLogger
from config import (
    DAY_IN_MIN,
    TANK_MAX,
    PERSONS,
    SIMULATION_DAYS,
)
from generators import (
    person_per_day,
)


def simulation(env: simpy.Environment, system: WaterSystemBase):
    # set a seed for random values
    random.seed(42)

    for i in range(PERSONS):
        env.process(
            person_per_day(
                env=env,
                name=f"Person {i + 1}",
                system=system,
                days=SIMULATION_DAYS
        )
        )

    env.run(until=SIMULATION_DAYS * DAY_IN_MIN + 1)

    system.save_logger()
    system.logger_analyze()


if __name__ == "__main__":

    grey_water_env = simpy.Environment()
    grey_water_logger = EventLogger(name="logger", storage_path="grey_water_system")
    grey_water_system = GrayWaterSystem(logger=grey_water_logger, grey_tank_max=TANK_MAX)

    normal_water_env = simpy.Environment()
    normal_water_logger = EventLogger(name="logger", storage_path="normal_water_system")
    normal_water_system = NormalWaterSystem(logger=normal_water_logger)

    simulation(
        env=grey_water_env,
        system=grey_water_system,
    )
    simulation(
        env=normal_water_env,
        system=normal_water_system,
    )
