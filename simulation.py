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

    for wt in ["normal", "grey"]:
        water_env = simpy.Environment()
        water_logger = EventLogger(name="logger", storage_path=f"{wt}_water_system", plot_prefix=wt)
        if wt == "grey":
            water_system = GrayWaterSystem(logger=water_logger, grey_tank_max=TANK_MAX)
        else:
            water_system = NormalWaterSystem(logger=water_logger)

        simulation(
            env=water_env,
            system=water_system,
        )
