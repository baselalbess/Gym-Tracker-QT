import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox
)

from PySide6.QtCore import Qt


class GymTracker(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gym Tracker")
        self.resize(1000, 600)

        # MAIN WIDGET
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # MAIN LAYOUT
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # =========================
        # SIDEBAR
        # =========================
        sidebar = QVBoxLayout()

        self.dashboard_btn = QPushButton("Dashboard")
        self.bmi_btn = QPushButton("BMI Calculator")
        self.workout_btn = QPushButton("Workouts")

        sidebar.addWidget(self.dashboard_btn)
        sidebar.addWidget(self.bmi_btn)
        sidebar.addWidget(self.workout_btn)
        sidebar.addStretch()

        # =========================
        # STACKED PAGES
        # =========================
        self.pages = QStackedWidget()

        # Create pages
        self.dashboard_page = self.create_dashboard_page()
        self.bmi_page = self.create_bmi_page()
        self.workout_page = self.create_workout_page()

        # Add pages
        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.bmi_page)
        self.pages.addWidget(self.workout_page)

        # Add to layout
        main_layout.addLayout(sidebar, 1)
        main_layout.addWidget(self.pages, 4)

        # =========================
        # BUTTON CONNECTIONS
        # =========================
        self.dashboard_btn.clicked.connect(
            lambda: self.pages.setCurrentIndex(0)
        )

        self.bmi_btn.clicked.connect(
            lambda: self.pages.setCurrentIndex(1)
        )

        self.workout_btn.clicked.connect(
            lambda: self.pages.setCurrentIndex(2)
        )

        # STYLE
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }

            QLabel {
                color: white;
                font-size: 16px;
            }

            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 8px;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #2980b9;
            }

            QLineEdit {
                padding: 8px;
                border-radius: 5px;
                background-color: white;
                color: black;           
            }

            QTableWidget {
                background-color: white;
                color: black;           
            }
        """)

    # =================================
    # DASHBOARD PAGE
    # =================================
    def create_dashboard_page(self):

        page = QWidget()

        layout = QVBoxLayout()

        title = QLabel("Welcome to Gym Tracker")
        title.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)

        page.setLayout(layout)

        return page

    # =================================
    # BMI PAGE
    # =================================
    def create_bmi_page(self):

        page = QWidget()

        layout = QVBoxLayout()

        title = QLabel("BMI Calculator")

        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("Enter Weight (kg)")

        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("Enter Height (m)")

        calculate_btn = QPushButton("Calculate BMI")

        self.result_label = QLabel("BMI Result")
        self.status_label = QLabel("Status")

        calculate_btn.clicked.connect(self.calculate_bmi)

        layout.addWidget(title)
        layout.addWidget(self.weight_input)
        layout.addWidget(self.height_input)
        layout.addWidget(calculate_btn)
        layout.addWidget(self.result_label)
        layout.addWidget(self.status_label)

        layout.addStretch()

        page.setLayout(layout)

        return page

    # =================================
    # WORKOUT PAGE
    # =================================
    def create_workout_page(self):

        page = QWidget()

        layout = QVBoxLayout()

        title = QLabel("Workout Tracker")

        self.exercise_input = QLineEdit()
        self.exercise_input.setPlaceholderText("Exercise")

        self.sets_input = QLineEdit()
        self.sets_input.setPlaceholderText("Sets")

        self.reps_input = QLineEdit()
        self.reps_input.setPlaceholderText("Reps")

        add_btn = QPushButton("Add Workout")
        delete_btn = QPushButton("Delete Workout")

        # TABLE
        self.table = QTableWidget()
        self.table.setColumnCount(3)

        self.table.setHorizontalHeaderLabels([
            "Exercise",
            "Sets",
            "Reps"
        ])

        add_btn.clicked.connect(self.add_workout)
        delete_btn.clicked.connect(self.delete_workout)

        layout.addWidget(title)
        layout.addWidget(self.exercise_input)
        layout.addWidget(self.sets_input)
        layout.addWidget(self.reps_input)

        layout.addWidget(add_btn)
        layout.addWidget(delete_btn)

        layout.addWidget(self.table)

        page.setLayout(layout)

        return page

    # =================================
    # BMI FUNCTION
    # =================================
    def calculate_bmi(self):

        try:
            weight = float(self.weight_input.text())
            height = float(self.height_input.text())

            bmi = weight / (height * height)

            self.result_label.setText(
                f"BMI: {bmi:.2f}"
            )

            if bmi < 18.5:
                self.status_label.setText(
                    "Underweight"
                )

            elif bmi < 25:
                self.status_label.setText(
                    "Normal"
                )

            elif bmi < 30:
                self.status_label.setText(
                    "Overweight"
                )

            else:
                self.status_label.setText(
                    "Obese"
                )

        except:
            QMessageBox.warning(
                self,
                "Error",
                "Please enter valid numbers"
            )

    # =================================
    # ADD WORKOUT
    # =================================
    def add_workout(self):

        row = self.table.rowCount()

        self.table.insertRow(row)

        self.table.setItem(
            row,
            0,
            QTableWidgetItem(
                self.exercise_input.text()
            )
        )

        self.table.setItem(
            row,
            1,
            QTableWidgetItem(
                self.sets_input.text()
            )
        )

        self.table.setItem(
            row,
            2,
            QTableWidgetItem(
                self.reps_input.text()
            )
        )

    # =================================
    # DELETE WORKOUT
    # =================================
    def delete_workout(self):

        current_row = self.table.currentRow()

        if current_row >= 0:
            self.table.removeRow(current_row)


# =====================================
# RUN APPLICATION
# =====================================
app = QApplication(sys.argv)

window = GymTracker()
window.show()

sys.exit(app.exec())