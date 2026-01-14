from .water_system_base import WaterSystemBase
from logger import (
    EventLogger,
    LoggerActionTypes,
)

from config import (
    SHOWER_USABLE_FACTOR,
    WC_WATER,
    LAUNDRY_WATER,
    SINK_WATER,
    SINK_USABLE_FACTOR,
)

class GrayWaterSystem(WaterSystemBase):
    def __init__(self, logger: EventLogger, grey_tank_max: int):
        super().__init__(logger=logger)
        self.grey_tank_max = grey_tank_max

    def _add_grey_water(self, amount: float | int, usable_factor: float, env_time: int, person: str, action: LoggerActionTypes):
        self._add_fresh(
            amount=amount,
            env_time=env_time,
            person=person,
            action=action,
        )

        usable = amount * usable_factor
        losses = amount - usable

        storage = min(usable, self.grey_tank_max - self.grey)
        loss = usable - storage + losses

        if storage > 0:
            self.grey += storage
        if loss > 0:
            self._add_black(
                amount=loss,
                env_time=env_time,
                person=person,
                action=action,
            )

    def _use_gray_or_fresh_water(self, amount: float | int, env_time: int, person: str, action: LoggerActionTypes):
        if self.grey >= amount:
            self._add_grey(
                amount=-amount,
                env_time=env_time,
                person=person,
                action=action,
            )
        else:
            missing = amount - self.grey
            self._add_grey(
                amount=-self.grey,
                env_time=env_time,
                person=person,
                action=action,
            )
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
        self._add_grey_water(
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
        self._add_grey_water(
            amount=LAUNDRY_WATER,
            usable_factor=1.,
            env_time=env_time,
            person=person,
            action=LoggerActionTypes.LAUNDRY.value
        )

    def sink(self, env_time: int, person: str):
        self._add_grey_water(
            amount=SINK_WATER,
            usable_factor=SHOWER_USABLE_FACTOR,
            env_time=env_time,
            person=person,
            action=LoggerActionTypes.SINK.value,
        )