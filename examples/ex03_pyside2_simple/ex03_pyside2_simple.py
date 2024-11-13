from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
)


def main():
    app = QApplication([])

    win = QWidget()
    win.setWindowTitle("pyside2 simple gui")

    layout = QVBoxLayout()
    label = QLabel("Hello, Pyside2!")
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
