from physical import *
from datetime import timedelta
import timetable
import time


digital_clocks = {}
digital_clocks["Fajr"] = Prayer(27, 22, 10, 9)
digital_clocks["Dhuhr"] = Prayer(2, 3, 20, 21)
digital_clocks["Asr"] = Prayer(15, 14, 16, 19)
digital_clocks["Maghrib"] = Prayer(18, 17, 13, 6)
digital_clocks["Isha"] = Prayer(23, 24, 12, 5)


prayers = ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]


def run():
    current_time = timetable.now = timetable.now + timedelta(seconds=1)
    # current_time = timetable.now = datetime.now()
    if current_time.hour == current_time.minute == current_time.second == 0:
        new_day()
    # time_label.setText(current_time.strftime("%H:%M:%S"))
    # time_remaining_label.setText(timetable.t.get_time_remaining())
    if timetable.t.updated:
        update_labels()
        timetable.t.updated = False


def new_day():
    timetable.t = timetable.Timetable()
    # date_label.setText(timetable.t.get_date())


def update_labels():
    updated_values = timetable.t.get_table()
    curr = timetable.t.current_prayer
    before = 1
    for p in prayers:
        digital_clocks[p].set_time(updated_values[p], colon=True)
        print(p, before, curr)
        if p == curr:
            prayers[p].green()
            before = 0
        elif before == 1:
            prayers[p].red()
        else:
            prayers[p].yellow()


if __name__ == "__main__":
    new_day()
    while 1:
        run()
        time.sleep(1)
