from PySide2.QtCore import *
from PySide2.QtWidgets import *


def main():
    app = QApplication([])

    win = QWidget()
    win.setWindowTitle("PyStand")

    layout = QVBoxLayout()
    label = QLabel("Hello, World !!")
    label.setAlignment(Qt.AlignCenter)
    layout.addWidget(label)

    btn = QPushButton(text="PUSH ME")
    layout.addWidget(btn)

    win.setLayout(layout)
    win.resize(400, 300)

    btn.clicked.connect(
        lambda: [
            print("exit"),
            win.close(),
        ]
    )

    win.show()
    app.exec_()
