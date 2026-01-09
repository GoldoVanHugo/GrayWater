from .water_system_base import WaterSystemBase
from logger import LoggerActionTypes
from config import (
    SHOWER_USABLE_FACTOR,
    WC_WATER,
    LAUNDRY_WATER
)


class NormalWaterSystem(WaterSystemBase):
    # ---- Logic ----
    def _fresh_to_black(self, amount: float | int, env_time: int, person: str, action: LoggerActionTypes, grey_water_factor: float = .0):
        self._add_fresh(
            amount=amount,
            env_time=env_time,
            person=person,
            action=action
        )
        if grey_water_factor > 0.:
            gray_water = amount * grey_water_factor
            self._add_grey(
                amount=gray_water,
                env_time=env_time,
                person=person,
                action=action,
            )

        self._add_black(
            amount=amount,
            env_time=env_time,
            person=person,
            action=action
        )

    # ---- Consumers ----
    def shower(self, amount: float | int, env_time: int, person: str):
        self._fresh_to_black(
            amount=amount,
            env_time=env_time,
            person=person,
            action=LoggerActionTypes.SHOWER.value,
            grey_water_factor=SHOWER_USABLE_FACTOR,
        )

    def wc(self, env_time: int, person: str):
        self._fresh_to_black(
            amount=WC_WATER,
            env_time=env_time,
            person=person,
            action=LoggerActionTypes.WC.value
        )

    def laundry(self, env_time: int, person: str):
        self._fresh_to_black(
            amount=LAUNDRY_WATER,
            env_time=env_time,
            person=person,
            action=LoggerActionTypes.LAUNDRY.value,
            grey_water_factor=1.
        )