from .water_system_base import WaterSystemBase
from logger import (
    EventLogger,
    LoggerActionTypes,
)

from config import (
    SHOWER_USABLE_FACTOR,
    WC_WATER,
    LAUNDRY_WATER,
)

class GrayWaterSystem(WaterSystemBase):
    def __init__(self, logger: EventLogger, gray_tank_max: int):
        super().__init__(logger=logger)
        self.gray_tank = 0
        self.gray_tank_max = gray_tank_max

    def _add_gray_water(self, amount: float | int, usable_factor: float, env_time: int, person: str, action: LoggerActionTypes):
        self._add_fresh(
            amount=amount,
            env_time=env_time,
            person=person,
            action=action,
        )

        usable = amount * usable_factor
        losses = amount - usable

        storage = min(usable, self.gray_tank_max - self.gray_tank)
        loss = usable - storage + losses

        if storage > 0:
            self._add_gray(
                amount=storage,
                env_time=env_time,
                person=person,
                action=action,
            )
            self.gray_tank += storage

        if loss > 0:
            self._add_black(
                amount=loss,
                env_time=env_time,
                person=person,
                action=action,
            )

    def _use_gray_or_fresh_water(self, amount: float | int, env_time: int, person: str, action: LoggerActionTypes):
        if self.gray_tank >= amount:
            self.gray_tank -= amount
        else:
            missing = amount - self.gray_tank
            self.gray_tank = 0
            self._add_fresh(
                amount=missing,
                env_time=env_time,
                person=person,
                action=action,
            )

        self._add_black(
            amount=amount,
            env_time=env_time,
            person=person,
            action=action,
        )

    # ---- Consumers ----
    def shower(self, amount: float | int, env_time: int, person: str):
        self._add_gray_water(
            amount=amount,
            usable_factor=SHOWER_USABLE_FACTOR,
            env_time=env_time,
            person=person,
            action=LoggerActionTypes.SHOWER.value
        )


    def wc(self, env_time: int, person: str):
        self._use_gray_or_fresh_water(
            amount=WC_WATER,
            env_time=env_time,
            person=person,
            action=LoggerActionTypes.WC.value
        )

    def laundry(self, env_time: int, person: str):
        self._add_gray_water(
            amount=LAUNDRY_WATER,
            usable_factor=1.,
            env_time=env_time,
            person=person,
            action=LoggerActionTypes.LAUNDRY.value
        )