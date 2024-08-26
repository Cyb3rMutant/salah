import eel
from datetime import datetime, timedelta
import timetable

eel.init("web")


@eel.expose
def new_day():
    timetable.t = timetable.Timetable()
    eel.set_date(timetable.t.get_date())


def secs():
    while 1:
        current_time = timetable.now = datetime.now()
        if current_time.hour == current_time.minute == current_time.second == 0:
            new_day()
        eel.set_time(current_time.strftime("%H:%M:%S"))
        eel.set_time_remaining(timetable.t.get_time_remaining())
        if timetable.t.updated:
            eel.update_tiles(
                timetable.t.get_table(),
                timetable.t.current_prayer,
            )
            timetable.t.updated = False
        eel.sleep(1)


eel.spawn(secs)


eel.start("main.html", mode="chrome")
