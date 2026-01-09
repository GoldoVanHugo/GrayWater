import pandas as pd
import os
import  csv

from matplotlib import pyplot as plt

from config import DAY_IN_MIN

from .enums import (
    LoggerHeaderKey,
    LoggerActionTypes,
    LoggerWaterTypes,
)


class EventLogger:
    def __init__(self, name: str, storage_path: str = None):
        self.name = name
        self.storage_path = storage_path
        self.events = []
        self.df = None

    def log(
            self,
            env_time: float | int,
            person: str,
            action: LoggerActionTypes,
            amount: float | int,
            water_type: LoggerWaterTypes
    ):
        day = env_time // DAY_IN_MIN + 1
        day_time = env_time % DAY_IN_MIN
        hour = int(day_time // 60)
        minute = int(day_time % 60)

        self.events.append({
            LoggerHeaderKey.TIME_MIN.value: env_time,
            LoggerHeaderKey.DAY.value: day,
            LoggerHeaderKey.TIME_OF_DAY.value: f"{hour:02d}:{minute:02d}",
            LoggerHeaderKey.PERSON.value: person,
            LoggerHeaderKey.ACTION.value: action,
            LoggerHeaderKey.AMOUNT_L.value: abs(amount),
            LoggerHeaderKey.WATER_TYPE.value: water_type,
        })

    def save(self):
        if len(self.events) < 1:
            raise ValueError("No event data to save.")

        path = self.name
        if self.storage_path is not None:
            if not os.path.exists(self.storage_path):
                os.makedirs(self.storage_path)
            path = os.path.join(self.storage_path, self.name)

        path += ".csv"
        self.df = pd.DataFrame(self.events)
        self.df.to_csv(path, index=False)
        print(f"Logger events stored in {path}")

    def load(self, load_file: str = ""):
        if load_file == "":
            if self.storage_path is not None:
                load_file = self.storage_path
            load_file += self.name + ".csv"

        self.df = pd.read_csv(load_file)

    def get_df(self) -> pd.DataFrame:
        if self.df is None:
            raise ValueError("First save or load logger events.")

        return self.df

    def analyze(self):
        df = self.get_df()
        self.analyze_year_amount(df=df)
        self.analyze_over_days(df=df)
        self.analyze_per_hour(df=df)

    def analyze_year_amount(self, df: pd.DataFrame):
        water_types = self._get_water_types(df=df)
        total = df.groupby(LoggerHeaderKey.WATER_TYPE.value)[LoggerHeaderKey.AMOUNT_L.value].sum()

        plt.figure()
        plt.bar(water_types, [total.get(wt, 0) for wt in water_types])
        plt.ylabel("Water amount in liter")
        plt.title("Water amount over the year")
        plt.grid(axis="y")
        file_name = "water_amount_year"
        self._save_plot(file_name=f"{file_name}.png")
        csv_data = [["Water Type", "Amount"]]
        csv_data += [[wt, total.get(wt, 0)] for wt in water_types]
        self._save_csv(file_name=f"{file_name}.csv", data=csv_data)

    def analyze_over_days(self, df: pd.DataFrame):
        water_types = self._get_water_types(df=df)
        days = self._get_days(df=df)

        csv_data = [["Water Types"] + [f"Day {i}" for i in range(days[0], days[-1] + 1)]]
        plt.figure()
        for wt in water_types:
            daily = (
                df[df[LoggerHeaderKey.WATER_TYPE.value] == wt]
                .groupby(LoggerHeaderKey.DAY.value)[LoggerHeaderKey.AMOUNT_L.value]
                .sum()
                .reindex(range(days[0], days[-1] + 1), fill_value=0)
            )
            plt.plot(daily.values, label=wt)
            data = [wt] + list(daily.values)
            csv_data.append(data)

        plt.xlabel("Day")
        plt.ylabel("Water amount in liter")
        plt.title("Daily water consumption")
        plt.legend()
        plt.grid()
        file_name = "daily_water_consumption"
        self._save_plot(file_name=f"{file_name}.png")
        self._save_csv(file_name=f"{file_name}.csv", data=csv_data)

    def analyze_per_hour(self, df: pd.DataFrame):
        water_types = self._get_water_types(df=df)

        df = df.copy()
        df["hour"] = df[LoggerHeaderKey.TIME_OF_DAY.value].str[:2].astype(int)

        csv_data = [["Water Types"] + [f"Hour {i}" for i in range(24)]]
        plt.figure()
        for wt in water_types:
            hourly = (
                df[df[LoggerHeaderKey.WATER_TYPE.value] == wt]
                .groupby("hour")[LoggerHeaderKey.AMOUNT_L.value]
                .sum()
                .reindex(range(24), fill_value=0)
            )
            plt.plot(hourly.values, label=wt)
            data = [wt] + list(hourly.values)
            csv_data.append(data)

        plt.xlabel("Hours of the day")
        plt.ylabel("Water amount in liter/year")
        plt.title("Hour profile of water amount")
        plt.xticks(range(24))
        plt.legend()
        plt.grid()
        file_name = "hour_profile"
        self._save_plot(file_name=f"{file_name}.png")
        self._save_csv(file_name=file_name, data=csv_data)

    @staticmethod
    def _get_water_types(df: pd.DataFrame):
        return sorted(df[LoggerHeaderKey.WATER_TYPE.value].unique())

    @staticmethod
    def _get_days(df: pd.DataFrame):
        return sorted(df[LoggerHeaderKey.DAY.value].unique())

    def _save_plot(self, file_name: str):
        if self.storage_path is not None:
            store_path = self.storage_path
        else:
            store_path = self.name

        store_path = os.path.join(store_path, file_name)
        plt.savefig(store_path)
        plt.close()

    def _save_csv(self, file_name: str, data: list):
        if self.storage_path is not None:
            store_path = self.storage_path
        else:
            store_path = self.name

        with open(os.path.join(store_path, file_name), mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(data)
