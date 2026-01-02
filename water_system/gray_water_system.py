from .water_system_base import WaterSystemBase
from config import (
    SHOWER_USABLE_FACTOR,
    WC_WATER,
)

class GrayWaterSystem(WaterSystemBase):
    GRAY = "Gray water in tank"

    def __init__(self, gray_tank_max: int):
        super().__init__()
        self.gray = 0
        self.gray_tank_max = gray_tank_max

        self._daily_data[self.GRAY] = 0

    # ---- Logic ----
    def _add_gray(self, volume):
        self.gray += volume
        self._daily_data[self.GRAY] += volume

    def _reset_gray(self):
        self.gray = 0
        self._daily_data[self.GRAY] = 0

    def _add_gray_water(self, volume: int, usable_factor: float):
        self._add_fresh(volume=volume)

        usable = volume * usable_factor
        losses = volume - usable

        storage = min(usable, self.gray_tank_max - self.gray)
        self._add_gray(volume=storage)
        self._add_black(volume=usable - storage + losses)

    def _use_gray_or_fresh_water(self, volume: int):
        if self.gray >= volume:
            self._add_gray(-volume)
        else:
            missing = volume - self.gray
            self._reset_gray()
            self._add_fresh(volume=missing)

    # ---- Consumers ----
    def shower(self, volume: int):
        self._add_gray_water(
            volume=volume,
            usable_factor=SHOWER_USABLE_FACTOR,
        )


    def wc(self):
        self._use_gray_or_fresh_water(volume=WC_WATER)
        self._add_black(volume=WC_WATER)
