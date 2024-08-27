from datetime import datetime, timedelta
from typing import Dict
import pandas as pd


def is_end_of_month(dt):
    todays_month = dt.month
    tomorrows_month = (dt + timedelta(days=1)).month
    return tomorrows_month != todays_month


def is_start_of_month(dt):
    todays_month = dt.month
    yesterdays_month = (dt - timedelta(days=1)).month
    return yesterdays_month != todays_month


now = datetime.now()


class Monthly_table:
    def __init__(self, file) -> None:
        self.table = self.init_table(file)
        self.next_table = None

    def init_table(self, file):
        return (
            pd.read_csv("./prayers/" + file + ".csv")
            .drop(columns=["Date"])
            .rename(columns={"Asar": "Asr"})
        ).apply(lambda col: pd.to_datetime(col, format="%H:%M").dt.time)

    def get_daily_table(self, date) -> pd.Series:
        if is_end_of_month(date):
            self.next_table = self.init_table(
                (date + timedelta(days=1)).strftime("%m_%y")
            )
        if is_start_of_month(date) and self.next_table != None:
            self.table = self.next_table
            self.next_table = None
        return self.table.iloc[date.day - 1]


month = Monthly_table(now.strftime("%m_%y"))


class Timetable:
    def __init__(self) -> None:
        self.day = now.date()
        self.times = month.get_daily_table(self.day)
        self.set_current_and_next_prayer()

    def set_current_and_next_prayer(self):
        self.updated = True
        curr_time = (now + timedelta(seconds=1)).time()
        previous_prayer = list(self.times.keys())[-1]

        for prayer, prayer_time in self.times.items():
            if curr_time < prayer_time:
                self.current_prayer, self.next_prayer = previous_prayer, prayer
                return
            previous_prayer = prayer
        # If all prayers for the day are past, return the last prayer as current and the first prayer of the next day as next
        self.current_prayer, self.next_prayer = (
            previous_prayer,
            list(self.times.keys())[0],
        )

    def get_date(self) -> str:
        return self.day.strftime("%A<br/>%d/%m")

    def get_table(self) -> Dict[str, int]:
        return {k: self.times[k].strftime("%H:%M") for k in self.times.keys()}

    def get_time_remaining(self):
        time = now
        next_prayer_time = datetime.combine(self.day, self.times[self.next_prayer])

        # If next prayer time has passed, this is an edge case where we set it to tomorrow's Fajr
        if next_prayer_time < time:
            next_prayer_time += timedelta(days=1)

        diff = next_prayer_time - time
        if diff.total_seconds() <= 1:
            self.set_current_and_next_prayer()

        return str(diff).split(".")[0]


t = Timetable()
