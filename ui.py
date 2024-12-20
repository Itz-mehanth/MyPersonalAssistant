from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon, QRegion
from PyQt5.QtCore import Qt, QPoint
import sys


class FloatingIcon(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up the floating window with frameless and always-on-top flags
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setGeometry(50, 50, 100, 100)  # Set the size of the circular window
        self.setWindowIcon(QIcon("logo.png"))  # Use your desired icon here

        # Create a circular mask for the window
        self.setMask(QRegion(self.rect(), QRegion.Ellipse))

        # Set the window background to transparent for rounded corners
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Add a button in the center of the circular window
        self.button = QPushButton("", self)
        self.button.setIcon(QIcon("logo.png"))
        self.button.setIconSize(self.size())
        self.button.setFlat(True)
        self.button.setGeometry(0, 0, 1, 1)  # Button fills the window
        self.button.clicked.connect(self.expandUI)

        self.expanded = False
        self.offset = None  # For dragging functionality
        self.show()

    def expandUI(self):
        if not self.expanded:
            self.setGeometry(self.x(), self.y(), 300, 200)  # Expand size
            layout = QVBoxLayout()

            # Add more buttons or widgets in expanded mode
            run_button = QPushButton("Run Python Program")
            run_button.clicked.connect(self.runPythonProgram)
            layout.addWidget(run_button)

            # Add a close button
            close_button = QPushButton("Close")
            close_button.clicked.connect(self.closeApp)
            layout.addWidget(close_button)

            # Set new layout
            container = QWidget()
            container.setLayout(layout)
            self.setCentralWidget(container)

            self.expanded = True
        else:
            self.setGeometry(self.x(), self.y(), 100, 100)  # Return to normal size
            self.setCentralWidget(self.button)
            self.expanded = False

        # Update the circular mask
        self.setMask(QRegion(self.rect(), QRegion.Ellipse))

    def runPythonProgram(self):
        print("Running Python Program...")

    def closeApp(self):
        self.close()

    # Add dragging functionality to the window
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = FloatingIcon()
    sys.exit(app.exec_())
