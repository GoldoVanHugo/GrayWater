from enum import Enum


class LoggerHeaderKey(Enum):
    TIME_MIN = "Time in minutes"
    DAY = "Day"
    TIME_OF_DAY = "Time of day"
    PERSON = "Person"
    ACTION = "Action"
    AMOUNT_L = "Amount in liter"
    WATER_TYPE = "Water type"


class LoggerWaterTypes(Enum):
    FRESH = "Fresh water"
    BLACK = "Black water"
    GREY = "Grey water"


class LoggerActionTypes(Enum):
    SHOWER = "shower"
    WC = "wc"
    LAUNDRY = "laundry"
    SINK = "sink"
