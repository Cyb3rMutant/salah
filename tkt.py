from datetime import datetime
import sys
from typing import Dict
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QTime
import timetable

prayers = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]


# Example of the external function get_table
def get_table() -> Dict[str, str]:
    # This function should return a dictionary with the prayer names as keys
    # and their updated values as the values.
    return {
        "Fajr": "5:00 AM",
        "Dhuhr": "1:00 PM",
        "Asr": "4:30 PM",
        "Maghrib": "6:45 PM",
        "Isha": "8:00 PM",
    }


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a layout
        layout = QVBoxLayout()

        # Create and add the time label
        self.time_label = QLabel("Time: ", self)
        layout.addWidget(self.time_label)
        self.time_remaining_label = QLabel("Time: ", self)
        layout.addWidget(self.time_remaining_label)

        # Create a label for each prayer and add it to the layout
        self.prayers = {}
        for prayer in prayers:
            self.prayers[prayer] = QLabel(prayer, self)
            layout.addWidget(self.prayers[prayer])

        # Set the layout to the window
        self.setLayout(layout)

        # Set the window title and size
        self.setWindowTitle("PyQt5 Text Update Example")
        self.setGeometry(300, 300, 300, 200)

        # Set up a timer to update the labels periodically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_labels)
        self.timer.start(1000)  # Update every 1 second (1000 milliseconds)

    def update_labels(self):
        """
        # Get the updated values from the get_table function
        updated_values = get_table()

        # Update the time label with the current time
        current_time = QTime.currentTime().toString("hh:mm:ss A")
        self.time_label.setText(f"Time: {current_time}")

        # Update each prayer label with the new value
        for prayer, time in updated_values.items():
            if prayer in self.prayers:
                self.prayers[prayer].setText(f"{prayer}: {time}")
        """
        current_time = timetable.now = datetime.now()
        self.time_label.setText(current_time.strftime("%H:%M:%S"))
        self.time_remaining_label.setText(timetable.t.get_time_remaining())
        if timetable.t.updated:
            updated_values = timetable.t.get_table()
            for prayer, time in updated_values.items():
                if prayer in self.prayers:
                    self.prayers[prayer].setText(f"{prayer}: {time}")
            timetable.t.updated = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
