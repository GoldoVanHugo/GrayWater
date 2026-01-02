from abc import abstractmethod


class WaterSystemBase:
    FRESH = "Fresh water"
    BLACK = "Black water"

    def __init__(self):
        # water type
        self.fresh = 0
        self.black = 0

        # report data
        self.report_data = []

        # daily data
        self._daily_data = {
            self.FRESH: 0,
            self.BLACK: 0,
        }

    # ---- Logic ----
    def _add_fresh(self, volume):
        self.fresh += volume
        self._daily_data[self.FRESH] += volume

    def _add_black(self, volume):
        self.black += volume
        self._daily_data[self.BLACK] += volume

    # ---- Consumers ----
    @abstractmethod
    def shower(self, volume: int):
        raise NotImplemented

    @abstractmethod
    def wc(self):
        raise NotImplemented

    # ---- Data ---
    def end_of_day(self):
        # save daily data
        self.report_data.append(self._daily_data.copy())

        # reset daily value for fresh and black water
        self._daily_data[self.FRESH] = 0
        self._daily_data[self.BLACK] = 0
