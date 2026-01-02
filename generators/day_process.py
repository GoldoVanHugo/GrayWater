from simpy import Environment

from water_system import  WaterSystemBase

from config import DAY_IN_MIN

def day_process(env: Environment, system: WaterSystemBase, days: int):
    for day in range(days):
        yield env.timeout(DAY_IN_MIN)
        system.end_of_day()
        print(f"end day {env.now}")
