import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QProgressBar, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer

class FloatingSearchBar(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        # Set background color to white with rounded corners
        self.setStyleSheet("""
            background-color: white;
            color: black;
        """)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create a horizontal layout for the search bar and buttons
        self.inputLayout = QHBoxLayout()

        self.searchBar = QLineEdit(self)
        self.searchBar.setPlaceholderText("Enter your search...")
        self.searchBar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.searchBar.setStyleSheet(
            """
            color: black;
            font-size: 24px
            """
        )
        self.inputLayout.addWidget(self.searchBar)

        self.submitButton = QPushButton("Submit", self)
        self.submitButton.clicked.connect(self.onSubmit)
        self.submitButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.submitButton.setStyleSheet(
            """
            background-color: green;
            color: white;
            font-size: 18px;
            """
        )
        self.inputLayout.addWidget(self.submitButton)

        self.closeButton = QPushButton("Close", self)
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.closeButton.setStyleSheet(
            """
            background-color: red;
            color: white;
            font-size: 18px;
            """
        )
        self.inputLayout.addWidget(self.closeButton)

        # Add the horizontal layout to the main vertical layout
        self.layout.addLayout(self.inputLayout)

        self.progressBar = QProgressBar(self)
        self.progressBar.setValue(0)
        self.layout.addWidget(self.progressBar)
        self.progressBar.hide()  # Initially hide the progress bar

        self.setLayout(self.layout)
        self.setFixedSize(800, 100)  # Set initial size of the window

    def onSubmit(self):
        if self.searchBar.text().strip() == "":
            return  # Optionally handle empty input

        self.progressBar.setValue(0)
        self.progressBar.show()
        self.expandWindow()

        # Simulate a loading process
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateProgressBar)
        self.timer.start(100)

    def expandWindow(self):
        self.setFixedSize(800, 150)  # Expand the window height
        self.layout.update()

    def updateProgressBar(self):
        if self.progressBar.value() < 100:
            self.progressBar.setValue(self.progressBar.value() + 10)
        else:
            self.timer.stop()
            self.progressBar.hide()
            self.setFixedSize(700, 100)  # Restore original size
            self.layout.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    searchBar = FloatingSearchBar()
    searchBar.show()
    sys.exit(app.exec_())
