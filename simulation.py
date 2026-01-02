import simpy
from matplotlib import pyplot as plt

from water_system import (
    WaterSystemBase,
    GrayWaterSystem,
    NormalWaterSystem,
)
from config import (
    DAY_IN_MIN,
    TANK_MAX,
    PERSONS,
    SIMULATION_DAYS,
)
from generators import (
    person,
    day_process,
)


def simulation(env: simpy.Environment, system: WaterSystemBase, title: str):
    for i in range(PERSONS):
        env.process(generator=person(
            env=env,
            name=f"Person {i + 1}",
            system=system,
            days=SIMULATION_DAYS,
        ))

    env.process(generator=day_process(
        env=env,
        system=system,
        days=SIMULATION_DAYS,
    ))

    env.run(until=SIMULATION_DAYS * DAY_IN_MIN + 1)

    days = list(range(1, SIMULATION_DAYS + 1))

    report_data = system.report_data
    data_per_label = {}
    for label in report_data[0].keys():
        data_per_label[label] = [d[label] for d in report_data]

    plt.figure(figsize=(10, 6))
    for label, data in data_per_label.items():
        plt.plot(days, data, marker="o", label=label)
    plt.xlabel("Day")
    plt.ylabel("Liter")
    plt.title(f"Water consumption per day for a {title}")
    plt.grid(True)
    plt.legend()
    plt.savefig(f"{title.lower().replace(' ', '_')}.png")

    plt.close()


if __name__ == "__main__":
    gray_water_env = simpy.Environment()
    gray_water_system = GrayWaterSystem(gray_tank_max=TANK_MAX)

    normal_water_env = simpy.Environment()
    normal_water_system = NormalWaterSystem()

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
