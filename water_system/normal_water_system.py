from .water_system_base import WaterSystemBase
from config import (
    WC_WATER,
)


class NormalWaterSystem(WaterSystemBase):
    # ---- Logic ----
    def _fresh_to_drain(self, volume: int):
        self._add_fresh(volume=volume)
        self._add_black(volume=volume)

    # ---- Consumers ----
    def shower(self, volume: int):
        self._fresh_to_drain(volume=volume)

    def wc(self):
        self._fresh_to_drain(volume=WC_WATER)
