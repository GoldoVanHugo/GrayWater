from abc import abstractmethod

from logger import (
    EventLogger,
    LoggerActionTypes,
    LoggerWaterTypes,
)


class WaterSystemBase:
    def __init__(self, logger: EventLogger):
        # water type
        self.fresh = 0
        self.black = 0
        self.grey = 0

        self.logger = logger

    # ---- Logic ----
    def _add_fresh(self, amount: float | int, env_time: int, person: str, action: LoggerActionTypes):
        if amount <= 0:
            raise ValueError("Fresh water amount must be more then 0.")

        self.fresh += amount
        self.logger.log(
            env_time=env_time,
            person=person,
            action=action,
            amount=amount,
            water_type=LoggerWaterTypes.FRESH.value,
        )

    def _add_black(self, amount: float | int, env_time: int, person: str, action: LoggerActionTypes):
        if amount <= 0:
            raise ValueError("Black water amount must be more then 0.")

        self.black += amount
        self.logger.log(
            env_time=env_time,
            person=person,
            action=action,
            amount=amount,
            water_type=LoggerWaterTypes.BLACK.value,
        )

    def _add_grey(self, amount: float | int, env_time: int, person: str, action: LoggerActionTypes):
        self.grey += amount
        self.logger.log(
            env_time=env_time,
            person=person,
            action=action,
            amount=amount,
            water_type=LoggerWaterTypes.GREY.value,
        )

    # ---- Consumers ----
    @abstractmethod
    def shower(self, amount: float | int, env_time: int, person: str):
        raise NotImplemented

    @abstractmethod
    def wc(self, env_time: int, person: str,):
        raise NotImplemented

    @abstractmethod
    def laundry(self, env_time: int, person: str):
        raise NotImplemented

    @abstractmethod
    def sink(self, env_time: int, person: str):
        raise NotImplemented

    # ---- Logger ----
    def save_logger(self):
        self.logger.save()

    def load_logger(self, load_path: str = None):
        self.logger.load(load_file=load_path)

    def logger_analyze(self, y_max=None):
        return self.logger.analyze(y_max=y_max)
