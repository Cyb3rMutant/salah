from datetime import datetime, timedelta
import sys
from typing import Dict
from PyQt5.QtGui import QFont, QFontDatabase, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QSizePolicy,
    QWidget,
    QLabel,
    QVBoxLayout,
)
from PyQt5.QtCore import QTimer, Qt
import timetable
import os

dirname = os.path.dirname(__file__)

prayers = ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]


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
        # Create the main layout as a horizontal box layout
        main_layout = QHBoxLayout()

        self.isoc_font_medium, self.isoc_font_extrabold = self.init_fonts()

        left_widget = self.init_left()

        right_widget = self.init_right()

        # Add the left and right widgets to the main layout
        main_layout.addWidget(left_widget, 16)  # 4 parts
        main_layout.addWidget(right_widget, 8)  # 1 part

        # Set the main layout to the window
        self.setLayout(main_layout)

        # Set the window title and size
        self.setWindowTitle("PyQt5 Prayer Times Example")
        self.setGeometry(
            300, 300, 600, 400
        )  # Adjusted width and height for a balanced layout
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()

        # Set up a timer to update the labels periodically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.run)
        self.timer.start(1000)  # Update every 1 second (1000 milliseconds)
        self.run()
        self.new_day()

    def init_fonts(self):
        # Load the first TTF font (Regular)
        font_db = QFontDatabase()
        font_id1 = font_db.addApplicationFont(
            os.path.join(dirname, "web/fonts/Montserrat-Medium.ttf")
        )  # Update this path
        font_family1 = font_db.applicationFontFamilies(font_id1)[0]
        self.isoc_font_medium = QFont(font_family1)
        self.isoc_font_medium.setPointSize(40)  # Set the desired font size

        # Load the second TTF font (ExtraBold)
        font_id2 = font_db.addApplicationFont(
            os.path.join(dirname, "web/fonts/Montserrat-ExtraBold.ttf")
        )  # Update this path
        font_family2 = font_db.applicationFontFamilies(font_id2)[0]
        self.isoc_font_extrabold = QFont(font_family2)
        self.isoc_font_extrabold.setPointSize(40)  # Set the desired font size
        self.isoc_font_extrabold.setWeight(
            QFont.ExtraBold
        )  # Set the weight to ExtraBold

        return self.isoc_font_medium, self.isoc_font_extrabold

    def init_left(self):
        # Left side (4 parts): Prayer times
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(
            0, 0, 0, 0
        )  # Remove margins from the left layout
        left_layout.setSpacing(0)  # Remove spacing between widgets in the left layout
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        # left_widget.setStyleSheet("border: 2px solid black;")

        self.prayers = {}
        for prayer in prayers:
            entry_widget = self.init_prayer(prayer)

            left_layout.addWidget(entry_widget)

        return left_widget

    def init_prayer(self, prayer):
        entry_layout = QVBoxLayout()
        entry_layout.setContentsMargins(
            0, 0, 0, 0
        )  # Remove margins from the entry layout
        entry_layout.setSpacing(0)  # Remove spacing between labels
        entry_widget = QWidget()
        entry_widget.setLayout(entry_layout)
        entry_widget.setObjectName(prayer)
        name_label = QLabel(prayer, self)
        time_label = QLabel("", self)
        name_label.setFont(self.isoc_font_extrabold)
        time_label.setFont(self.isoc_font_medium)
        self.prayers[prayer] = time_label

        # self.prayers[prayer].parent.setHidden(1)

        entry_layout.addWidget(name_label, alignment=Qt.AlignBottom | Qt.AlignCenter)
        entry_layout.addWidget(time_label, alignment=Qt.AlignTop | Qt.AlignCenter)

        if prayer == "Sunrise":
            self.prayers[prayer].parent().setHidden(1)

        return entry_widget

    def init_right(self):
        # Right side (1 part): Logo, Time, and Time Remaining
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(
            0, 0, 0, 0
        )  # Remove margins from the right layout
        right_layout.setSpacing(0)  # Remove spacing between widgets in the right layout
        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        # right_widget.setStyleSheet("border: 2px solid black;")

        logo_widget = self.init_logo()
        right_layout.addWidget(logo_widget, 4)

        date_time_widget = self.init_datetime()
        right_layout.addWidget(date_time_widget, 3)

        self.time_remaining_label = self.init_remaining()
        right_layout.addWidget(self.time_remaining_label, 3)

        return right_widget

    def init_logo(self):
        logo_layout = QVBoxLayout()
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setSpacing(0)
        logo_widget = QWidget()
        logo_widget.setLayout(logo_layout)
        logo_widget.setObjectName("logoWid")
        logo_widget.setStyleSheet("QWidget#logoWid {border:2px solid black;}")

        # Add the logo
        logo_label = QLabel(self)
        pixmap = QPixmap(
            os.path.join(dirname, "web/img/logo.png")
        )  # Replace with the path to your logo file
        # pixmap = pixmap.scaled(200, 200)  # Scale to 50%
        logo_label.setPixmap(
            pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
        # logo_label.setScaledContents(True)
        logo_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        logo_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(logo_label, 4)

        logo_text = QLabel("uwe.isoc.link", self)
        logo_text.setFont(self.isoc_font_extrabold)
        logo_layout.addWidget(logo_text, 1, alignment=Qt.AlignCenter)

        return logo_widget

    def init_datetime(self):
        # Add the current time
        date_time_layout = QVBoxLayout()
        date_time_layout.setContentsMargins(
            0, 0, 0, 0
        )  # Remove margins from the date/time layout
        date_time_layout.setSpacing(0)  # Remove spacing between date and time
        date_time_widget = QWidget()
        date_time_widget.setLayout(date_time_layout)
        date_time_widget.setObjectName("datetimeWid")
        date_time_widget.setStyleSheet("QWidget#datetimeWid {border:2px solid black}")

        # Add the current date
        self.date_label = QLabel("Date: ", self)
        self.date_label.setFont(self.isoc_font_medium)
        date_time_layout.addWidget(
            self.date_label, alignment=Qt.AlignBottom | Qt.AlignCenter
        )

        # Add the current time
        self.time_label = QLabel("Time: ", self)
        self.time_label.setFont(self.isoc_font_medium)
        date_time_layout.addWidget(
            self.time_label, alignment=Qt.AlignTop | Qt.AlignCenter
        )

        return date_time_widget

    def init_remaining(self):
        # Add the remaining time
        time_remaining_label = QLabel("Time remaining: ", self)
        time_remaining_label.setStyleSheet("border: 2px solid black;")
        time_remaining_label.setAlignment(Qt.AlignCenter)
        time_remaining_label.setFont(self.isoc_font_extrabold)
        return time_remaining_label

    def run(self):
        # current_time = timetable.now = timetable.now + timedelta(seconds=1)
        current_time = timetable.now = datetime.now()
        if current_time.hour == current_time.minute == current_time.second == 0:
            self.new_day()
        self.time_label.setText(current_time.strftime("%H:%M:%S"))
        self.time_remaining_label.setText(timetable.t.get_time_remaining())
        if timetable.t.updated:
            self.update_labels()
            timetable.t.updated = False

    def new_day(self):
        timetable.t = timetable.Timetable()
        self.date_label.setText(timetable.t.get_date())

    def update_labels(self):
        updated_values = timetable.t.get_table()
        curr = timetable.t.current_prayer
        before = 1
        for p in prayers:
            self.prayers[p].setText(updated_values[p])
            print(p, before, curr)
            if p == curr:
                self.prayers[p].parent().setStyleSheet(
                    f"QWidget#{p} {{border: 2px solid black; background-color: #75A297}}"
                )
                before = 0
            elif before == 1:
                self.prayers[p].parent().setStyleSheet(
                    f"QWidget#{p} {{border: 2px solid black; background-color: #FF4E60}}"
                )
            else:
                self.prayers[p].parent().setStyleSheet(
                    f"QWidget#{p} {{border: 2px solid black; background-color: #E3AE7A}}"
                )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
