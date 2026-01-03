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


def simulation(env: simpy.Environment, system: WaterSystemBase, title: str):
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

    gray_water_env = simpy.Environment()
    gray_water_logger = EventLogger(name="logger", storage_path="gray_water_system")
    gray_water_system = GrayWaterSystem(logger=gray_water_logger, gray_tank_max=TANK_MAX)

    normal_water_env = simpy.Environment()
    normal_water_logger = EventLogger(name="logger", storage_path="normal_water_system")
    normal_water_system = NormalWaterSystem(logger=normal_water_logger)

    simulation(
        env=gray_water_env,
        system=gray_water_system,
        title="Gray water system"
    )
    simulation(
        env=normal_water_env,
        system=normal_water_system,
        title="Normal water system"
    )
