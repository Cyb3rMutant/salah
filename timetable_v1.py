from datetime import datetime, time, timedelta
from typing import Dict

from generator import get_prayer_times

# Maps the app's prayer names to generator.py's output keys.
# "asr shafi" matches the convention the old salahtimes.com CSVs used (acm=1).
PRAYER_KEYS = {
    "Fajr": "fajr",
    "Sunrise": "sunrise",
    "Dhuhr": "dhuhr",
    "Asr": "asr shafi",
    "Maghrib": "maghrib",
    "Isha": "isha",
}

now = datetime.now()  # + timedelta(days=5, hours=11)


def get_daily_table(date) -> Dict[str, time]:
    raw = get_prayer_times(date)
    return {
        name: datetime.strptime(raw[key], "%H:%M").time()
        for name, key in PRAYER_KEYS.items()
    }


class Timetable:
    def __init__(self) -> None:
        self.day = now.date()
        self.times = get_daily_table(self.day)
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
        return self.day.strftime("%A\n%d/%m")

    def get_table(self) -> Dict[str, str]:
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
